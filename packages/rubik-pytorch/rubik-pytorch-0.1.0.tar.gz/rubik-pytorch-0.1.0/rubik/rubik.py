from tqdm import tqdm
import torch
import rubik.utils as utils
import rubik.logger as logger

class Cube():
    '''
    Rubik's Cube
    '''

    def __init__(self):
        self.__init_config()
        self.__set_core_function()
        self.__set_default_action()
        self.__init_checklist()
        self.__init_other()

    def __init_config(self):
        '''
        Config includes ``func``: customizable functions, ``hparam``: \
        training hyperparameters, and ``data``: training related variables
        '''
        config = {}
        config['proc'] = {} # includes all variable functions
        config['hparam'] = {} # hyperparameters
        config['data'] = {} # datalodaers, current epoch, etc.
        self.config = config


    # Checklist before start training
    def __init_checklist(self):
        '''
        create a checklist 
        '''
        steps = ['hparam', 'dataloader', 'model', 'train', 'val', 
                 'optimizer', 'criterion', 'checkpoint']
        values = [0] * len(steps)
        self.checklist = dict(zip(steps, values))

    def __check(self, item_name):
        if item_name in self.checklist.keys():
            self.checklist[item_name] = 1
        
    def __checklist_complete(self):
        if sum(self.checklist.values()) != len(self.checklist):
            missing_list = []
            for k, v in self.checklist.items():
                if v == 0:
                    missing_list.append(k)
            raise Exception(f'{missing_list} not defined.')

    # Function setup
    def __set_core_function(self):
        self.config['proc']['loop'] = self.__loop
        self.config['proc']['train_wrapper'] = self.__train_wrapper
        self.config['proc']['train_loop'] = self.__train_loop
        self.config['proc']['val_wrapper'] = self.__val_wrapper
        self.config['proc']['val_loop'] = self.__val_loop
        self.config['proc']['checkpoint_wrapper'] = \
                                                self.__checkpoint_wrapper

    # Other initalization
    def __init_other(self):
        # init device
        self.config['data']['device'], _ = utils.get_device()
        self.config['data']['global_step'] = 0

    # Before run starts
    def __init_run(self):
        # init run dir
        base_dir = './runs'
        run_name = f"{self.config['hparam']['run_name']}_{utils.get_time()}"
        run_dir = f'{base_dir}/{run_name}'
        checkpoint_dir = f'{run_dir}/checkpoints'
        utils.create_dir(base_dir)
        utils.create_dir(run_dir)
        utils.create_dir(checkpoint_dir)
        self.config['data']['run_dir'] = run_dir
        self.config['data']['checkpoint_dir'] = checkpoint_dir
        # init logger
        self.config['data']['logger'] = logger.Logger(self.config)
        # log training device
        _, device_log = utils.get_device()
        self.config['data']['logger'].log_message(device_log, 0)

    # Action decorator
    def set_action(self, action_path):
        def wrapper_set_action(func):
            self.config['proc'][action_path] = func
        return wrapper_set_action

    # Action does nothing by default
    def __set_default_action(self):
        action_sections = ['run', 'loop', 'epoch', 'batch', 'train', 'val', 
                           'train_batch', 'val_batch']
        no_action = lambda *args : None
        for sec in action_sections:
            self.config['proc'][f'pre_{sec}'] = no_action
            self.config['proc'][f'post_{sec}'] = no_action
            

    # Training functions 
    def __loop(self, config):
        self.config['proc']['pre_loop'](self.config)
        for epoch in range(self.config['hparam']['epochs']):
            self.config['data']['current_epoch'] = epoch
            self.config['proc']['pre_epoch'](self.config)
            self.config['proc']['train_wrapper'](self.config)
            if self.__is_now(epoch, self.config['hparam']['val_interval']):
                self.config['proc']['val_wrapper'](self.config)
            if self.__is_now(epoch, self.config['hparam']['save_interval']):
                self.config['proc']['checkpoint_wrapper'](self.config)
            self.config['proc']['post_epoch'](self.config)
        self.config['proc']['post_loop'](self.config)

    def __train_wrapper(self, config):
        self.config['proc']['pre_train'](self.config)
        self.config['data']['model'].train() # Set model to training
        self.config['proc']['train_loop'](self.config)
        self.config['proc']['post_train'](self.config)
        for metric in self.config['data']['train_metrics']:
            result = metric.reduce_wrap(self.config)
            self.config['data']['logger'].log_value(
                f'train_{metric.__class__.__name__}', 
                result, 
                self.config['data']['global_step'],
                self.config['data']['current_epoch'])

    def __train_loop(self, config):
        for i, data in enumerate(tqdm(self.config['data']['train_loader'])):
            self.config['data']['current_batch'] = i
            data = self.__transfer_device(data)

            self.config['proc']['pre_train_batch'](data, self.config)
            outputs = self.config['proc']['train_func'](data, self.config)
            self.config['proc']['post_train_batch'](outputs, self.config)

            config['data']['global_step'] += 1
            for metric in self.config['data']['train_metrics']:
                metric.step_wrap(outputs)

    def __val_wrapper(self, config):
        self.config['proc']['pre_val'](self.config)
        with torch.no_grad(): 
            self.config['data']['model'].eval() # Set model to eval
            self.config['proc']['val_loop'](self.config)
        self.config['proc']['post_val'](self.config)
        for metric in self.config['data']['val_metrics']:
            result = metric.reduce_wrap(self.config)
            self.config['data']['logger'].log_value(
                f'val_{metric.__class__.__name__}', 
                result, 
                self.config['data']['global_step'],
                self.config['data']['current_epoch'])

    def __val_loop(self, config):
        for i, data in enumerate(tqdm(self.config['data']['val_loader'])):
            self.config['data']['current_val_batch'] = i
            data = self.__transfer_device(data)
            self.config['proc']['pre_val_batch'](data, self.config)
            outputs = self.config['proc']['val_func'](data, self.config)
            self.config['proc']['post_val_batch'](outputs, self.config)
            for metric in self.config['data']['val_metrics']:
                metric.step_wrap(outputs)

    def __transfer_device(self, data):
        data_batch = []
        for data_i in data:
            data_batch.append(data_i.to(self.config['data']['device']))
        return data_batch

    def __checkpoint_wrapper(self, config):
        self.config['proc']['checkpoint'](self.config)

    def __is_now(self, current, interval):
        return (current + 1) % interval == 0


    # Required setup steps
    def set_hparam(self, hparam_func):
        self.config['hparam'] = hparam_func(self.config)
        self.__check('hparam')
    
    #TODO override to support multiple test loader
    def set_dataloader(self, loader_func):
        train_loader, test_loader = loader_func(self.config)
        self.config['data']['train_loader'] = train_loader
        self.config['data']['val_loader'] = test_loader
        self.__check('dataloader')

    def set_model(self, model_func):
        model = model_func(self.config)
        model = model.to(self.config['data']['device'])
        self.config['data']['model'] = model
        self.__check('model')

    def set_optimizer(self, optimizer_func):
        self.config['data']['optimizer'] = optimizer_func(self.config)
        self.__check('optimizer')

    def set_criterion(self, criterion_func):
        self.config['data']['criterion'] = criterion_func(self.config)
        self.__check('criterion')

    def set_metrics(self, metrics_func):
        train_metrics, val_metrics = metrics_func(self.config)
        self.config['data']['train_metrics'] = train_metrics
        self.config['data']['val_metrics'] = val_metrics
        self.__check('criterion')

    def set_train(self, train_func):
        self.config['proc']['train_func'] = train_func
        self.__check('train')

    def set_val(self, val_func):
        self.config['proc']['val_func'] = val_func
        self.__check('val')

    def set_checkpoint(self, checkpoint_func):
        self.config['proc']['checkpoint'] = checkpoint_func
        self.__check('checkpoint')

    # Start training
    def start_run(self):
        self.config['proc']['pre_run'](self.config)
        self.__checklist_complete()
        self.__init_run()
        self.config['proc']['loop'](self.config)
        self.config['proc']['post_run'](self.config)

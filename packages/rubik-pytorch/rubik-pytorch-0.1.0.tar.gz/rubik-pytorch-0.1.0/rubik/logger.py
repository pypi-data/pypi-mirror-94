import os
import csv
import torch

from PIL import Image

from torchvision.utils import make_grid, save_image

from torch.utils.tensorboard import SummaryWriter
try:
    from torch.utils.tensorboard.summary import hparams
except:
    hparams = lambda x, y: (0, 0, 0)


# Epoch for message logging and iteration for value logging
class Logger():

    def __init__(self, config, cli_log = True, f_log = True, tb_log = True):
        ''' CLI, file and tensorboard logger '''
        self.cli = CLILogger(cli_log)
        self.f = FileLogger(config['data']['run_dir'], f_log)
        self.tb = TensorBoardLogger(config['data']['run_dir'], tb_log)
        self.loggers = [self.f, self.tb, self.cli]

    def log_images(self, img_name, images):
        if images.shape[1] > 3:
            images = images.sum(dim = 1, keepdim = True)
        for logger in self.loggers:
            logger.log_images(img_name, images)

    def log_message(self, message, epoch):
        for logger in self.loggers:
            logger.log_message(message, epoch)

    def log_value(self, value_name, value, iteration, epoch):
        for logger in self.loggers:
            logger.log_value(value_name, value, iteration, epoch)

    def log_hparams(self, hparam, metrics):
        for logger in self.loggers:
            logger.log_hparams(hparam, metrics)

    def log_graph(self, model, data):
        self.tb.log_graph(model, data)

    # Extra layer has to have string name of the layer
    def log_grad(self, model, iteration, num_layer = 3, extra_layers = []):
        selected_layers = self.select_layers(model, num_layer, extra_layers)
        for name, parameters in model.named_parameters():
            true_name = name.split('.')[0]
            if true_name in selected_layers:
                self.tb.log_grad(name, parameters.grad, iteration)

    def select_layers(self, model, num_layer, extra_layers):
        all_layers = []
        for name, _ in model.named_parameters():
            true_name = name.split('.')[0]
            if true_name not in all_layers: all_layers.append(true_name)

        # Select layers according to layers
        selected_layers = []
        for i in range(num_layer - 1):
            factor = int(len(all_layers) / (num_layer - 1))
            selected_layers.append(all_layers[i * factor])
        selected_layers.append(all_layers[-1])
        selected_layers.extend(extra_layers)
        return selected_layers

    def close(self):
        self.tb.close()

class CLILogger():
    def __init__(self, enable = True):
        self.disable = not enable

    def log_images(self, img_name, images):
        if self.disable: return
        print('Image {}.png is saved.'.format(img_name))

    def log_message(self, message, epoch):
        if self.disable: return
        print('epoch: {}, msg: {}'.format(epoch, message))

    def log_value(self, value_name, value, iteration, epoch):
        if self.disable: return
        print('ep: {}, iter: {}, {}: {}'.format(epoch, iteration, 
                                                value_name, value))

    def log_hparams(self, hparam, metrics):
        if self.disable: return
        if not metrics is None:
            hparam.update(metrics)
        print('Hyperparameter: \n {}'.format(hparam))


class FileLogger():
    def __init__(self, log_dir, enable = True):
        self.disable = not enable
        self.metrics_dicts = []
        self.metrics_column = ['epoch', 'iteration'] # Avoid repetitive add
        self.metrics_file = self.init_file('metrics.csv', log_dir)
        self.message_file = self.init_file('log.txt', log_dir)
        self.hparam_file = self.init_file('hparam.csv', log_dir)
        self.data_dir = self.init_dir('data', log_dir)

    def init_file(self, file_name, save_dir):
        if self.disable: return
        file_dir = '{}/{}'.format(save_dir, file_name)
        if os.path.exists(file_dir):
            raise Exception('File {} exists!'.format(file_dir))
        return file_dir
        
    def init_dir(self, dir_name, save_dir):
        if self.disable: return
        sub_dir = '{}/{}'.format(save_dir, dir_name)
        if os.path.exists(sub_dir):
            raise Exception('Path {} exists!'.format(sub_dir))
        else:
            os.mkdir(sub_dir)
        return sub_dir
        
    def log_images(self, img_name, images):
        if self.disable: return
        img_grid = make_grid(images)
        save_image(img_grid, '{}/{}.png'.format(self.data_dir, img_name))

    def log_message(self, message, epoch):
        if self.disable: return
        with open(self.message_file, 'a') as f:
            f.write('epoch: {} | {}\n'.format(epoch, message))

    def log_value(self, value_name, value, iteration, epoch):
        if self.disable: return
        m_dicts = self.metrics_dicts
        if len(m_dicts) == 0 or m_dicts[-1]['iteration'] != iteration:
            m_dicts.append({'epoch' : epoch,
                            'iteration' : iteration,
                            value_name : value})
        else:
            m_dicts[-1][value_name] = value

        if value_name not in self.metrics_column: 
            self.metrics_column.append(value_name)
        with open(self.metrics_file, 'w') as f:
            writer = csv.DictWriter(f, 
                                    fieldnames = self.metrics_column, 
                                    restval = 'NaN')
            writer.writeheader()
            for data in m_dicts:
                writer.writerow(data)

    def log_hparams(self, hparam, metrics):
        if self.disable: return
        if not metrics is None:
            hparam.update(metrics)
        with open(self.hparam_file, 'w') as f:
            writer = csv.writer(f)
            for key, value in hparam.items():
                writer.writerow([key, value])


class TensorBoardLogger():

    def __init__(self, log_dir, enable = True):
        self.writer = ModSummaryWriter(log_dir)
        self.disable = not enable

    def log_images(self, img_name, images):
        if self.disable: return
        img_grid = make_grid(images)
        self.writer.add_image(img_name, img_grid)

    def log_value(self, value_name, value, iteration, epoch):
        if self.disable: return
        self.writer.add_scalar(value_name, value, iteration)

    def log_message(self, message, epoch):
        if self.disable: return
        self.writer.add_text('log', message, epoch)

    def log_hparams(self, hparam, metrics):
        if self.disable: return
        self.writer.add_mod_hparams(hparam, metrics)

    def log_graph(self, model, data):
        if self.disable: return
        self.writer.add_graph(model, data)

    def log_grad(self, name, data, iteration):
        if self.disable: return
        self.writer.add_histogram(name, data, iteration)

    def close(self):
        self.writer.close()

# Custom Hparam Writer that prevent split folders
# https://github.com/pytorch/pytorch/issues/32651#issuecomment-643791116
class ModSummaryWriter(SummaryWriter):
    def add_mod_hparams(self, hparam_dict, metric_dict):
        torch._C._log_api_usage_once("tensorboard.logging.add_hparams")
        if type(hparam_dict) is not dict or type(metric_dict) is not dict:
            raise TypeError('hparam_dict and metric_dict should be dictionary.')
        exp, ssi, sei = hparams(hparam_dict, metric_dict)
        logdir = self._get_file_writer().get_logdir()
        self.file_writer.add_summary(exp)
        self.file_writer.add_summary(ssi)
        self.file_writer.add_summary(sei)
        for k, v in metric_dict.items():
            self.add_scalar(k, v)

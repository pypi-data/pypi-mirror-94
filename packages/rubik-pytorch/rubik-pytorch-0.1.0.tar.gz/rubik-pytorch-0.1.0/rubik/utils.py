import torch
import datetime, os

def get_device():
    message = ''
    # Check device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    message += "Computation device: {}".format(device) + '\n '
    #Additional Info when using cuda
    if device.type == 'cuda':
        message += str(torch.cuda.get_device_name(0)) + '\n'
        message += ' Memory:\n Allocated:{} GB\n Cached:{} GB\n'.format(
            round(torch.cuda.memory_allocated(0)/1024**3,1),
            round(torch.cuda.memory_cached(0)/1024**3,1))
    return device, message

def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')[:-3]

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

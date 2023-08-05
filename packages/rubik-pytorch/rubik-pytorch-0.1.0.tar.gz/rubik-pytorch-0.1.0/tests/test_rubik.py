import unittest
from unittest import TestCase

import rubik.rubik as rubik

import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import Dataset

@unittest.skip('tested')
class TestRubic(TestCase):

    @classmethod
    def setUpClass(self):
        config = {}
        config['input_size'] = 5
        config['hidden_size'] = 32
        config['num_layers'] = 2
        config['dropout'] = 0.2
        self.rubik= rubik.Rubik()
    
    @unittest.skip('legacy test')
    def test_pipeline(self):
        #import pdb; pdb.set_trace()
        def train_func(data, config):
            #print('training')
            pass
        def val_func(data, config):
            #print('val')
            pass

        @self.rubik.set_action('pre_train')
        def pre_loop(config):
            print(config['hparam']['epochs'])

        self.rubik.set_hparam({'epochs':10})
        self.rubik.set_train(train_func)
        self.rubik.set_val(val_func)

        transform = transforms.Compose([transforms.ToTensor(),
                                    transforms.Normalize((0.5, 0.5, 0.5), 
                                                         (0.5, 0.5, 0.5))])
        CIFAR10 = torchvision.datasets.CIFAR10
        trainset = CIFAR10(root='./data', train=False,
                       download=True, transform=transform)
        trainloader = torch.utils.data.DataLoader(trainset, 
                                            batch_size=128, 
                                            shuffle=True, 
                                            num_workers=8,
                                            pin_memory=True) 
        self.rubik.set_dataloader(trainloader, trainloader)

        model = torchvision.models.resnet18()
        self.rubik.set_model(model)

        self.rubik.start()


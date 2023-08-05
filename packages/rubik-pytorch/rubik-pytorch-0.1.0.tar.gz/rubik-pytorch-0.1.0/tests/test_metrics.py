import unittest
from unittest import TestCase

import metrics
import random

import torch
import torchvision
import torchvision.transforms as transforms

#@unittest.skip('tested')
class TestMetrics(TestCase):

    @classmethod
    def setUpClass(self):
        pass
    
    #@unittest.skip('tested')
    def test_accuracy(self):
        acc = metrics.Accuracy()
        for i in range(10):
            for j in range(200):
                bs = 10
                loss = 0
                inputs = torch.rand(bs, 3, 32, 32)
                outputs = torch.rand(bs, 1)
                labels = torch.randint(2 + i, [bs, 1])
                outputs = (loss, inputs, outputs, labels)
                acc.step_wrap(outputs)
            acc_score = acc.reduce_wrap(None)
            self.assertTrue(acc_score < 1 / (i + 2) + 0.1)
            self.assertTrue(acc_score > 1 / (i + 2) - 0.1)

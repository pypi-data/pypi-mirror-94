import numpy as np
import torch
import sklearn.metrics as sk_metrics

class Metric():
    '''
    Metrics holds values during accumulation and reduce to stats in the \
        end, should be aware of memory issue when saving all scores with \
        with large datasets. Also hold the best metrics/epoch for the run.
    '''
    
    def __init__(self):
        self.memory = []
        self.best_result = None
        self.best_epoch = None

    def reset_memory(self):
        self.memory = []

    def step_wrap(self, output_data):
        stats = self.step(output_data)
        self.memory.append(stats)

    def reduce_wrap(self, config):
        result = self.reduce(self.memory, config)
        self.update_result(result, config)
        self.reset_memory()
        return result

    def update_result(self, new, config):
        current_epoch = config['data']['current_epoch']
        old = self.best_result
        if self.best_result is None or self.select_better(old, new) == new:
            self.best_result = new
            self.best_epoch = current_epoch

    def get_best(self):
        '''
        Get the best result from current run

        Returns:
            float: best result of this metric
            int: epoch where the best result is reached
        '''
        return self.best_result, self.best_epoch

    def step(self, output_data):
        '''
        Store scores to avoid large RAM usage

        Args:
            output_data (tuple): Output from train function has form: \
                ``loss.item(), inputs, outputs, labels`` or form defined \
                by customized train function.

        Returns:
            list: an array of transformed stats for computation.
        '''
        raise NotImplementedError('Accumulation not implemented')

    def reduce(self, memory, config):
        '''
        Reduce arrays using the format in the accumulation phase

        Args:
            config (dict): Determine global progress, Metric is memoryless.
        '''
        raise NotImplementedError('Reduce not implemented')

    def select_better(self, old, new):
        '''
        Select the better metrics from two metrics

        Args:
            old (float): old metrics data
            new (float): new metrics data

        Returns:
            float: old or new metrics
        '''
        raise NotImplementedError('Reduce not implemented')


class Loss(Metric):

    def step(self, outputs):
        loss, inputs, outputs, labels = outputs
        return loss

    def reduce(self, memory, config):
        return sum(memory) / len(memory)

    def select_better(self, old, new):
        return min(old, new)

class Accuracy(Metric):
    
    def step(self, output_data):
        loss, inputs, outputs, labels = output_data
        return outputs, labels

    def reduce(self, memory, config):
        outputs = [entry[0] for entry in memory]
        labels = [entry[1] for entry in memory]
        outputs = torch.argmax(torch.cat(outputs), dim = 1).cpu().numpy()
        labels = torch.cat(labels).cpu().numpy()
        score = sk_metrics.accuracy_score(labels, outputs)
        return score

    def select_better(self, old, new):
        return max(old, new)

class AUC(Metric):

    def step(self, output_data):
        loss, inputs, outputs, labels = output_data
        return outputs, labels

    def reduce(self, memory, config):
        outputs = [entry[0] for entry in memory]
        labels = [entry[1] for entry in memory]
        outputs = self.softmax(torch.cat(outputs).cpu().numpy())[:, 1]
        labels = torch.cat(labels).cpu().numpy()
        score = sk_metrics.roc_auc_score(labels, outputs)
        return score

    def softmax(self, x):
        return np.exp(x) / np.exp(x).sum(axis = 1, keepdims = True)

    def select_better(self, old, new):
        return max(old, new)

class F1(Metric):

    def step(self, output_data):
        loss, inputs, outputs, labels = output_data
        return outputs, labels

    def reduce(self, memory, config):
        outputs = [entry[0] for entry in memory]
        labels = [entry[1] for entry in memory]
        outputs = torch.argmax(torch.cat(outputs), dim = 1).cpu().numpy()
        labels = torch.cat(labels).cpu().numpy()
        score = sk_metrics.f1_score(labels, outputs)
        return score

    def select_better(self, old, new):
        return max(old, new)

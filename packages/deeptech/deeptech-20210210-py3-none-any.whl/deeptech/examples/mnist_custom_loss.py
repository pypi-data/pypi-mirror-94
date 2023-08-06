"""doc
# Example: Fashion MNIST with custom loss

This example shows how to solve fashion MNIST with a custom loss.

First we import everything, then we write the config, then we implement the custom loss and finaly we tell deeptech to run this.
"""
from deeptech.data.datasets import FashionMNISTDataset
from deeptech.model.module_from_json import Module
from deeptech.training import tensorboard
from deeptech.training.trainers import SupervisedTrainer
from deeptech.training.losses import SparseCrossEntropyLossFromLogits
from deeptech.training.optimizers import smart_optimizer
from deeptech.core import Config, cli
import torch.nn as nn
from torch.optim import SGD


class FashionMNISTConfig(Config):
    def __init__(self, training_name, data_path, training_results_path):
        super().__init__(training_name, data_path, training_results_path)
        # Config of the data
        self.data_dataset = FashionMNISTDataset

        # Config of the model
        self.model_model = lambda config: Module.create_from_file("deeptech/examples/mnist_model.json", "MNISTModel", num_classes=10, logits=True)

        # Config for training
        self.training_loss = MyLoss
        self.training_optimizer = smart_optimizer(SGD)
        self.training_trainer = SupervisedTrainer
        self.training_epochs = 10
        self.training_batch_size = 32


# Should be in a loss.py
class MyLoss(nn.Module):
    def __init__(self, config=None, model=None):
        super().__init__()
        self.loss = SparseCrossEntropyLossFromLogits()

    def forward(self, y_pred, y_true):
        loss = self.loss(y_pred=y_pred, y_true=y_true)
        tensorboard.log_scalar("loss/my_ce", loss)
        return loss


# Run with parameters parsed from commandline.
# python -m deeptech.examples.mnist_custom_loss --mode=train --input=Datasets --output=Results
if __name__ == "__main__":
    cli.run(FashionMNISTConfig)

import numpy as np
from train import train
from nn import NeuralNet
from layers import Linear, Tanh, Sigmoid

inputs = np.array([
    [0, 0],
    [1, 0],
    [0, 1],
    [1, 1]
])

targets = np.array([
    [1, 0],
    [0, 1],
    [0, 1],
    [1, 0]
])

targets = targets[:, 1].reshape(len(targets), 1)

net = NeuralNet([
    Linear(input_size  = 2, output_size = 2),
    Sigmoid(),
    Linear(input_size = 2, output_size = 1),
    Sigmoid()
])

from loss import BinaryCrossentropy, MSE
from optimizers import SGD
train(net, inputs, targets, loss = BinaryCrossentropy(), optimizer = SGD(0.1))

for x, y in zip(inputs, targets) :
    predicted = net.forward(x)
    print(x, predicted, y)
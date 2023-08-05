"""
Fizzbuzz :

for each of the numbers from 1 to 100 :
if the number is divisible by 3, print "fuzz"
if the number is divisible by 5, print "buzz"
if the number is divisible by 15, print "fizzbuzz"
otherwise, print the number
"""

import numpy as np

from SimpleDL.train import train
from SimpleDL.nn import NeuralNet
from SimpleDL.layers import Linear, Tanh
from SimpleDL.optimizers import SGD
from typing import List

def fizz_buzz_encode(x : int) -> List[int] :
    if x % 15 == 0 :
        return [0, 0, 0, 1]
    if x % 5 == 0 :
        return [0, 0, 1, 0]
    if x % 3 == 0 :
        return [0, 1, 0, 0]
    else :
        return [1, 0,0, 0]

def binary_encode(x : int) -> List[int] :
    '''10 digit binary encoding of x'''
    return [x >> i  & 1 for i in range(10)]

inputs = np.array([
    binary_encode(x)
    for x in range(101, 1024)
])

targets = np.array([
    fizz_buzz_encode(x)
    for x in range(101, 1024)
])

net = NeuralNet([
    Linear(input_size = 10, output_size = 50),
    Tanh(),
    Linear(input_size = 50, output_size=4)
])

train(net,
      inputs,
      targets,
      num_epochs=5000,
      optimizer = SGD(lr = 0.001))

for x in range(1, 101) :
    predicted = net.forward(binary_encode(x))
    predicted_idx = np.argmax(predicted)
    actual_idx = np.argmax(fizz_buzz_encode(x))
    labels = [str(x), "fizz", "buzz", "fizzbuzz"]
    print(x, labels[predicted_idx], labels[actual_idx])
"""
Our neural net will be made up of layers.
Each layer passes its inputs forward and propagate grads backward.
"""

import numpy as np
from tensor import Tensor
from typing import Dict, Callable

class Layer :
    def __init__(self) -> None :
        self.params : Dict[str, Tensor] = {}
        self.grads : Dict[str, Tensor] = {}
        pass

    def forward(self, inputs : Tensor) -> Tensor:
        """
        produce outputs
        """
        raise NotImplementedError
    def backward(self, grad : Tensor) -> Tensor:
        '''backpropagate through the layer'''
        raise NotImplementedError


class Linear(Layer) :
    '''computes = output = inputs * w + b '''
    def __init__(self, input_size: int, output_size: int) -> None :
        #inputs will be (batch_size, input_size)
        #outputs will be (batch_size, output_size)
        super().__init__()
        self.params["w"] = np.random.randn(input_size, output_size)
        self.params["b"] = np.random.randn(output_size)

    def forward(self, inputs : Tensor) -> Tensor:
        """outputs = inputs @ w  + b """
        self.inputs = inputs # save a copy
        return inputs @ self.params["w"] + self.params["b"] #which derivative is this ?

    def backward(self, grad : Tensor) -> Tensor:
        """
        if y = f(x), and x = a * b + c
        then dY/da = f'(x) * b
        then dY/db = f'(x) * a
        and dY/dC = f'(x)

        if y = f(x) and x = a @ b + c
        then dy/da = f'(x) @ b.T
        and dy/db = a.T @ f'(x)
        and dY/dC = f'(x)
        """

        self.grads['b'] = np.sum(grad, axis = 0)
        self.grads['w'] = self.inputs.T @ grad
        return grad @ self.params['w'].T #grad = dLdZ2 * dZ2/dA1

F = Callable[[Tensor], Tensor]

class Activation(Layer) :
    '''an activation layer just applies a function element-wise to its inputs'''
    def __init__(self, f : F, f_prime : F) -> None :
        super().__init__()
        self.f = f
        self.f_prime = f_prime

    def forward(self, inputs : Tensor) -> Tensor:
        self.inputs = inputs # save
        return self.f(inputs)

    def backward(self, grad : Tensor) -> Tensor:
        '''
        if y = f(x) and x = g(z)
        then dY/dZ = f'(x) * g'(z)
        '''

        return self.f_prime(self.inputs) * grad

def tanh(x : Tensor) -> Tensor :
    return np.tanh(x)

def tanh_prime(x : Tensor) -> Tensor :
    y = tanh(x)
    return 1 - y ** 2

class Tanh(Activation) :
    def __init__(self):
        super().__init__(tanh, tanh_prime)

def sigmoid(x : Tensor) -> Tensor :
    return 1 / (1 + np.exp(-x))

def sigmoid_prime(x : Tensor) -> Tensor :
    return sigmoid(x) * (1 - sigmoid(x))

class Sigmoid(Activation) :
    def __init__(self):
        super().__init__(sigmoid, sigmoid_prime)
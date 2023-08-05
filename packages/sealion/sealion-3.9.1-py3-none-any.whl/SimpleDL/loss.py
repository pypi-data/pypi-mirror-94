"""
A loss function measures how good our predictions are.
We can use this to adjust the params.
"""

import numpy as np

from tensor import Tensor

class Loss :
    def loss(self, predicted : Tensor, actual : Tensor) -> float :
        raise NotImplementedError
    def grad(self, predicted : Tensor, actual : Tensor) -> Tensor :
        raise NotImplementedError


class MSE(Loss) :
    def loss(self, predicted : Tensor, actual : Tensor) -> float :
        error = np.sum((predicted - actual) ** 2)
        return error
    def grad(self, predicted : Tensor, actual : Tensor) -> Tensor :
        return 2 * (predicted - actual)

class BinaryCrossentropy(Loss) :
    def loss(self, predicted : Tensor, actual : Tensor) -> float :
        error = np.sum((predicted - actual) ** 2)
        return error
    def grad(self, predicted : Tensor, actual : Tensor) -> Tensor :
        return - ((actual/predicted) - (1-actual)/(1-predicted))
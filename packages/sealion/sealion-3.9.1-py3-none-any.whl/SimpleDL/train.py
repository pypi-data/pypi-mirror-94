"""function to train the neural network"""

from tensor import Tensor
from nn import NeuralNet
from loss import Loss, MSE
from optimizers import Optimizer, SGD
from data import DataIterator, BatchIterator

def train(net : NeuralNet,
          inputs : Tensor,
          targets : Tensor,
          num_epochs : int = 5000,
          iterator  : DataIterator = BatchIterator(),
          loss : Loss = MSE(),
          optimizer : Optimizer = SGD()) -> None :
    for epoch in range(num_epochs) :
        epoch_loss = 0.0
        for batch in iterator(inputs, targets) :
            predicted = net.forward(batch.inputs)
            epoch_loss += loss.loss(predicted, batch.targets)
            grad = loss.grad(predicted, batch.targets) #this is dLdY
            net.backward(grad) #backpropagate this back
            optimizer.step(net)
        print(epoch, epoch_loss)
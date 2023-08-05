from typing import Callable
from DataScienceFromScratch.LinearAlgebra import Vector

def difference_quotient(f : Callable[[float], float], x : float, h : float) -> float :
    '''approximate the derivative with f(x+h) - f(x)/ h'''
    return (f(x+h) - f(x))/h


#taking the derivative of most functions is easy with the power and chain rules
def square(x : float) -> float :
    return x ** 2

def derivative(x : float) -> float :
    return 2 * x

#using a small h leads to very close derivatives, look at the plot of the actual derivative rule and the difference_quotient method
xs = range(-10, 11)
actuals = [derivative(x) for x in xs]
estimates = [difference_quotient(square, x, h = 0.00001) for x in xs]

#plot to show that they are basically the same
import matplotlib.pyplot as plt
plt.title("Actual derivs vs. Estimates")
plt.plot(xs, actuals, 'rx', label = "actual_derivs") #red x-s
plt.plot(xs, estimates, 'b+', label = "different_quotient_estimates") #blue plus-s
plt.legend(loc = 9)
plt.show()

#partial derivs! -> find a partial derivatives @ i by the + difference_quotient of the function at that index

def partial_difference_quotient(f : Callable[[Vector], float],
                                v : Vector,
                                i : int,
                                h : float) -> float :
    '''returns partial derivative of how the function's output changes on small changes of the ith index, feature, aka axis'''
    w = [v_j + (h if j == i else 0 )
         for j, v_j in enumerate(v)]

    return (f(w) - f(v))/h


def estimate_gradient(f : Callable[[Vector], float],
                      v : Vector,
                      h : float = 0.00001) :
    return [partial_difference_quotient(f, v, i, h) for i in range(len(v))] #for every axis of v find the direction of steepest ascent

def vector_function(v : Vector) -> float :
    return v[0] + v[1]**2 - v[2]

print("Partial derivative gradient : " , estimate_gradient(vector_function, [1, 2, 3]))

#gradients can be used to minimize cost functions, train models, and get to the bottom of a function
import random
from DataScienceFromScratch.LinearAlgebra import distance, add, scalar_multiply

def gradient_step(v : Vector, gradient : Vector, step_size : float) -> Vector :
    '''moves in gradient descent direction'''
    assert len(v) == len(gradient)
    step = scalar_multiply(step_size, gradient)
    return add(v, step)

def sum_of_squares_gradient(v : Vector) -> Vector :
    return [2 * v_i for v_i in v]

#pick a random starting point -> kinda like picking random weights
v = [random.uniform(-10, 10) for i in range(3)]

for epoch in range(1000) :
    grad = sum_of_squares_gradient(v) #compute the gradient of v
    v = gradient_step(v, grad, -0.01) #take a negative gradient step
    print(epoch, v)

assert distance(v, [0, 0, 0]) < 0.0001 # v should be very close to 0 (lowest point on graph)

#Using GD to fit models
inputs = [(x, 20 * x + 5) for x in range(-50, 50)]

def linear_gradient(x : float, y : float, theta : Vector) -> Vector :
    slope, intercept = theta
    predicted = slope * x + intercept #prediction
    error = (predicted - y) #should be mse but okay
    squared_error = error ** 2 #wow
    grad = [2 * error * x, 2 * error] #the gradients of dL/dW, dL/dB(intercept)
    return grad

'''
How the fitting process really is like : 

1. Start with a random value for theta. 
2. Compute the mean of the gradients
3. Adjust theta in that direction
4. Repeat 2 and 3 until not needed
'''

from DataScienceFromScratch.LinearAlgebra import vector_mean

theta = [random.uniform(-1, 1), random.uniform(-1, 1)] #random values of slope, intercept

learning_rate = 0.001

for epoch in range(5000)  :
    #compute the mean of the grads
    grad = vector_mean([linear_gradient(x, y, theta) for x, y in inputs])
    theta = gradient_step(theta, grad, -learning_rate) #take a step in the opposite direction of steepest ascent of J(theta),  learning rate step size
    print(epoch, theta)

slope, intercept = theta
assert 19.9 < slope < 20.1, "slope should be about 20"
assert 4.9 < intercept < 5.1 , "intercept should be around 5"


'''
Using SGD or Mini-Batch-Gradient Descent for faster convergence
'''

from typing import TypeVar, List, Iterator
T = TypeVar("T") #helps create generate functions which take in lists of any datatypes and return that datatype too
def minibatches(dataset : List[T],
                batch_size : int,
                shuffle : bool = True) -> Iterator[List[T]] :
    '''generates batch_size-batches in this generator (from the dataset)'''
    batch_starts = [start for start in range(0, len(dataset), batch_size)]
    if shuffle : random.shuffle(batch_starts) #shuffle batches if desired so
    for start in batch_starts :
        end = start + batch_size
        yield dataset[start : end]

'''solving y = 20x + 5 using minibatches'''

theta = [random.uniform(-1, 1), random.uniform(-1, 1)]

for epoch in range(1000) :
    for batch in minibatches(inputs, batch_size = 20) :
        grad = vector_mean([linear_gradient(x, y , theta) for x, y in inputs]) #take the gradient
        theta = gradient_step(theta, grad, -learning_rate) #move in the direction
    print(epoch, theta)

slope, intercept = theta
assert 19.9 < slope < 20.1, "slope should be about 20"
assert 4.9 < intercept < 5.1 , "intercept should be around 5"

#sgd -> taking gradient steps based on one training example, bad if the example is noisy, training is noisy
# and will convergence fast and slow in a way


theta = [random.uniform(-1, 1), random.uniform(-1, 1)]

for epoch in range(100) :
    for x, y in inputs :
        grad = linear_gradient(x, y, theta)
        theta = gradient_step(theta, grad, -learning_rate)
    print(epoch, theta)

slope, intercept = theta
assert 19.9 < slope < 20.1, "slope should be about 20"
assert 4.9 < intercept < 5.1, "intercept should be around 5"

'''
"The gradient for a single point might lie in a very different direction from the gradient for the dataset as a whole."
- Joel Grus, DSFS

- SGD samples randomly, one input at a time
- Mini Batch takes bigger batches, meant to be the midpoint bewtween Batch and Scochastic Gradient Descent
'''







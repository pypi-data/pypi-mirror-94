import time
start_time = time.time()
import math
import numpy as np
from tqdm import tqdm
from data_preprocessing import one_hot, revert_one_hot
import pandas as pd
data = pd.read_csv('/users/anish/downloads/breast-cancer-wisconsin.data')

def data_collection(data) :
    training_data = data[['ID', 'clump_thickness','cell_uniformity', 'shape_uniformity', 'chromatin','nucleoli']]
    labels = data['class']

    training_data = training_data.drop(['ID', 'chromatin'], axis = 1)
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    training_data = training_data._get_numeric_data()

    training_data = scaler.fit_transform(training_data)

    training_data, labels = np.array(training_data), np.array(labels)

    split = 30
    x_test, y_test = training_data[:split], labels[:split]
    x_train,y_train = training_data[split:], labels[split:]

    x_train, y_train, x_test, y_test = np.array(x_train, dtype = float), np.array(y_train, dtype = float), np.array(x_test, dtype = float), np.array(y_test, dtype = float)
    y_train, y_test = y_train/2 - 1, y_test/2 - 1

    return x_train,x_test, y_train, y_test

x_train, x_test, y_train, y_test = data_collection(data)


def _preprocess_data(data, labels):
    """
    Convert all data + labels to numpy arrays, and make data 2D if needed and labels 2D (for it to work with subtraction with the np.dot, etc.)
    :param self:
    """
    data, labels = np.array(data), np.array(labels)

    if len(data.shape) < 2:
        data = np.array([np.array([x_i]) for x_i in data])

    if len(labels.shape) < 2:
        labels = np.array([np.array([y_i]) for y_i in labels])

    return data, labels


class LinearRegression():
    def __init__(self):
        self.information = """

                Linear Regression is arguably the most basic and simple machine learning algorithm there is. There is a huge chance that you have used this algorithm in your math class in the past or heard of it. All it tries to
                do is find the line of best fit in data. Seems simple to do with paper, but how about in code? And what if the graph is 100+ dimensions? How would you find the best line in the first place? All of this creates 
                an optimization problem for finding the line that reduces the residuals (distance from point and line) to as much as possible. Linear Regression utilizes an algorithm known as gradient descent, also found in 
                all other regression models and heavily in neural networks today. Make sure to read on, as the lines below explain how to use the library (the syntax is consistent for all models.)

                To train a model : - Data must be 2D, meaning a list/vector of list/vectors. For example : [[1, 1, 1], [2, 2, 2], [3, 3, 3]] - All data points must be of the same size. This works : [[1, 1], [1, 2], [0, 1]]. 
                This doesn't : [[0], [1, 2], [3, 4]] (first data point has only a size of 1) - labels must 
                be stored in a 1D dataset like : [1, 2, 3, 4, 4]. You cannot do : [[1, 2, 3, 4]] or [[1], [2], [3]]. 

                Onto code! First step is to define a model to use its functions.

                model = LinearRegression()

                Training the model : 

                model.fit(data, labels)  # note : certain models will have certain keywords required. Call model.information to see that

                Evaluating model (you want a higher number here): 

                model.evaluate(data, labels) #data must be 2D, labels must be 1D
                ex. data = [[1, 1]]; labels = [1]
                ex. data = [[1, 1], [2, 2], [3, 3]], labels = [1, 2, 3]

                Predict : 

                model.predict(data) #data must be 2D, even if just one sample (ex. model.predict([[1, 2]])!

                © Anish Lakkapragada 2020   
        """

    def reset_params(self):
        '''when model predictions aren't good you can always do model.reset_params() and retrain. Always train before resetting parameters.'''
        self.weights = np.random.randn(self.num_features, 1)
        self.bias = np.random.uniform()

    def fit(self, x_train, y_train, accuracy_desired=0.95, learning_rate=0.01, max_iters=10000, show_acc=True):
        """
        :param x_train: input (has to be 2D) ex. [[1, 1], [2, 2]]
        :param y_train: labels (has to be 1D) ex. [0, 1] -> (has to start from zero)
        :param accuracy_desired: Accuracy threshold dictating that training stops at that percentage.
        Enables user to allow some bias in model to prevent overfitting.
        :param learning_rate: How fast neural network learns, weights = weights - learning_rate * gradients
        :param max_iters: Max iterations (or epochs) of the model to train
        :param show_acc : whether user would like to see the accuracy in training
        :return:
        """

        x_train, y_train = _preprocess_data(x_train, y_train)

        def param_init(x_train):
            '''initialize weights and biases'''
            num_features = len(x_train[0])  # number of features
            weights = np.random.randn(num_features, 1)
            bias = np.random.uniform()
            return weights, bias

        weights, bias = param_init(x_train)
        self.num_features = len(x_train[0])

        m = len(y_train)  # useful for derivatives in training

        iterations = tqdm(range(max_iters))
        for iteration in iterations:
            """"
            Training model. Stops when the accuracy_desired is met or too many iterations. 
            Specifications about the model : 
            ->> uses MSE loss
            ->> uses gradient descent

            In forward-propagation : 
            ->> y_hat (predictions) = weights * inputs + bias 
            ->> one_liner : y_hat = np.dot(x_train, weights) + bias 

            In gradient descent : 
            ->> Uses MSE (mean-squared-error) derivative of (yH - y) / m 
            ->> weights gradients in the inputs transpose (dot) derivative of MSE loss
            ->> bias gradients are just the sum of the errors

            Evaluation : 
            ->> Measures accuracy by seeing the error_rmse (how much it is off from the label on average)
            and then doing 1 - (error/rmse / np.mean(np.abs(y_train)) to see whether error_rmse is a lot or little given 
            the scale of the data.

            """

            y_hat = np.dot(x_train, weights) + bias  # forward pass, y_hat = wx + b

            # gradient descent
            dLdYh = (y_hat - y_train) / m  # MSE derivative
            weights -= learning_rate * np.dot(x_train.T, dLdYh)  # multiply by x_train.T as ∂Yh/∂W is just x_train
            bias -= learning_rate * sum(dLdYh)

            error_rmse = np.sqrt(np.sum((y_hat - y_train) ** 2) / (
                    2 * m))  # RMSE - how far on average are my predictions from their targets?

            accuracy_perc = 1 - (error_rmse / np.mean(np.abs(y_train)))

            if show_acc:
                iterations.set_description("accuracy : " + str(round(accuracy_perc * 100, 2)) + "% ")

            if accuracy_perc >= accuracy_desired:
                iterations.close()
                print("Accuracy threshold met!")
                break

            self.weights = weights  # updated every single iteration so you can manually stop training and not lose training progress
            self.bias = bias

    def predict(self, prediction_data):
        """
        :param prediction_data: points to be predicted on. Has to be stored in 2D array, even if just one data point. Ex. : [[1, 1]] or [[1, 1], [2, 2], [3, 3]]
        :return: flattened numpy array of your data going through the forward pass
        """

        prediction_data = np.array(prediction_data)
        if len(prediction_data.shape) < 2:
            prediction_data = np.array(
                [np.array([x_i]) for x_i in prediction_data])  # simple preprocessing to make it 2-Dimensional

        return (np.dot(prediction_data, self.weights) + self.bias).flatten()  # go through the forward pass for this
        # prediction_data

    def evaluate(self, x_test, y_test):
        """
        :param x_test: data to be evaluated on
        :param y_test: labels
        :return: score

        Evaluation done same as in training, calculate how far off from target on average (error_rmse), and how much that is compared to scale of data (np.mean(np.abs(y_test))
        """

        x_test, y_test = _preprocess_data(x_test, y_test)

        y_pred = []  # y_pred stores predictions

        for data in x_test:
            # forward pass for all data
            y_pred.append(np.dot(data, self.weights) + self.bias)

        y_pred = np.array(y_pred).flatten()
        y_test = np.array(
            y_test).flatten()  # make sure y_pred & y_test are same shape so y_pred - y_test works. Use the .flatten() method for this.
        m = len(y_pred)  # use for averaging evaluation
        error_rmse = np.sqrt(
            np.sum((y_pred - y_test) ** 2) / (2 * m))  # how much am are predictions off from targets on average?
        return 1 - (error_rmse / np.mean(np.abs(y_test)))  # how does that compare to the scale of the data

    def visualize_evaluation(self, y_pred, y_test):
        """
        :param y_pred: predictions given by model
        :param y_test: actual labels

        visualize data using matplotlib.pyplot ->> (only for 2D data)
        """
        import matplotlib.pyplot as plt
        plt.cla()
        plt.plot([_ for _ in range(len(y_pred))], y_pred, color="blue",
                 label="predictions/y_pred")  # plot all predictions in blue
        plt.plot([_ for _ in range(len(y_test))], y_test, color="green",
                 label="labels/y_test")  # plot all labels in green
        plt.legend()
        plt.show()


def sigmoid(x):
    '''sigmoid/logistic function in Logistic Regression.'''
    return 1 / (1 + np.exp(-x))


class LogisticRegression():
    def __init__(self):
        self.information = '''

                Logistic Regression, contrary to its name, is actually a classification algorithm. This 
            means instead of trying to predict numbers, it will predict whether something is a dog or a cat for instance. 
            This algorithm still tries to make a line, just of a different shape. The use of sigmoid (1/ (1 + e^-x)) 
            function over all inputs helps create that shape optimal for binary classification. Logistic Regression can 
            classify data into 2 (binary) categories. No changes from the standard linear regression module in calls. For 
            classification of ≥ 2 classes, softmax regression is the way to go! 

            © Anish Lakkapragada 2020
        '''

    def reset_params(self):
        '''when model predictions aren't good you can always do model.reset_params() and retrain. Always train before resetting parameters.'''
        self.weights = np.random.randn(self.num_features, 1)
        self.bias = np.random.uniform()

    def fit(self, x_train, y_train, accuracy_desired=0.95, learning_rate=0.01, max_iters=10000, show_acc=True):
        """
        :param x_train: input (has to be 2D) ex. [[1, 1], [2, 2]]
        :param y_train: labels (has to be 1D) ex. [0, 1] -> (has to start from zero)
        :param accuracy_desired: Accuracy threshold dictating that training stops at that percentage.
        Enables user to allow some bias in model to prevent overfitting.
        :param learning_rate: How fast neural network learns, weights = weights - learning_rate * gradients
        :param max_iters: Max iterations (or epochs) of the model to train
        :param show_acc : whether user would like to see the accuracy in training
        :return:
        """

        x_train, y_train = _preprocess_data(x_train, y_train)

        def param_init(x_train):
            '''initialize weights and biases'''
            num_features = len(x_train[0])  # number of features
            weights = np.random.randn(num_features, 1)
            bias = np.random.uniform()
            return weights, bias

        weights, bias = param_init(x_train)
        self.num_features = len(x_train[0])
        m = len(y_train)
        iterations = tqdm(range(max_iters))
        for iteration in iterations:
            """"
            Training model. Stops when the accuracy_desired is met or too many iterations. 
            Specifications about the model : 
            ->> uses log loss (a.k.a binary cross entropy)  = -1/m * ∑ y(i)log(yH(i)) + (1-y(i))log(1-yH(i))
            ->> derivative of loss with respect to Z, where yH = sigmoid(Z) and Z = wx + b, will be 1/m * yH - y due to use of log loss
            ->> uses gradient descent

            In forward-propagation : 
            ->> z = weights * inputs + bias (note : z never actually defined just 1 line)
            ->> y_hat (predictions) = sigmoid(z)
            ->> one_liner : y_hat = sigmoid(np.dot(x_train, weights) + bias)

            In gradient descent : 
            ->> Same derivative as linear regression due to using log loss (instead of MSE)
            ->> weights gradients in the inputs transpose (dot) derivative of log loss wrt. z
            ->> bias gradients are just the sum of the dLdZ

            Evaluation : 
            ->> Measures accuracy very simple, just what percent of data is predicted in the correct class? Stops
            when accuracy_desired is met.

            """
            y_hat = sigmoid(np.dot(x_train, weights) + bias)  # forward pass, y_hat = sigmoid(wx + b)

            # gradient descent
            y_hat, y_train = y_hat.reshape(m, 1), y_train.reshape(m, 1)
            dLdZ = (y_hat - y_train) / m  # Log Loss derivative
            weights -= learning_rate * np.dot(x_train.T, dLdZ)
            bias -= learning_rate * sum(dLdZ)

            num_correct = sum([1 if pred == label else 0 for pred, label in
                               zip(np.round_(y_hat), y_train)])  # what percent are labeled correctly - super simple!

            accuracy_perc = num_correct / m

            if show_acc:
                iterations.set_description("accuracy : " + str(round(accuracy_perc * 100, 2)) + "% ")

            if accuracy_perc >= accuracy_desired:
                iterations.close()
                print("Accuracy threshold met!")
                break

            self.weights = weights
            self.bias = bias

    def predict(self, prediction_data):
        """
        :param prediction_data: points to be predicted on. Has to be stored in 2D array, even if just one data point. Ex. : [[1, 1]] or [[1, 1], [2, 2], [3, 3]]
        :return: flattened numpy array of your data going through the forward pass (that's rounded as it's either 0 or 1)
        """
        prediction_data = np.array(prediction_data)
        if len(prediction_data.shape) < 2:
            prediction_data = np.array([np.array([x_i]) for x_i in prediction_data])  # make it 2D

        return np.round_(sigmoid(np.dot(prediction_data, self.weights) + self.bias)).flatten()

    def evaluate(self, x_test, y_test):
        """
        :param x_test: data to be evaluated on
        :param y_test: labels
        :return: score

        Evaluation, just like in training, is the percent of data that is predicted to the correct class.
        """
        x_test, y_test = _preprocess_data(x_test, y_test)

        y_pred = []  # stores predictions

        for data in zip(x_test):
            y_pred.append(sigmoid(np.dot(data, self.weights) + self.bias))

        y_pred = np.array(y_pred).flatten()
        y_test = np.array(y_test).flatten()  # make sure same shape
        num_correct = sum([1 if pred == label else 0 for pred, label in
                           zip(np.round_(y_pred), y_test)])  # what percent properly predicted?
        return num_correct * 100 / len(y_test)

    def visualize_evaluation(self, y_pred, y_test):
        """
        :param y_pred: predictions given by model
        :param y_test: actual labels

        visualize data using matplotlib.pyplot ->> (only for 2D data)
        """
        import matplotlib.pyplot as plt
        plt.cla()
        y_pred, y_test = y_pred.flatten(), y_test.flatten()
        plt.scatter([_ for _ in range(len(y_pred))], y_pred, color="blue", label="predictions/y_pred")
        plt.scatter([_ for _ in range(len(y_test))], y_test, color="green", label="labels/y_test")
        plt.legend()
        plt.show()


def softmax(scores):
    '''
    Used for Softmax Regression in the forward pass.

    :param scores: pre-softmax outputs for softmax regression
    :return: return each element's exponential divided by some of all element's exponential
    '''
    return np.exp(scores) / np.sum(np.exp(scores))


class SoftmaxRegression():
    def __init__(self, **kwargs):
        self.information = '''

                    Softmax Regression is a classification algorithm for when you're classes are >= 2 (not binary). This 
                makes it a versatile for datasets like Iris where there are many classes. Softmax Regression builds 
                off of Logistic Regression (binary classifier) so be familiar with that prior using this algorithm. 
                However, it is worth noting that Softmax Regression performs the same as Logistic Regression when 
                there are just 2 classes (binary.) In the fit() method of this class make sure to have the 
                "num_classes" keyword , for instance : model.fit(data, labels, num_classes = ?) This is needed for 
                the algorithm to learn. 

                © Anish Lakkapragada 2020 

        '''

    def reset_params(self):
        '''when model predictions aren't good you can always do model.reset_params() and retrain. Always train before resetting parameters.'''
        self.weights = np.random.randn(self.num_features, self.num_classes)
        self.bias = np.random.uniform()

    def fit(self, x_train, y_train, num_classes, accuracy_desired=0.95, learning_rate=0.01, max_iters=10000,
            show_acc=True):
        """
        :param x_train: input (has to be 2D) ex. [[1, 1], [2, 2]]
        :param y_train: labels (has to be 1D) ex. [0, 1] -> (has to start from zero)
        :param accuracy_desired: Accuracy threshold dictating that training stops at that percentage.
        Enables user to allow some bias in model to prevent overfitting.
        :param learning_rate: How fast neural network learns, weights = weights - learning_rate * gradients
        :param max_iters: Max iterations (or epochs) of the model to train
        :param show_acc : whether user would like to see the accuracy in training
        :return:
        """

        x_train, _ = _preprocess_data(x_train,
                                      y_train)  # the other labels don't matter because y_train has to be one-hot-encoded
        y_train = one_hot(y_train, num_classes=num_classes)  # one_hot_encode the labels
        x_train, y_train = np.array(x_train), np.array(y_train)  # convert to numpy arrays

        def param_init(x_train):
            num_features = len(x_train[0])
            weights = np.random.randn(num_features, num_classes)
            bias = np.random.randn(1, num_classes)
            return weights, bias

        weights, bias = param_init(x_train)
        self.num_features = len(x_train[0])
        self.num_classes = num_classes  # important for parameter intializations
        m = len(y_train)

        iterations = tqdm(range(max_iters))
        for iteration in iterations:
            """
            Training model. Stops when the accuracy_desired is met or too many iterations. 
            Specifications about the model : 
            ->> uses categorical cross entropy loss (-1/m * ∑y * ln(y_hat))
            ->> keep in mind that you do softmax for all scores in y_hat, so not a one-liner
            ->> bias is now the number of classes, so more verbose calculations there


            In forward-propagation : 
            ->> z = weights * inputs + bias (note : z = np.dot(x_train, weights) + bias)
            ->> y_hat (predictions) = [softmax(z_i) for z_i in z]
            ->> first two lines of forward pass

            In gradient descent : 
            ->> Same derivative as logistic regression due to using cross entropy loss (same as binary cross entropy derivative)
            ->> weights gradients in the inputs transpose (dot) derivative of crossentropy loss wrt. z
            ->> bias gradients are just the sum of the dLdZ

            Evaluation : 
            ->> Measures accuracy very simple, just what percent of data is predicted in the correct class? Stops
            when accuracy_desired is met.  
            """

            z = np.dot(x_train, weights) + bias  # forward pass start
            y_hat = np.array([softmax(z_i) for z_i in z])  # softmax for each output

            # gradient descent
            dLdZ = (y_hat - y_train) / m  # crossentropy loss derivative
            weights -= learning_rate * np.dot(x_train.T, dLdZ)
            for error in dLdZ: bias -= learning_rate * error  # change bias -> dLdZ is a matrix now due to one_hot_labels
            num_correct = sum([1 if np.argmax(pred) == np.argmax(label) else 0 for pred, label in
                               zip(np.round_(y_hat), y_train)])  # what percent are labeled correctly - super simple!

            accuracy_perc = num_correct / m
            if show_acc:
                iterations.set_description("accuracy : " + str(round(accuracy_perc * 100, 2)) + "% ")

            if accuracy_perc >= accuracy_desired:
                iterations.close()
                print("Accuracy threshold met!")
                break

            self.weights = weights
            self.bias = bias

    def predict(self, prediction_data):
        """
        :param prediction_data: points to be predicted on. Has to be stored in 2D array, even if just one data point. Ex. : [[1, 1]] or [[1, 1], [2, 2], [3, 3]]
        :return: flattened numpy array of your data going through the forward pass (that's rounded as it's either 0 or 1)
        """

        prediction_data = np.array(prediction_data)
        if len(prediction_data.shape) < 2:
            prediction_data = np.array([np.array([x_i]) for x_i in prediction_data])  # make it 2D

        Z = np.dot(prediction_data, self.weights) + self.bias
        y_hat = np.array([softmax(z) for z in Z])
        return np.array([np.argmax(output) for output in y_hat])  # go through each output and give the index of where
        # the probability is highest for that output
        # ex. [[0.2, 0.3, 0.5], [0.9, 0.06, 0.04]] will become [2, 0]

    def evaluate(self, x_test, y_test):
        """
        :param x_test: data to be evaluated on
        :param y_test: labels
        :return: score

        Evaluation, just like in training, is the percent of data that is predicted to the correct class.
        """
        x_test, _ = _preprocess_data(x_test, y_test)
        y_test = one_hot(y_test, self.num_classes)

        Z = np.dot(x_test, self.weights) + self.bias
        y_pred = np.array([softmax(z) for z in Z])
        y_pred = np.array(y_pred)
        num_correct = sum(
            [1 if np.argmax(pred) == np.argmax(label) else 0 for pred, label in zip(np.round_(y_pred), y_test)])
        return num_correct * 100 / len(y_test)  # basic evaluation

    def visualize_evaluation(self, y_pred, y_test):
        """
        :param y_pred: predictions given by model
        :param y_test: actual labels

        visualize data using matplotlib.pyplot ->> (only for 2D data)
        """
        import matplotlib.pyplot as plt
        plt.cla()
        y_pred, y_test = y_pred.flatten(), y_test.flatten()
        plt.scatter([_ for _ in range(len(y_pred))], y_pred, color="blue", label="predictions/y_pred")
        plt.scatter([_ for _ in range(len(y_test))], y_test, color="green", label="labels/y_test")
        plt.legend()
        plt.show()


def _poly_transform(data):
    '''take data and transform it like [2, 3, 4] - > [2, 9, 64]'''
    new_data = []
    for observation in data:
        new_observation = []
        for feature in range(len(observation)): new_observation.append(math.pow(observation[feature], (feature + 1)))
        new_data.append(new_observation)
    return np.array(new_data)


class PolynomialRegression():
    '''
    Polynomial Regression here works by first :
    1. taking data in
    2. transforming it into new data, where every element in the data ^ (index_in_observation + 1).
    For example : [[1, 2, 3], [2, 3, 4]] -> [[1, 4, 27], [2, 9, 64]]
    '''

    def __init__(self):
        self.information = """

            Polynomial Regression is an extension of Linear Regression. Just like linear regression 
            it predicts numbers, not categories. The only difference is that each observation/input in your data has each 
            of its elements go to the power of its num_feature in the data. If that doesn't make any sense that's okay. 
            Here's an example. 

            [2, 3, 4] -> where 2 is the 1th feature, 3 is the 2nd feature, 4 is the 3rd feature. 
            Therefore transforming the data though function t(x), gives this : t([2, 3, 4]) = [2, 9, 64]
            That's because 2^1 = 2, 3^2 = 9 , 4^3 = 64.

            These transformed inputs are then learnt by the Linear Regression Algorithm. 
        """
        self.inner_linear_model = None  # this inner_linear_model is the Linear Regression model used to predict

    def reset_params(self):
        self.inner_linear_model.reset_params()  # calls the LinearRegression.reset_params() method

    def fit(self, x_train, y_train, accuracy_desired=0.95, learning_rate=0.01, max_iters=10000, show_acc=True):
        """
        :param x_train: input (has to be 2D) ex. [[1, 1], [2, 2]]
        :param y_train: labels (has to be 1D) ex. [0, 1] -> (has to start from zero)
        :param accuracy_desired: Accuracy threshold dictating that training stops at that percentage.
        Enables user to allow some bias in model to prevent overfitting.
        :param learning_rate: How fast neural network learns, weights = weights - learning_rate * gradients in gradient descent
        :param max_iters: Max iterations (or epochs) of the model to train
        :param show_acc : whether user would like to see the accuracy in training
        :return:
        """

        x_train, y_train = _preprocess_data(x_train, y_train)
        x_train = _poly_transform(x_train)  # transform data

        self.inner_linear_model = LinearRegression()  # build the linear regression model
        self.inner_linear_model.fit(x_train, y_train, accuracy_desired=accuracy_desired, learning_rate=learning_rate,
                                    max_iters=max_iters, show_acc=show_acc)  # fit it (using all given parameters)

    def predict(self, prediction_data):
        """
        :param prediction_data: points to be predicted on. Has to be stored in 2D array, even if just one data point. Ex. : [[1, 1]] or [[1, 1], [2, 2], [3, 3]]
        :return: flattened numpy array of your data going through the forward pass (that's rounded as it's either 0 or 1)
        """
        prediction_data = _poly_transform(prediction_data)
        return self.inner_linear_model.predict(prediction_data)  # just use the prediction method

    def evaluate(self, x_test, y_test):
        """
        :param x_test: data to be evaluated on
        :param y_test: labels
        :return: score

        Evaluation using the same method as Linear Regression.
        """
        x_test = _poly_transform(x_test)
        return self.inner_linear_model.evaluate(x_test, y_test)

    def visualize_evaluation(self, y_pred, y_test):
        """
        :param y_pred: predictions given by model
        :param y_test: actual labels

        visualize data using matplotlib.pyplot ->> (only for 2D data)
        """
        import matplotlib.pyplot as plt
        plt.cla()
        plt.plot([_ for _ in range(len(y_pred))], y_pred, color="blue", label="predictions/y_pred")
        plt.plot([_ for _ in range(len(y_test))], y_test, color="green", label="labels/y_test")
        plt.legend()
        plt.show()


def reLU(X, leaking=0):
    """
    :param x: Input
    :param leaking: Leaking value, default 0 for vanilla reLU activation
    :return:
    """
    return np.array([x_i if x_i >= 0 else x_i * leaking for x_i in X])


def reLU_deriv(y_hat, leaking=0):
    """
    :param y_hat:
    :return: reLU derivative of each element in y_hat
    """
    return np.array([[1] if pred > 0 else [leaking] for pred in y_hat])


class ReLURegression:
    def __init__(self):
        self.information = "dwadwa"

    def reset_params(self):
        '''when model predictions aren't good you can always do model.reset_params() and retrain. Always train before resetting parameters.'''
        self.weights = np.random.randn(self.num_features, 1)
        self.bias = np.random.uniform()

    def fit(self, x_train, y_train, leaking=0, accuracy_desired=0.95, learning_rate=0.01, max_iters=10000,
            show_acc=True):
        """
        :param x_train: input (has to be 2D) ex. [[1, 1], [2, 2]]
        :param y_train: labels (has to be 1D) ex. [0, 1] -> (has to start from zero)
        :param accuracy_desired: Accuracy threshold dictating that training stops at that percentage.
        Enables user to allow some bias in model to prevent overfitting.
        :param learning_rate: How fast neural network learns, weights = weights - learning_rate * gradients
        :param max_iters: Max iterations (or epochs) of the model to train
        :param show_acc : whether user would like to see the accuracy in training
        :return:
        """

        x_train, y_train = _preprocess_data(x_train, y_train)  # first preprocess data
        self.leaking = leaking

        def param_init(x_train):
            num_features = len(x_train[0])
            weights = np.random.randn(num_features, 1)
            bias = np.random.uniform()
            return weights, bias

        weights, bias = param_init(x_train)
        self.num_features = len(x_train[0])
        m = len(y_train)
        iterations = tqdm(range(max_iters))
        for iteration in iterations:
            """"
            Training model. Stops when the accuracy_desired is met or too many iterations. 
            Specifications about the model : 
            ->> uses MSE loss, simple derivative of (yH - y)/m
            ->> uses (leaking) relu activation function, which is x if x >= 0 or leaking_param * x if x < 0 
            ->> uses gradient descent

            In forward-propagation : 
            ->> Z = wx + b
            ->> y_hat = (leaking) reLU(Z)  (NOTE : Z never defined)
            ->> one_liner = reLU(np.dot(x_train, weights) + bias)

            In gradient descent : 
            ->> Same derivative as linear regression for ∂L/∂Yh which is (yH - y)/,
            ->> However, that vector needs to go through the reLU derivative (which is if yH > 0 : 1,  else : leaking)
            ->> multiply the two together to get dLdZ

            Evaluation : 
            ->> Measures accuracy same as linear regression. Check docs above.
            """

            y_hat = reLU(np.dot(x_train, weights) + bias, leaking=leaking)  # forward pass, y_hat = relu(Z) | Z = wx + b

            # gradient descent
            y_hat, y_train = y_hat.reshape(m, 1), y_train.reshape(m, 1)
            dLdYh = (y_hat - y_train) / m
            dYhdZ = reLU_deriv(y_hat, leaking=leaking)
            dLdZ = dLdYh * dYhdZ  # chain rule!
            weights -= learning_rate * np.dot(x_train.T, dLdZ)
            bias -= learning_rate * np.sum(dLdZ)

            error_rmse = np.sqrt(np.sum((y_hat - y_train) ** 2) / (
                    2 * m))  # RMSE - how far on average are my predictions from their targets?

            accuracy_perc = 1 - (error_rmse / np.mean(np.abs(y_train)))

            if show_acc:
                iterations.set_description("accuracy : " + str(round(accuracy_perc * 100, 2)) + "% ")

            if accuracy_perc >= accuracy_desired:
                iterations.close()
                print("Accuracy threshold met!")
                break

            self.weights = weights  # updated every single iteration so you can manually stop training and not lose training progress
            self.bias = bias

    def predict(self, prediction_data):
        """
        :param prediction_data: points to be predicted on. Has to be stored in 2D array, even if just one data point. Ex. : [[1, 1]] or [[1, 1], [2, 2], [3, 3]]
        :return: flattened numpy array of your data going through the forward pass
        """

        prediction_data = np.array(prediction_data)
        if len(prediction_data.shape) < 2:
            prediction_data = np.array(
                [np.array([x_i]) for x_i in prediction_data])  # simple preprocessing to make it 2-Dimensional

        return reLU(np.dot(prediction_data, self.weights) + self.bias,
                    leaking=self.leaking).flatten()  # go through the forward pass for this
        # prediction_data

    def evaluate(self, x_test, y_test):
        """
        :param x_test: data to be evaluated on
        :param y_test: labels
        :return: score

        Evaluation done same as in training, calculate how far off from target on average (error_rmse), and how much that is compared to scale of data (np.mean(np.abs(y_test))
        """

        x_test, y_test = _preprocess_data(x_test, y_test)

        y_pred = []  # y_pred stores predictions

        for data in x_test:
            # forward pass for all data
            y_pred.append(reLU(np.dot(data, self.weights) + self.bias, leaking=self.leaking))

        y_pred = np.array(y_pred).flatten()
        y_test = np.array(
            y_test).flatten()  # make sure y_pred & y_test are same shape so y_pred - y_test works. Use the .flatten() method for this.
        m = len(y_pred)  # use for averaging evaluation
        error_rmse = np.sqrt(
            np.sum((y_pred - y_test) ** 2) / (2 * m))  # how much am are predictions off from targets on average?
        return 1 - (error_rmse / np.mean(np.abs(y_test)))  # how does that compare to the scale of the data

    def visualize_evaluation(self, y_pred, y_test):
        """
        :param y_pred: predictions given by model
        :param y_test: actual labels

        visualize data using matplotlib.pyplot ->> (only for 2D data)
        """
        import matplotlib.pyplot as plt
        plt.cla()
        plt.plot([_ for _ in range(len(y_pred))], y_pred, color="blue",
                 label="predictions/y_pred")  # plot all predictions in blue
        plt.plot([_ for _ in range(len(y_test))], y_test, color="green",
                 label="labels/y_test")  # plot all labels in green
        plt.legend()
        plt.show()

log_reg = LogisticRegression()
log_reg.fit(x_train, y_train)
print(time.time() - start_time)
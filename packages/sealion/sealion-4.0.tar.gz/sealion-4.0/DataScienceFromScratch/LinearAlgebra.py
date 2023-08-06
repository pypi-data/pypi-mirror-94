from typing import List
from typing import Tuple
from typing import Callable
import math

Vector = List[float]  # Vector represented as list containing floats


def add(v: Vector, w: Vector) -> Vector:
    '''add vectors element wise'''
    assert len(v) == len(w), "vectors must be same size"
    return [v_i + w_i for v_i, w_i in zip(v, w)]


assert add([1, 2, 3], [2, 3, 4]) == [3, 5, 7]


def subtract(v: Vector, w: Vector) -> Vector:
    '''subtracts element wise'''
    assert len(v) == len(w), "vectors must be same size"
    return [v_i - w_i for v_i, w_i in zip(v, w)]


def vector_sum(vectors: List[Vector]) -> Vector:
    '''returns the sum of the nth dimension of all of the vectors. [[1, 2, 3], [2, 3, 1]] will become [3, 5, 6] for example'''
    assert vectors, "no vectors provided"  # make sure vectors aren't empty
    num_elements = len(vectors[0])
    assert all(len(v) == num_elements for v in vectors), "vectors cannot be of different sizes"
    return [sum(vector[i] for vector in vectors)
            for i in range(
            num_elements)]  # basically for each dimension go through all vectors and sum up each vector at that dimension


def scalar_multiply(c: float, v: Vector) -> Vector:
    assert v, "vector is empty"
    return [c * v_i for v_i in v]


def vector_mean(vectors: List[Vector]) -> Vector:
    '''this gives the mean for every dimension in the vector'''
    n = len(vectors)  # number of vectors
    return scalar_multiply((1 / n), vector_sum(vectors))  # mean of every dimension


assert vector_mean([[1, 2, 1], [0, 1, 0]]) == [0.5, 1.5, 0.5]


def dot(v: Vector, w: Vector) -> float:
    '''sum of every element in v * every element in w corresponding'''
    assert len(v) == len(w), "vectors have to be same size"
    return sum([v_i * w_i for v_i, w_i in zip(v, w)])


assert dot([1, 2, 3], [4, 5, 6]) == 32


def sum_of_squares(v: Vector) -> float:
    '''return the sum of all of v_i ** 2'''
    # return sum([v_i ** 2 for v_i in v])
    return dot(v, v)  # pythonic


assert sum_of_squares([1, 2, 4]) == 21


def magnitude(v: Vector) -> float:
    '''sqrt of the sum of squares of everything in a vector'''
    return math.sqrt(sum_of_squares(v))


assert magnitude([2, 2]) == 2 * math.sqrt(2)


def squared_distance(v: Vector, w: Vector) -> float:
    '''computes (v_i - w_i) ** 2 ... (v_n + w_n) ** 2 for all'''
    return sum_of_squares(subtract(v, w))


def distance(v: Vector, w: Vector) -> float:
    '''Compute distance between v and w'''
    # return math.sqrt(squared_distance(v, w)) works! - still finds distance
    return magnitude(subtract(v, w))  # works as well by finding the length of the subtracted vector


Matrix = List[Vector]  # list of vector


def shape(A: Matrix) -> Tuple[int, int]:
    # returns (num_rows of A, num_cols of A)
    num_rows = len(A)
    num_cols = len(A[0])  # if A else 0
    return num_rows, num_cols


assert shape([[1, 2, 3], [2, 31, 3]]) == (2, 3)

def get_row(A: Matrix, i: int) -> Vector:
    '''returns that row of A'''
    return A[i]  # ith row


def get_column(A: Matrix, j: int) -> Vector:
    '''return everything at that column'''
    return [A_i[j] for A_i in A]  # jth dimension for A_i vector/row in A

def make_matrix(num_rows : int, num_cols : int, entry_fn = Callable[[int, int], float]) -> Matrix :
    '''returns a matrix with an entry_fn function that takes in i * j entry and gives value'''
    return [[entry_fn(i, j) #given i, create a list
             for j in range(num_cols)] #for every column
            for i in range(num_rows) #in every row
            ]

def identity_matrix(n : int) -> Matrix :
    '''returns an identity matrix. Has 1s on the diagonal and 0s elsewhere. Matrix is square'''
    return make_matrix(n, n, lambda i, j : 1 if i == j else 0) #lambda function takes in an entry and decides whether 1 or 0

friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2,3), (3, 4),
               (4, 5), (5, 6), (6, 8), (7, 8), (8, 9)]

friend_matrix = identity_matrix(10)

#first set everything to 0 below
for row in range(len(friend_matrix)) :
    for col in range(len(friend_matrix[row])) :
        friend_matrix[row][col] = 0

for friendship in friendships :
    friend1 = friendship[0]
    friend2 = friendship[1]
    friend_matrix[friend1][friend2] = 1
    friend_matrix[friend2][friend1] = 1


'''for friendship in friend_matrix :
    print(friendship)'''

friend_matrix = [[0, 1, 1, 0, 0, 0, 0, 0, 0, 0], #user 0, 1 on indices 1 & 2 as user 0 is friends with 1  & 2
                [1, 0, 1, 1, 0, 0, 0, 0, 0, 0], #user 1
                [1, 1, 0, 1, 0, 0, 0, 0, 0, 0], #user 2
                [0, 1, 1, 0, 1, 0, 0, 0, 0, 0], #...
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]] #user 9

#why this demonstration is useful

assert friend_matrix[0][2] == 1, "user 0 and user 2 are friends" #easy to access data
assert friend_matrix[0][8] == 0, "user 0 and user 8 aren't friends"

friends_of_five = [i for i, is_friend in enumerate(friend_matrix[5]) if is_friend] #all indices of where there is a friendship in user 5

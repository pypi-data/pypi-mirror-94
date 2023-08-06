'''statistics are used to quantify and highlight the most important things about data'''

import matplotlib.pyplot as plt
from collections import Counter

num_friends = [100, 49, 41, 40, 25, 21, 21, 19, 19, 18, 18, 16, 15, 15, 15, 15, 14, 14, 13, 13, 13, 13, 12, 12, 11, 10,
               10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
               9, 9, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6, 6,
               6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4,
               4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
               3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
               1, 1, 1, 1, 1, 1, 1, 1]
friend_counts = Counter(num_friends)
xs = range(max(num_friends) + 1)  # highest number in data - leave buffer of 1 so all data shows
ys = [friend_counts[x] for x in xs]  # default dict friend counts
plt.bar(xs, ys)
plt.axis([0, 101, 0, 25])
plt.title("Histogram of Friend Counts")
plt.xlabel("# for friends")
plt.ylabel("# of people")
plt.show()

# more simple statistics
num_points = len(num_friends)  # aka number of observations
largest_value = max(num_friends)  # highest number of friends
lowest_value = min(num_friends)  # lowest num of friends

sorted_values = sorted(num_friends)
smallest_value = sorted_values[0]
second_smallest_value, second_largest_value = sorted_values[1], sorted_values[-2]

# CENTRAL TENDENCIES
from typing import List, Tuple, Callable


def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs)


# underscores on functions show that users shouldn't use the function - > the function is just there for other usable of functions of the library
def _median_odd(xs: List[float]) -> float:
    '''halfway point, so if len(xs) = 3, then 3 // 2 or 1 is the index of the median'''
    return sorted(xs)[len(xs) // 2]


def _median_even(xs: List[float]) -> float:
    '''average of middle elements'''
    low_midpoint = len(xs) // 2
    xs = sorted(xs)
    return (xs[low_midpoint] + xs[low_midpoint - 1]) / 2


def median(xs: List[float]) -> float:
    '''not as sensitive to outliers as the mean'''
    return _median_odd(xs) if len(xs) % 2 != 0 else _median_even(xs)


assert median([1, 10, 5, 9, 2]) == 5
assert median([1, 9, 2, 10]) == (2 + 9) / 2


def quantile(xs: List[float], p: float) -> float:
    '''returns the p-th quantile of that data - like 99th quantile of NWEA'''
    p_index = int(p * len(xs))
    return sorted(xs)[p_index]


assert quantile(num_friends, 0.1) == 1
assert quantile(num_friends, 0.25) == 3
assert quantile(num_friends, 0.75) == 9
assert quantile(num_friends, 0.9) == 13


def mode(xs: List[float]) -> List[float]:
    '''return most common number(s) in data
        -> doesn't have to necessarily be one, ex. [1,1,2,2]
    '''
    counts = Counter(xs)
    max_count = max(counts.values())  # highest cases of appearance
    return [x_i for x_i, count in counts.items() if
            count == max_count]  # if the count is the highest count(s), then give the x_i for it


assert set(mode(num_friends)) == {1, 6}


# DISPERSION - how spread out is our data?

def data_range(xs: List[float]) -> float:
    '''range of the data'''
    return max(xs) - min(xs)


assert data_range(num_friends) == 99  # 100 - 1 = 99

# variance = ∑(x - x_mean)**2
from DataScienceFromScratch.LinearAlgebra import sum_of_squares
import math


def de_mean(xs: List[float]) -> List[float]:
    '''give each value in xs with its deviation from the mean'''
    x_bar = mean(xs)
    return [x_i - x_bar for x_i in xs]


def variance(xs: List[float]) -> float:
    deviations = de_mean(xs)
    n = len(xs)
    return sum_of_squares(deviations) / (n - 1)


assert 81.54 < variance(num_friends) < 81.55


def standard_deviation(xs: List[float]) -> float:
    '''highly affected, just like range, by outliers in the data'''
    return math.sqrt(variance(xs))

assert math.sqrt(81.54) < standard_deviation(num_friends) < math.sqrt(81.55)

def interquartile_range(xs : List[float]) -> float :
    '''not so much affected by outliers, calculates range from 75th to 25th quantile range'''
    return quantile(xs, 0.75) - quantile(xs, 0.25)

assert interquartile_range(num_friends) == 6

#CORRELATION

daily_minutes = [1,68.77,51.25,52.08,38.36,44.54,57.13,51.4,41.42,31.22,34.76,54.01,38.79,47.59,49.1,27.66,41.03,36.73,48.65,28.12,46.62,35.57,32.98,35,26.07,23.77,39.73,40.57,31.65,31.21,36.32,20.45,21.93,26.02,27.34,23.49,46.94,30.5,33.8,24.23,21.4,27.94,32.24,40.57,25.07,19.42,22.39,18.42,46.96,23.72,26.41,26.97,36.76,40.32,35.02,29.47,30.2,31,38.11,38.18,36.31,21.03,30.86,36.07,28.66,29.08,37.28,15.28,24.17,22.31,30.17,25.53,19.85,35.37,44.6,17.23,13.47,26.33,35.02,32.09,24.81,19.33,28.77,24.26,31.98,25.73,24.86,16.28,34.51,15.23,39.72,40.8,26.06,35.76,34.76,16.13,44.04,18.03,19.65,32.62,35.59,39.43,14.18,35.24,40.13,41.82,35.45,36.07,43.67,24.61,20.9,21.9,18.79,27.61,27.21,26.61,29.77,20.59,27.53,13.82,33.2,25,33.1,36.65,18.63,14.87,22.2,36.81,25.53,24.62,26.25,18.21,28.08,19.42,29.79,32.8,35.99,28.32,27.79,35.88,29.06,36.28,14.1,36.63,37.49,26.9,18.58,38.48,24.48,18.95,33.55,14.24,29.04,32.51,25.63,22.22,19,32.73,15.16,13.9,27.2,32.01,29.27,33,13.74,20.42,27.32,18.23,35.35,28.48,9.08,24.62,20.12,35.26,19.92,31.02,16.49,12.16,30.7,31.22,34.65,13.13,27.51,33.2,31.57,14.1,33.42,17.44,10.12,24.42,9.82,23.39,30.93,15.03,21.67,31.09,33.29,22.61,26.89,23.48,8.38,27.81,32.35,23.84]

from DataScienceFromScratch.LinearAlgebra import dot, scalar_multiply

#cov(x, y) = ∑(x - x_bar)(y-y_bar) / (n - 1)
def covariance(xs : List[float], ys : List[float]) -> float :
    '''tells us correlation by whether < or > 1 , but not actionable and easily interpreted like correlation
        ->> covariances closer to 0 mean no/litte correlation exists
        ->> covariance changes with the scale of the data, so no baseline on what is high or low to compare it to
    '''
    assert len(xs) == len(ys), "must be same size"
    n = len(xs)
    x_deviations, y_deviations = de_mean(xs), de_mean(ys)
    return dot(x_deviations, y_deviations) / (n - 1)

assert 22.42 < covariance(num_friends, daily_minutes) < 22.43
# covariance of daily_hours would be exactly covariance(num_friends, daily_minutes) / 60
daily_hours = scalar_multiply((1/60), daily_minutes)
assert 22.42/60 < covariance(num_friends, daily_hours) < 22.43/60

#correlation(x, y) = cov(x, y)  / std_dev(x) * std_dev(y)
def correlation(xs : List[float], ys : List[float]) -> float :
    '''measures how much xs & ys vary in tandem to their means
        -> -1 to 1, 0 none, 1 high, -1 high anticorrelation
        -> unlike covariance, scale of data doesn't change correlation (highly interpretable)
    '''
    stdev_x = standard_deviation(xs)
    stdev_y = standard_deviation(ys)
    if stdev_x > 0 and stdev_y > 0 :
        return covariance(xs, ys) / (stdev_x * stdev_y)
    else :
        return 0 #no variation in standard_dev, must be 0

assert 0.24 < correlation(num_friends, daily_minutes) < 0.25 and 0.24 < correlation(num_friends, daily_hours) < 0.25

#very weak data correlation, let's remove the outlier and see what happens

outlier = num_friends.index(100) #index of outlier

num_friends_good = [x
                    for i, x in enumerate(num_friends)
                    if i != outlier]

daily_minutes_good = [x for i, x in enumerate(daily_minutes)
                    if i != outlier]

daily_hours_good = scalar_multiply((1/60), daily_minutes_good) #or : [dm/60 for dm in daily_minutes_good]

assert 0.57 < correlation(num_friends_good, daily_minutes_good) < 0.58
assert 0.57 < correlation(num_friends_good, daily_hours_good) < 0.58

'''
Other Notes : 

- Simpson Paradox : 
    West Coast PhD 35 3.1
    East Coast PhD 70 3.2
    West Coast NPHD 66 10.9
    East Coast NPHD 33 13.4

    - there are way more PHDs on East Coast and those who have PhD and NPHD on East Coast have more average friends than on West Coast (kinda like 6 * 1.5 (higher observations, less rate) > 4 * 2 (less observations, higher rate)
    - but the averages for East vs. West Coast are still higher for West Coast due to more data of those who have NPHD 
    - the big thing that separates whether you are friendly or not is PHD
    - not all variables/features in data are equal

- more (correlation) caveats : 
    x = [-2, -1, 0, 1, 2]
    y = [2, 1, 0, 1, 2] 
    cov(x, y) = 0, no correlation here (just y = |x|)
    
    - visualization matters a lot because statistics make things easy to lie with numbers

- correlation doesn't mean causation
    -> for example does having more friends on the site mean more time on the site per day or more time on the site per day leads to more friends? 
    -> one way to figure this out is to do A/B testing with slight changes and see whether tweaking something makes a difference
        -> this could be showing or slowing down the growth of friends to see if more time on the site is what leads to more friends 
        -> promoting barriers and time limits and seeing what that does to your new friend count growth
'''






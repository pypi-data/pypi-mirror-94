"""
Working with 1D data is the easiest. Instead of finding mean, min, std, etc. it's more interesting to bucketize your data
and count how many points fall into each bucket and put that in a histogram.
"""

from typing import List, Dict
from collections import Counter
import math

import matplotlib.pyplot as plt


def bucketize(point: float, bucket_size: float) -> float:
    """Floor point to the next lower multiple of bucket_size."""
    return bucket_size * math.floor(point / bucket_size)


def make_histogram(points: List[float], bucket_size: float) -> Dict[float, int]:
    """Bucket the points and count how many points are in each bucket"""
    return Counter(bucketize(point, bucket_size) for point in points)  # for each point put it into a bucket and count
    # how many in each bucket


def plot_histogram(points: List[float], bucket_size: float, title: str = ""):
    histogram = make_histogram(points, bucket_size)
    plt.bar(histogram.keys(), histogram.values(), width=bucket_size)
    plt.title(title)


# considering 2 datasets below
import random
from DataScienceFromScratch.Probability import inverse_normal_cdf

random.seed(0)

# uniform between -100 and 100
uniform = [200 * random.random() - 100 for _ in range(10000)]

# normal distribution with mean 0, std 57
normal = [57 * inverse_normal_cdf(random.random())
          # what values give probablities from 0 - 1 in the standard normal CDF (mu = 0, std = 1)
          for _ in range(10000)]  # std * x + mu

plot_histogram(uniform, 10, title="Uniform Histogram")
plt.cla()  # clear
plot_histogram(normal, 10, title="Normal Histogram")
plt.cla()

"""
Having a dataset in 2-Dimensions : (understand each dimension individually)
"""


def random_normal() -> float:
    """Returns a value leading to a random decimal probability in a standard normal distribution"""
    return inverse_normal_cdf(random.random())


xs = [random_normal() for _ in range(1000)]
ys1 = [x + random_normal() / 2 for x in xs]
ys2 = [-x + random_normal() / 2 for x in xs]

# despite both being normally distributed, they have different shapes

plt.scatter(xs, ys1, marker=".", color="red", label="ys1")
plt.scatter(xs, ys2, marker=".", color="green", label="ys2")
plt.xlabel("xs")
plt.ylabel("ys")
plt.legend(loc=9)
plt.title("Very Different Joint Distributions")
plt.show()

# plt.cla()

# looking at correlation to find the difference
from DataScienceFromScratch.Statistics import correlation

print("XS & YS1 correlation : ", correlation(xs, ys1))
print("XS & YS2 correlation : ", correlation(xs, ys2))

# many more dimensions.
"""
If you have many more dims, you would like to know how all dims relate 
to one another. Taking a look at the correlation matrix is a way to see how the ith row 
and jth column.
"""

from DataScienceFromScratch.LinearAlgebra import Matrix, Vector, make_matrix, get_column, shape


def correlation_matrix(data: List[Vector]) -> Matrix:
    """Returns the len(data) * len(data) matrix whose of i-j entry is the correlation
    of the i and j dimensions"""

    def correlation_ij(i: int, j: int) -> float:
        return correlation(get_column(data, i), get_column(data, j))  # correlation between the ith

    return make_matrix(len(data), len(data), correlation_ij)


# making a scatterplot matrix

def create_data(rows: int, cols: int) -> Matrix:
    return [[random.random() for col in range(cols)]
            for row in range(rows)]


corr_data = create_data(4, 4)
_, num_cols = shape(corr_data)
fig, ax = plt.subplots(num_cols, num_cols)
for i in range(num_cols):
    for j in range(num_cols):

        # scatter column_j on x-axis vs. column-i on the y-axis
        if i != j:
            ax[i][j].scatter(corr_data[j], corr_data[i])

        # if they are equal (the diagonal), show the series name
        else:
            ax[i][j].annotate("series " + str(i), (0.5, 0.5),
                              xycoords="axes fraction",
                              ha="center", va="center")

        # hide axis labels except for the left and bottom charts
        if i < num_cols - 1: ax[i][j].xaxis.set_visible(False)
        if j > 0: ax[i][j].yaxis.set_visible(False)

# Fix the bottom-right and top-left axis labels, which are wrong because their charts have only text in them
ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
ax[0][0].set_ylim(ax[0][1].get_ylim())

plt.show()

# Named Tuples

# a common way of representing data is through dicts like :
import datetime

stock_price = {"closing_price": 102.06,
               "date": datetime.date(2021, 1, 1),
               "symbol": "New Year"}

# inefficient for storage, and accessing can go wrong, e.g : stoc_price['cosing_price'] = 102 (typo)

# you don't know what is stored where in a dictionary, e.g. what every key means

prices: Dict[datetime.date, float] = {}  # what if there are multiple different data types

# instead, use a named tuple - which is just a tuple but has named slots
from collections import namedtuple

StockPrice = namedtuple("StockPrice", ['Symbol', 'Date',
                                       'Closing_price'])  # name_of_tuple = namedtuple("name_of_tuple", [all_data_in_strings])
price = StockPrice('MSFT', datetime.date(2021, 1, 1), '106.03')

assert price.Symbol == "MSFT"
assert price.Closing_price == '106.03'  # easy access to anything here

# however, these named tuples are immutable.

# for typing annotations you can use NamedTuple
from typing import NamedTuple


class StockPrice(NamedTuple):
    Symbol: str
    Date: datetime.date
    Closing_price: float

    def is_new_year(self) -> bool:
        return self.Date == datetime.date(2021, 1, 1)


price = StockPrice("MSFT", datetime.date(2021, 1, 1), 200.0)

assert price.Symbol == "MSFT"
assert price.Closing_price == 200
assert price.is_new_year()

# dataclasses, added functions to NamedTuples
from dataclasses import dataclass


@dataclass
class StockPrice2:
    Symbol: str
    Date: datetime.date
    Closing_price: float

    def is_new_year(self) -> bool:
        return self.Date == datetime.date(2021, 1, 1)


price2 = StockPrice2("AAPL", datetime.date(2021, 1, 1), 2000)
assert price2.Symbol == "AAPL"
assert price2.Date == datetime.date(2021, 1, 1)
assert price2.is_new_year()

# we can modify a data class values
price2.Date = datetime.date(2021, 1, 2)
assert not price2.is_new_year()

# unfortunately, this doesn't give an error : price2.cosing_price = 200 (typo allowed)

# cleaning and munging data

from dateutil.parser import parse


def parse_row(row: List[str]) -> StockPrice:
    Symbol, Date, Closing_price = row
    return StockPrice(Symbol=Symbol,
                      Date=parse(Date).date(),  # turns "2020-1-1" -> datetime.date(2020, 1, 1)
                      Closing_price=float(Closing_price))


stock = parse_row(["MSFT", "2020-1-1", "200.54"])
print("This is the stock : ", stock)
assert stock.Symbol == "MSFT"
assert stock.Closing_price == 200.54
assert stock.Date == datetime.date(2020, 1, 1)

# if there's some bad data (e.g. a string in a numeric col or vice versa) - maybe you want to turn that to None and
# avoid the error(s) ?

from typing import Optional
import re


def try_parse_row(row: List[str]) -> Optional[StockPrice]:
    Symbol, Date_, Closing_price_ = row

    # Stock symbol should be all CAPS and only letters
    if not re.match(r"^[A-Z]+$", Symbol):
        return None

    try:
        Date = parse(Date_).date()
    except ValueError:
        return None

    try:
        Closing_price = float(Closing_price_)
    except ValueError:
        return None

    return StockPrice(Symbol, Date, Closing_price)


assert try_parse_row(["msft", '2021-1-1', '200']) is None
assert try_parse_row(["MSFT", '2019-2030-02', 2031]) is None
assert try_parse_row(["MSFT", "2020-31-12", "?"]) is None
assert try_parse_row(['TSLA', '2021-1-1', '200.56']) is not None
assert try_parse_row(["MSFT", "2020-1-1", "200.54"]) == stock

# now we can read and return only the good data

import csv

data: List[StockPrice] = []

with open("comma_delimited_stock_prices.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        maybe_stock = try_parse_row(row)  # may return None or all will be correct
        if not maybe_stock:
            print(f"skipping invalid row : {row}")
        else:
            data.append(maybe_stock)

print("This is the data : ", data)

# Manipulating Data

# easy way to find the highest closing price for AAPL stock

max_aapl_price = max(stock_price.Closing_price for stock_price in data if stock_price.Symbol == "AAPL")

# to find the highest closing price for each stock

from collections import defaultdict

max_prices: Dict[str, float] = defaultdict(lambda: float('-inf'))  # -inf if the price is invalid because anything else
# is greater than that and will take it's place

for sp in data:
    Symbol, Closing_price = sp.Symbol, sp.Closing_price
    if Closing_price > max_prices[Symbol]:
        max_prices[Symbol] = Closing_price

print("Max prices : ", max_prices)

#What is the smallest and biggest 1-day percent changes?

#collect the prices by symbol
prices : Dict[str, List[StockPrice]] = defaultdict(list)

for sp in data :
    prices[sp.Symbol].append(sp)

prices = {symbol : sorted(symbol_prices) for symbol, symbol_prices in prices.items()} #sorts in order, so if there are
# multiple same symbols next it gets sorted by date

print("These are prices : ", prices)

def pct_change(yesterday : StockPrice, today : StockPrice) -> float :
    return today.Closing_price / yesterday.Closing_price - 1 #gives the percent change

class DailyChange(NamedTuple) :
    Symbol : str
    Date : datetime.date
    pct_change : float

def day_over_day_changes(prices : List[StockPrice]) -> List[DailyChange] :
    return [DailyChange(Symbol = today.Symbol,
                        Date = today.Date,
                        pct_change = pct_change(yesterday, today)) #percent change
                    for yesterday, today in zip(prices, prices[1:])] #give a named tuple w/ type annotations of yesterday and today changes

all_changes = [change
               for symbol_prices in prices.values()
               for change in day_over_day_changes(symbol_prices)]

print("This is all_changes : ", all_changes)

#find the largest and smallest changes
max_change = max(all_changes, key = lambda change : change.pct_change) #take the named_tuple and find it's change
print("Single max_change : ", max_change)
assert max_change.Symbol == "FB"

min_change = min(all_changes, key = lambda all_change : all_change.pct_change)
print("Single min change : ", min_change)

changes_by_month : Dict[int, List[DailyChange]] = {month : [] for month in range(1, 13)}

for change in all_changes :
    '''take every Daily Change item and put it into the changes_by_month by its month'''
    changes_by_month[change.Date.month].append(change)

avg_daily_changes = {
    month : sum(change.pct_change for change in changes) / len(changes) if len(changes) else 0  #for each month give the average of its change (changes is a List[DailyChange] item)
    for month, changes in changes_by_month.items()
}

print("Best change : ", max(avg_daily_changes.values()))
#to find the best month
changes_to_month = {changes : month for month, changes in avg_daily_changes.items()}
print("Best month : ", changes_to_month[max(changes_to_month)]) #at the biggest change, what was the best month (looks like there was no change?)

#many techniques require rescaling and here's why :

from DataScienceFromScratch.LinearAlgebra import distance

#measuring distance of points
a_to_b = distance([63, 150], [67, 160])
a_to_c = distance([63, 150], [70, 171])
b_to_c = distance([67, 160], [70, 171])
print("Inches : ")
print(a_to_b)
print(a_to_c)
print(b_to_c)

#measuring distance, now with cm instead of inches
a_to_b = distance([160, 150], [170.2, 160])
a_to_c = distance([160, 150], [177.8, 171])
b_to_c = distance([170.2, 160], [177.8, 171])
print("Centimeters : ")
print(a_to_b)
print(a_to_c)
print(b_to_c)

"""
This a problem, because the units can change distances like that. We may not be able to always convert units, so instead
we can rescale so each dimension has a mean of 0 and an std of 1. This gets rid of the units, and everything is measured
in standard deviations from the mean (much more effective.)
"""

from typing import Tuple
from DataScienceFromScratch.LinearAlgebra import vector_mean
from DataScienceFromScratch.Statistics import standard_deviation

def scale(data : List[Vector]) -> Tuple[Vector, Vector] :
    """returns the mean and std for each position"""
    means = vector_mean(data)
    dims = len(data[0]) #no. of dimensions
    stdev = [standard_deviation(get_column(data, i)) for i in range(dims)] #std of each dimension
    return means, stdev

vectors = [[-3, -1, 1], [-1, 0, 1], [1, 1, 1]]
means, stdevs = scale(vectors)
assert means == [-1, 0, 1]
assert stdevs == [2, 1, 0]


def rescale(data : List[Vector]) -> List[Vector] :
    """Rescales so input data has mu 0 , std 1."""
    dim = len(data[0])
    means, stdevs = scale(data)

    #make a copy of each vector (don't edit previous one)
    rescaled = [v[:] for v in data]

    for v in rescaled :
        for i in range(dim) :
            if stdevs[i] > 0: #if there's no deviation, don't rescale
                v[i] = (v[i] - means[i])/stdevs[i]

    return rescaled


means, stdevs = scale(rescale(vectors))
assert means == [0, 0, 1] #no deviation on 3rd dim
assert stdevs == [1, 1, 0] #no deviation in 3rd dim

#you may have to use your judgemnet, because let's say you're looking at data in a range from 3.5 to 4, the variation could just be noise
# so why make it as important as other dimensions (hide the fact its noise to the machine)

#an aside : using tqdm
import tqdm

for i in tqdm.tqdm(range(100)) :
    _ = [random.random() for _ in range(100000)]

#setting the description bar while it is running
from typing import List

def primes_up_to(n : int) -> List[int] :
    primes = [2]
    with tqdm.trange(3, n) as t :
        for i in t :
            #i is prime if no smaller prime divides it
            i_is_prime = not any(i % p == 0 for p in primes)
            if i_is_prime :
                primes.append(i)
            t.set_description(f"{len(primes)} primes")
    return primes

primes_100 = primes_up_to(100)

#PCA w/o the SVD
"""
Find an axis that captures the most variance as possible.
"""

from DataScienceFromScratch.LinearAlgebra import subtract

def de_mean(data : List[Vector]) -> List[Vector] :
    """recenter data to get mean 0 in each dim"""
    mean = vector_mean(data)
    return [subtract(vector, mean) for vector in data]

from DataScienceFromScratch.LinearAlgebra import magnitude

def direction(w : Vector) -> Vector :
    '''direction is just a magnitude 1 vector, so rescale it here '''
    magnitude_w = magnitude(w)
    return [w_i / magnitude_w for w_i in w]

assert round(magnitude(direction([3, 4, 5]))) == 1

#due to direction, we can calculat ethe variance of data in the direction determined by nonzero w

from DataScienceFromScratch.LinearAlgebra import dot

def directional_variance(data : List[Vector], w : Vector) -> float :
    '''returns variance of x in the direction w'''
    w_dir = direction(w)
    return sum(dot(v, w_dir) ** 2 for v in data) #for v in data find how much v extends in the w direction ** 2

#todo - why no N-1

def directional_variance_gradient(data : List[Vector], w : Vector) -> Vector :
    """gradient of directional variance wrt w"""
    w_dir = direction(w)
    return [sum(2 * dot(v, w_dir) * v[i] for v in data) for i in range(len(w))] #for each dimension see which direction
    #maximizes the variance

from DataScienceFromScratch.GradientDescent import gradient_step

def first_principal_component(data : List[Vector],
                              n : int = 100,
                              step_size : float = 0.1) -> Vector :

    #start out with a random guess
    guess = [1.0 for _ in data[0]]

    with tqdm.trange(n) as t :
        for _ in t :
            dv = directional_variance(data, guess)
            gradient = directional_variance_gradient(data, guess)
            guess = gradient_step(guess, gradient, step_size)
            t.set_description(f" dv : {dv:.3f}")

    return direction(guess)

from DataScienceFromScratch.LinearAlgebra import scalar_multiply

def project(v : Vector, w : Vector) -> Vector :
    """return the projection of v onto w"""
    projection_length = dot(v, w)
    return scalar_multiply(projection_length, w)

from DataScienceFromScratch.LinearAlgebra import subtract

def remove_projection_from_vector(v : Vector, w : Vector) -> Vector :
    """projects  v onto w and subtracts the result from v"""
    return subtract(v, project(v, w))

def remove_projection(data : List[Vector], w : Vector) -> List[Vector] :
    return [remove_projection_from_vector(v, w) for v in data]

#this makes the dataset 1D, but for higher dimensional datasets :

def pca(data : List[Vector], num_components : int) -> List[Vector] :
    components : List[Vector] = []
    for _ in range(num_components) :
        component = first_principal_component(data)
        components.append(component)
        data = remove_projection(data, component)
    return components

#transform the data

def transform_vector(v : Vector, components : List[Vector]) -> Vector :
    return [dot(v, w) for w in components]

def transform(data : List[Vector], components : List[Vector]) -> List[Vector] :
    return [transform_vector(v, components) for v in data]

#do PCA on X


X = [
    [20.9666776351559,-13.1138080189357],
    [22.7719907680008,-19.8890894944696],
    [25.6687103160153,-11.9956004517219],
    [18.0019794950564,-18.1989191165133],
    [21.3967402102156,-10.8893126308196],
    [0.443696899177716,-19.7221132386308],
    [29.9198322142127,-14.0958668502427],
    [19.0805843080126,-13.7888747608312],
    [16.4685063521314,-11.2612927034291],
    [21.4597664701884,-12.4740034586705],
    [3.87655283720532,-17.575162461771],
    [34.5713920556787,-10.705185165378],
    [13.3732115747722,-16.7270274494424],
    [20.7281704141919,-8.81165591556553],
    [24.839851437942,-12.1240962157419],
    [20.3019544741252,-12.8725060780898],
    [21.9021426929599,-17.3225432396452],
    [23.2285885715486,-12.2676568419045],
    [28.5749111681851,-13.2616470619453],
    [29.2957424128701,-14.6299928678996],
    [15.2495527798625,-18.4649714274207],
    [26.5567257400476,-9.19794350561966],
    [30.1934232346361,-12.6272709845971],
    [36.8267446011057,-7.25409849336718],
    [32.157416823084,-10.4729534347553],
    [5.85964365291694,-22.6573731626132],
    [25.7426190674693,-14.8055803854566],
    [16.237602636139,-16.5920595763719],
    [14.7408608850568,-20.0537715298403],
    [6.85907008242544,-18.3965586884781],
    [26.5918329233128,-8.92664811750842],
    [-11.2216019958228,-27.0519081982856],
    [8.93593745011035,-20.8261235122575],
    [24.4481258671796,-18.0324012215159],
    [2.82048515404903,-22.4208457598703],
    [30.8803004755948,-11.455358009593],
    [15.4586738236098,-11.1242825084309],
    [28.5332537090494,-14.7898744423126],
    [40.4830293441052,-2.41946428697183],
    [15.7563759125684,-13.5771266003795],
    [19.3635588851727,-20.6224770470434],
    [13.4212840786467,-19.0238227375766],
    [7.77570680426702,-16.6385739839089],
    [21.4865983854408,-15.290799330002],
    [12.6392705930724,-23.6433305964301],
    [12.4746151388128,-17.9720169566614],
    [23.4572410437998,-14.602080545086],
    [13.6878189833565,-18.9687408182414],
    [15.4077465943441,-14.5352487124086],
    [20.3356581548895,-10.0883159703702],
    [20.7093833689359,-12.6939091236766],
    [11.1032293684441,-14.1383848928755],
    [17.5048321498308,-9.2338593361801],
    [16.3303688220188,-15.1054735529158],
    [26.6929062710726,-13.306030567991],
    [34.4985678099711,-9.86199941278607],
    [39.1374291499406,-10.5621430853401],
    [21.9088956482146,-9.95198845621849],
    [22.2367457578087,-17.2200123442707],
    [10.0032784145577,-19.3557700653426],
    [14.045833906665,-15.871937521131],
    [15.5640911917607,-18.3396956121887],
    [24.4771926581586,-14.8715313479137],
    [26.533415556629,-14.693883922494],
    [12.8722580202544,-21.2750596021509],
    [24.4768291376862,-15.9592080959207],
    [18.2230748567433,-14.6541444069985],
    [4.1902148367447,-20.6144032528762],
    [12.4332594022086,-16.6079789231489],
    [20.5483758651873,-18.8512560786321],
    [17.8180560451358,-12.5451990696752],
    [11.0071081078049,-20.3938092335862],
    [8.30560561422449,-22.9503944138682],
    [33.9857852657284,-4.8371294974382],
    [17.4376502239652,-14.5095976075022],
    [29.0379635148943,-14.8461553663227],
    [29.1344666599319,-7.70862921632672],
    [32.9730697624544,-15.5839178785654],
    [13.4211493998212,-20.150199857584],
    [11.380538260355,-12.8619410359766],
    [28.672631499186,-8.51866271785711],
    [16.4296061111902,-23.3326051279759],
    [25.7168371582585,-13.8899296143829],
    [13.3185154732595,-17.8959160024249],
    [3.60832478605376,-25.4023343597712],
    [39.5445949652652,-11.466377647931],
    [25.1693484426101,-12.2752652925707],
    [25.2884257196471,-7.06710309184533],
    [6.77665715793125,-22.3947299635571],
    [20.1844223778907,-16.0427471125407],
    [25.5506805272535,-9.33856532270204],
    [25.1495682602477,-7.17350567090738],
    [15.6978431006492,-17.5979197162642],
    [37.42780451491,-10.843637288504],
    [22.974620174842,-10.6171162611686],
    [34.6327117468934,-9.26182440487384],
    [34.7042513789061,-6.9630753351114],
    [15.6563953929008,-17.2196961218915],
    [25.2049825789225,-14.1592086208169]
] #all the data

components = pca(X, 1)
X_transform = transform(X, components)

plt.cla()
plt.scatter([x_i[0] for x_i in X], [x_i[1] for x_i in X])
plt.scatter([x_i for x_i in X_transform], [0 for x_i in X_transform])
plt.show()

#PCA's really useful, but a little less interpretable





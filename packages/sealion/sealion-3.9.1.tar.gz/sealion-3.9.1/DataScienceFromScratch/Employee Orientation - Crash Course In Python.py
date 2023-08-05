back_slash_skills = "back_slash" + \
     "skills" #split up words

import re
my_regex = re.compile("[0-9+]", re.I)

import random
def print_number(num) :
    print(random.randint(0, num))

def print_multiple_numbers(nums) :
    '''demonstrates Python first class functions of being able to call a function in another function'''
    for num in nums :
        print_number(num)

def double(x) :  return x * 2

def apply_to_one(f) :
    return f(1)

my_double = double #refers to function
x = apply_to_one(my_double)

another_double = lambda x : x * 2

#or

def another_double(x) :
    return x * 2

not_tab_string = r"\t"
len(not_tab_string)

print("NTS : " , not_tab_string)

multi_line_string = """
    This is the first line.
    This is the second line.
    This is the third line.
"""

first_name = "Anish"
last_name = "Lakkapragada"

full_name1 = first_name + " " + last_name #string.concat/add
full_name2 = "{0} {1}".format(first_name, last_name) #string.format
full_name3 = f"{first_name} {last_name}" #f-string

#exceptions
try :
    print(0/0)
except ZeroDivisionError :
    print("cannot divide by zero")

x = [_ for _ in range(10)]

nine = x[-1] #pythonic with -1

#slicing with stride

every_third = x[::3]
five_to_three = x[5:2:-1] #going backward by -1 index

#list concat
x = [1, 2, 3]
x.extend([4, 5, 6])

#OR

y = [4, 5, 6]
x += y
print(x)

#unpack a list
x, y = [1, 2]

#tuples
my_list = [1, 2]
my_tuple = (1, 2)
other_tuple = 3, 4
my_list[1] = 3 #edit the list

try :
    my_tuple[1] = 3
except TypeError :
    print("tuples are immutable")

#tuples are good for storing stuff
def sum_and_product(x, y) :
    return (x + y), (x * y) #stored in (add, mult) tuple

empty_dict = {}
empty_dict2 = dict() #not pythonic at all
grades = {"Anish" : 100, "Lakkapragada" : 101}

anish_grade = grades["Anish"]

lakka_in_grades = "Lakkapragada" in grades #is key in dict

#if you don't want an exception if a value isn't there :
item_if_there = grades.get("key to search ", 0) #0 is the default value given if "key to search " isn't there -> you can change it

tweet = {
    "user" : "joelgrus",
    "text" :  "Data Science is awesome",
    "retweet_count" : 100,
    "hashtags" : ["#data", "#science", "#datascience", "#awesome", "#yolo"]
}

tweet_keys = tweet.keys()
tweet_values = tweet.values()
tweet_items = tweet.items() #tuple of (key, value) for entry in tweet dict

print(tweet_keys, tweet_values, tweet_items)

#default dict module
from collections import defaultdict

word_counts = defaultdict(int) #naturally the (int) produces 0
doc = ["dwadwa", "dwadwa", "dwawww"]
for word in doc :
    word_counts[word] += 1

#default dicts can be useful for list and dicts

dd_list = defaultdict(list) #creates empty lists
dd_list[2].append(1)

dd_dict = defaultdict(dict) #creates empty dictionaries
dd_dict["Anish"]["last_name"] = "Lakkapragada"

dd_pair = defaultdict(lambda : [0, 0])
dd_pair[2][1] = 1 #now dd_pair = {2 : [0, 1]}

from collections import Counter

c = Counter([0,1 , 2, 0]) # {0 : 2, 1 : 1, 2 : 1}

word_counts = Counter(doc)

for word, count in word_counts.most_common(10) :
    print(word, count)

#set, defines a group/collection of DISTINCT elements

primes_below_10 = {2, 3, 5, 7}
s = set()
s.add(1) #{1}
s.add(2) #{2}
s.add(2) #{2}

#good to find the distinct items at any given point

parity = "even" if x % 2 == 0 else "odd"

for x in range(10) :
    if x == 3 :
        continue #go onto next loop
    if x == 5 :
        break #immediately stop the for loop

#something is false if there is nothing in it
false_list = []
if false_list :
    '''asking if the list is True or not'''
    print("TRUE")
else : print("FALSE")

#sorting in python

x = [4, 1, 2, 3]
y = sorted(x) #y = [1, 2, 3, 4]
x.sort() #x = [1, 2, 3, 4] now with .sort()

x = sorted([-4, 1, -2, 3], key = abs, reverse = True) #you can sort using a function with key so this is going to be [-4, 3, -2, 1]

#you can also sort tuples using the key param
sorted_tweet = sorted(
    tweet.items(),
    key = lambda stuff : len(stuff[0]),
    reverse = True
)

print("This is the sorted_tweet : ", sorted_tweet)

#list comprehension

even_numbers = [x for x in range(5) if x % 2 == 0] #[0, 2, 4]
squares = [x ** 2 for x in range(5)] # [0, 1, 4, 9, 16]
even_squares = [x ** 2 for x in even_numbers]
#or non-pythonic : even_squares = [x**2 for x in range(5) if x % 2 == 0]

zeros = [0 for _ in even_numbers] # underscore if useless

pairs = [(x,y)
         for x in range(10)
         for y in range(10)]

#or
pairs = []
for x in range(10) :
    for y in range(10) :
        pairs.append((x,y))

#assert statements
#returns AssertionError if incorect statement
assert 1 + 1 == 2
try :
    assert 1 + 1 == 3, "1 + 1 should be equal 2 but it didn't" #you get : AssertionError: 1 + 1 should be equal 2 but it didn't
except AssertionError :
    pass


def smallest_item(xs) :
    assert xs, "empty list won't have a min"
    return min(xs)

assert smallest_item([10, 20, 5, 40]) == 5
assert smallest_item([1, 0, -1, 2]) == -1

#Object Oriented Programming in Python

class CountingClicker :
    def __init__(self, count = 0 ):
        self.count = count
    def __repr__(self):
        return f"CountingClicker(count = {self.count})"
    def click(self, num_times = 1):
        self.count += num_times
    def read(self):
        return self.count
    def reset(self):
        self.count = 0

clicker = CountingClicker()
assert clicker.read() == 0
clicker.click()
clicker.click()
assert clicker.read() == 2
clicker.reset()
assert clicker.read() == 0

#inheritance of classes in python
class NoResetClicker(CountingClicker) :
    def reset(self):
        pass

clicker = NoResetClicker()
clicker.click(num_times = 100)
clicker.reset()
print(".read() : " , clicker.read())
assert clicker.read() == 100 , "not working"

#iterators and generators in python
def generate_range(n) :
    '''creates a generater object'''
    i = 0
    while i < n :
        yield i
        i += 1

for i in generate_range(10) :
    print(f"i : {i}")

def generate_natural_numbers() :
    n = 1
    while n < 5 :
        yield n
        n += 1

data = generate_natural_numbers()
evens = (x for x in data if x %2  == 0 )
odds = (x for x in data if x%2 != 0)
even_squares = (x ** 2 for x in evens)

#enumerate, pythonic function
names = ["Anish", "Kanchan", "Shobhan", "Ankit"]

for index, name in enumerate(names) :
    print(f"name {index} : {name}")

#randominess in python
import random
random.seed(10) #reproducibile results

four_uniform_randoms = [random.random() for _ in range(4)]

#random.randrange() randomly selects something
random.randrange(10) #selecting from [0, 1, ..., 9]
random.randrange(3,6) #selecting from 3 - 6 [3, 4, 5]

random.shuffle(names)
print("new names : " , names)

#sampling from list randomly
two_names = random.sample(names, 2) #(list, num_samples)

#regular expressions with re!

import re
re_examples = [
    not re.match("a", "cat") ,#re.match() checks whether a is the first in cat here
    re.search("a", "cat"), #true 'cat' has an 'a'
    not re.search("c", "dog"), #true, as there is no c in dog
    3 == len(re.split("[ab]", "carbs")), #removing the a & b in carbs leads to to crs, len("crs") == 3
    "R-D-" == re.sub("[0-9]", "-", "R2D2") #remove any numbers with a dash instead
]

assert all(re_examples) #make sure all of them are true

#zip & argument unpacking!

list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

alpha_to_nums = {char : index for char, index in zip(list1, list2)}
pairs = [pair for pair in zip(list1, list2)]
letters, numbers = zip(*pairs)

#the * does argument unpacking - see below with functions

def add(a, b) : return a + b
add(1,2)
try :
    add([1, 2])
except TypeError :
    print("add excepts two inputs")
add(*[1,2]) #unpakcs -> 3


#args + kwargs

def doubler(f) :
    '''define function that refenes f'''
    def g(x) :
        return 2 * f(x)
    return g

def f1(x) : return x + 1
g = doubler(f1)
assert g(3) == 8
assert g(-1) == 0

def f2(x, y) :
    return x + y

g = doubler(f2)
try :
    g(1, 2) #won't work
except Exception :
    print("g takes in 1 argument only")

def magic(*args, **kwargs) :
    '''args are unamed arguments, kwargs are keyword arguments'''

    print("unamed args : ", args)
    print("keyword args : ", kwargs)

magic(1, 2, key  = "java")

def other_way_magic(x, y, z) :
    return  x + y  + z

x_y_list = [1, 2]
z_dict = {"z": 3}

assert other_way_magic(*x_y_list, **z_dict) #use ** for dict unpacking

def doubler_correct(f) :
    def g(*args, **kwargs) :
        return 2 * f(*args, **kwargs)
    return g

g = doubler_correct(f2)
assert g(1, 2) == 6

#type annotations in python (dynamic -> static)

def total(xs : list) -> float :
    return sum(total)

#even more specific
from typing import List
def total(xs : List[float]) -> float :
    return sum(total)

#type annotating variables
x : float = 5.0

#not specifiying type below :
values = []
best_so_far = None

#specifiying type :
from typing import Optional

values = List[int] = []
best_so_far = Optional[float] = None #can be both a None and float

#other type annotations with typing module
from typing import Dict, Iterable, Tuple

counts : Dict[str, int] = {"data" : 1, "science" : 2}

lazy = False
if lazy :
    events = Iterable[int] = (x for x in range(10) if x % 2 == 0)
else :
    evens = [0, 2, 4, 6, 8]

triple = Tuple[int, float, int] = (10, 2.3, 5)

from typing import Callable
def twice(repeater : Callable[[str, int], str], s:str) -> str :
    return repeater(s, 2)

def comma_repeater(s : str, n : int) -> str :
    n_copies = [s for _ in range(n)]
    return ",".join(n_copies)

print("2x : " , twice(comma_repeater, "type_hints"))

#to redefine them easier
Number = int
Numbers = List[Number]

def total(xs : Numbers) -> Number :
    return sum(xs)




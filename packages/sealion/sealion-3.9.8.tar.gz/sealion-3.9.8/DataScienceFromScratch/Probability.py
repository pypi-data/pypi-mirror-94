# Two events E and F are independent if
# the probability of them P(E, F) = product of each one or P(E)P(F)
from DataScienceFromScratch.Statistics import mean
from collections import Counter

'''
->> independence : P(E, F) = P(E)P(F)
->> otherwise they are conditional : P(E | F) = P(E, F)/P(F) #the P(event a | event b) means prob of A
given B
->> P(E, F) = P(E|F)P(F)
->> P(E|F) = P(E), when E and F are independent events (being conditional on F doesn't change P(E) in P(E | F)

Famous example :
- >> if there are two children and one is a girl (G) what's the probability both are girls (B)
->> this is P(B|G) = P(B, G)/P(G) = P(B)/P(G) = 1/2 / 1 = 1/2
->>  P(B, G) = P(B) as the two events are independent
->> P(B, G) = P(B)P(G)/P(G) = P(B) = 1/2 anyways...

Slightly harder example :
->> probability of event B given at least one is a girl (L)
->> P(B | L)  = P(B)/P(L) = 1/3!
->> if you know at least 1 of the children is a girl, then it is 2x more likely there is one boy and one girl (0.5)
than just both (0.25), so only 1 out of 3 times will you meet a family with that 0.25 case

Bayes Theorem :
->> P(H|E) = P(E|H)P(H)/ P(E|H)P(H) + P(E!H)P(!H)
->> this could be for instance that if 99% of the time people are diagnosed correctly and 1% has the disease
->> H = actually +, and E is diagnosed positive
then ->> P(actually positive) = 0.99(0.01)/ (0.99 * 0.01 + 0.01 * 0.99) = 0.5% is correctly diagnosed
->> another way to think about this could be that in a population with a thousand people you would expect
->> 10 of them to have the disease and 9 to test positive. Out of the other 990 that don't have the disease
you would expect then that about 10 of them test posiitve. So 9/(9 + 10) shows the test is only 47% accurate.
'''

#example to prove that :
import enum, random
# Enum is a set of items attached to values
class Kid(enum.Enum) :
    BOY = 0
    GIRL = 1
def random_kid() -> Kid  :
    return random.choice([Kid.BOY, Kid.GIRL])

both_girls = older_girl = either_girl = 0

for _ in range(10000) :
    younger = random_kid()
    older = random_kid()
    if older == Kid.GIRL :
        older_girl += 1
    if older == Kid.GIRL and younger == Kid.GIRL :
        both_girls += 1
    if older == Kid.GIRL or younger == Kid.GIRL :
        either_girl += 1

print("P(both | older) : ", (both_girls/older_girl)) #chance of getting both girls
print("P (both | either) : ", (both_girls/either_girl)) #chance of having both given at least

'''
Note on Random Variables : 
-> implicitly defined in typical data science
->> a random variable is a variable whose possible values have a probability distribution
->> this could be 0 if tails, 1 if heads so var = {0 <- 1/2 and 1 <- 1/2}
->> there is an expected value result, which is just the sum of each prob * value
->> another example of a random variable could be Y where it gives the number of girls conditional on either
->> Y = {1 : 2/3, 2 : 1/3}
->> Z = {1 : 1/2, 2 : 1/2}, Z could be how many boys you have if you already have one
'''

def expected_value(random_variable) :
    '''random_variable is dict'''
    return sum([item * prob for item, prob in random_variable.items()])

assert expected_value({0 : 0.5, 1 : 0.5}) == 0.5
assert expected_value({2 : 0.5, 3 : 0.25, 10 : 0.25}) == 17/4

'''
Notes on PDFs and CDFs : 
->> a probability density function is tellling us the probability of a value leading to a result
->> integral of PDF must equal 1 
->> CDF (cumulative distributon gives the probability) something is less than or equal to a value
->> see page 81, looks like as it goes to 0.5, prob is 0.5 (cumulative from 0.0 - 0.5) and as it goes to 0.9 it's 0.9 (cumulative from 0.0 - 0.9)
'''

def uniform_pdf(x : float) -> float :
    return 1 if 0 <= x < 1 else 0

def uniform_cdf(x : float) -> float :
    '''returns probability that a uniform variable (0 or 1) is less than x'''
    if x < 0 : return 0 #uniform var never less than 0
    elif x < 1 : return x #i.e. if it's 0.5 (cumulative), then prob is 0.5
    else : return 1 #yes because if x >= 1, a uniform var is for sure <= x

'''
Normal Distribution : 
->> shorter skinnier, longer more dull 
->> PDF : f(x | mu, std) = 1/(sqrt(2pi) * std) * exp(-(x-mu)^2/2*std^2))
'''

import math
SQRT_TWO_PI = math.sqrt(2 * math.pi)

def normal_pdf(x: float, mu : float = 0, sigma : float = 1) -> float :
    return (math.exp(-(-x-mu)**2 / 2/ sigma ** 2)/(SQRT_TWO_PI * sigma))

#plot some of these PDFs
import matplotlib.pyplot as plt
xs = [x/10.0 for x in range(-50, 50)]
plt.plot(xs, [normal_pdf(x) for x in xs], '-', label = "mu=0, sigma=1")
plt.plot(xs, [normal_pdf(x, sigma = 2) for x in xs], '--', label = "mu=0, sigma=2")
plt.plot(xs, [normal_pdf(x, sigma = 0.5) for x in xs], ':', label = "mu=0, sigma=0.5")
plt.plot(xs, [normal_pdf(x, mu = -1) for x in xs], '-.', label = "mu=-1, sigma=1")
plt.legend()
plt.title("Various Normal PDFs")
plt.show()

'''notice how shrinking the deviation makes the PDF taller and skinnier'''
'''increasing deviation does the opposite, and changing mean changes the center of the data'''

'''
The standard normal distribution is when mu = 0, std/sigma = 0 (of any PDF - normal or random).
If Z is a standard normal variable, then : 
X = sigmaZ + mu is also normal but with mean u and std sigma (hence why np.random.randn() * sqrt(2/fan_in)) 
creates sqrt(2/fan_in) variance as np.random.random() is already a standard normal distribution

Conversely if X is a normal random variable with mu and sigma : 
Z = (X - mu)/sigma is also standard normal variable
'''

def normal_cdf(x : float, mu : float = 0 , sigma : float =1) -> float :
    '''chance anything selected in the given normal PDF is less than x'''
    return (1 + math.erf((x-mu)/math.sqrt(2)/sigma)) / 2

plt.cla()
plt.plot(xs, [normal_cdf(x, sigma=1) for x in xs], '-', label = 'mu=0, sigma = 1')
plt.plot(xs, [normal_cdf(x, sigma=2) for x in xs], '--', label = 'mu=0, sigma = 2')
plt.plot(xs, [normal_cdf(x, sigma=0.5) for x in xs], ':', label = 'mu=0, sigma = 0.5')
plt.plot(xs, [normal_cdf(x, mu=-1) for x in xs], '-.', label = 'mu=-1, sigma = 1')
plt.legend(loc = 4) #bottom right
plt.title("Various Normal CDFs")
plt.show()

'''
Sometimes we will need to invert normal_cdf to find the value corresponding
to a specified probability. Normal_cdf is continuous and increasing, so you can use 
the binary search algorithm.
'''

def inverse_normal_cdf(p : float, mu :float =0, sigma : float = 1,
                       tolerance : float = 0.000001) -> float :
    '''find approximate inverse using binary search'''
    #if not standard, compute and rescale
    if mu != 0 or sigma != 1 :
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance) #cstandardize
    low_z = -10 #normal_cdf(-10) is very close to 0
    high_z = 10 #normal_cdf(10) is very close to 1
    while high_z  - low_z > tolerance :
        mid_z = (low_z + high_z)/2 #find midpoint
        mid_p = normal_cdf(mid_z) #find cdf value there
        if mid_p < p :
            low_z = mid_z #midpoint too low, search above it
        else :
            high_z = mid_z #midpoint too high, search below it
    return mid_z

print(inverse_normal_cdf(0.5))

'''
Why is the normal distribution useful? 
->> sampled averages of any dataset create a normal distribution
'''

xs = [_ for _ in range(-100, 100)]
ys = [2 * x + 1 for x in xs]
sample_size = 30
n_means = 10000
means = []
for _ in range(n_means) :
    start_index = random.randint(0, len(xs) - sample_size)
    sample = ys[start_index : start_index + sample_size]
    means.append(mean(sample))

plt.cla()
frequency_means = Counter(round(mean/10) * 10 for mean in means)
plt.bar(
    [fr + 5 for fr in frequency_means.keys()], frequency_means.values()
)


"""
Why is the normal distribution so useful? 

- the central limit theorem states that any random variable that comes 
from an average of an identically distributed set creates a normal distribution. 

(x1 + ... xN) - mean * n_samples / sigma * sqrt(n_samples) is equal to the normal distribution
where the denominator sigma * sqrt(n_samples) is the std

Binomial Random Variables - > Binomial(n, p) random variable is the sum 
of n bernoulli trials, each with a probability p of 1 and 1 - p of 0 
"""

def bernoulli_trial(p : float) -> int :
    """Returns 1 with probability p and 0 with probability 1 - p"""
    return 1 if random.random() < p else 0 #the smaller the p, the more likely
    # random.random() will be less than p and vice versa.

def binomial(n : int, p : float) -> float :
    '''return the sum of n bernoulli trials with probability p '''
    return sum(bernoulli_trial(p) for trial in range(n))

"""
the mean of a bernoulli(p) variable is p, and its std is sqrt(p(1-p))

the central limit theorem states that as n gets large, a binomial(n, p) 
variable has mu = np, and a standard deviation of sqrt(np(1-p))
"""

#proving this

def binomial_histogram(p : float, n : int, num_points : int) -> None :
    """Pick points from a binomial (n, p) and plot their histogram"""

    data = [binomial(n, p) for _ in range(num_points)]

    #use a bar chart to show the actual binomial samples
    histogram = Counter(data)
    plt.bar([x - 0.4 for x in histogram.keys() ],
            [ v / num_points for v in histogram.values()],
            0.8,
            color = '0.75')

    mu = n * p
    sigma = math.sqrt(n * p * (1 - p)) #todo understand why it is this

    #use a line chart to show the normal approximation
    xs = range(min(data), max(data) + 1)
    ys = [normal_cdf(i + 0.5, mu, sigma) - normal_cdf(i - 0.5, mu , sigma)
          for i in xs] #this is because of continuity correction we have the +/- 0.5
    plt.plot(xs, ys)
    plt.title("binomial distribution vs. normal approximation")
    plt.show()

binomial_histogram(0.5, 100, 10000)

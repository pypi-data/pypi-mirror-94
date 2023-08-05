'''
- data sciencetists can assume data statistics as random variables from a distribution
- a null hypothesis, H0, represents some default position and H1, the alternative hypothesis,
 is what we would like to compare it to
'''

#Example : Flipping a Coin

#null hypothesis that the coin is fair if p = 0.5, here p is the probability of landing heads

#each coin flip is a bernoulli trial, and we have binomial (n , p) random var, which can be approxcimated

from typing import Tuple
import math

def normal_approximation_to_binomial(n : int, p : float) -> Tuple[float, float] :
    '''return mu and sigma corresponding to a Binomial(n, p)'''
    mu = n * p
    sigma = math.sqrt(p * (1  - p) * n )
    return mu, sigma

#Whenever a random variable follows a normal distribution, use the cdf to see if it lies between a given interval

from DataScienceFromScratch.Probability import normal_cdf

#the Normal cdf is the probability the variable is below a threshold (cumulative)

normal_probability_below = normal_cdf

#if it's above the threshold then it's not below
def normal_probability_above(lo : float,
                             mu : float = 0,
                             sigma : float = 1) -> float :
    """the probability that an N(mu, sigma) is greater than lo"""
    return 1 - normal_probability_below(lo, mu, sigma)

#less than hi, but more than lo
def normal_probability_between(lo : float,
                               ho : float,
                               mu : float = 0,
                               sigma : float = 1) -> float :
    '''probability it's between lo and ho'''
    return normal_cdf(ho, mu, sigma) - normal_cdf(lo, mu, sigma)

#and outside (1 - between)
def normal_probability_outside(lo : float,
                               ho : float,
                               mu : float = 0,
                               sigma : float = 1) -> float :
    return 1 - normal_probability_between(lo, ho, mu, sigma)

"""
We can also do the reverse, where we find an interval which contains a given % probability

An example could be an interval with 60% probability, so a upper tail at 80% and a lower tail and 20% will leave 60%
and each will have 20% of the probability on each side. 
"""

from DataScienceFromScratch.Probability import inverse_normal_cdf

def normal_upper_bound(probability : float,
                       mu : float = 0,
                       sigma : float = 1) -> float :
    """returns the higher z, or the value that leads to the given probability on the CDF (mu, sigma)"""
    return inverse_normal_cdf(probability, mu, sigma)

def normal_lower_bound(probability : float,
                       mu : float = 0,
                       sigma : float = 1) :
    '''take a probability, like 80% and find a value giving prob 20% on the CDF'''
    return inverse_normal_cdf(1 - probability, mu, sigma)

def normal_two_sided_bounds(probability : float,
                            mu : float = 0,
                            sigma : float = 1) -> Tuple[float, float] :
    """
    Return the lower and upper bound to create an interval which contains a given probability
    """

    tail_probability = (1 - probability) / 2 #here this is 0.2

    #upper bound shuold have tail_probability above it
    upper_bound = normal_lower_bound(tail_probability, mu, sigma) #finds the upper 80% threshold

    #lower bound should have tail probability below it
    lower_bound = normal_upper_bound(tail_probability, mu, sigma) #finds the lower 20% threshold

    return lower_bound, upper_bound

mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5) #(n,p) for our null hypothesis p = 0.5 for 1000 trials
#mu0, sigma0 if the coin is far (H0, null hypothesis is correct)

lower_bound, upper_bound = normal_two_sided_bounds(0.95, mu_0, sigma_0)
#if X, the number of heads after n trials, is outside the lower and upper bounds, then the coin is not fair (H0 is wrong)

print("Lower : ", lower_bound, " ; Upper : ", upper_bound)

#we are also want to know the Power of a test, in which we fail to reject H0 despite it being false
"""
H0 here is false if p ≠ 0.5, so we can test for p = 0.55 for example. We want to see what percent of our bound is correct
given a different p, or what's the chance we reject H0 with a different p. 
"""

lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0) # given the actual p's mean and std, find the bounds containing
 # 95 % of the probability

#the actual mu and sigma given p = 0.55
mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)

# a type 2 error means we fail to reject the null hypothesis,
# which happens when X is still in the original interval for p = 0.5 (our null hypothesis.)

type2_probability = normal_probability_between(lo, hi, mu_1, sigma_1) #given the range for the null hypothesis
# find the probability shared between the two
power = 1 - type2_probability

print("This is the power : ", power)

"""
Instead if our null hypothesis was that the coin liked tails more, or p ≤ .5, and that should have X lower than 500.

hi = normal_upper_bound(0.95, mu_0, sigma_0) #upper bound for 95% confidence
type2_probability = normal_probability_below(hi, mu1, sigma1) #calculate probablity from X = 0 to the high X 
power = 1 - type2_probability #a change in the p value (giving mu1, sigma1) changes the probability on both CDFs.
"""

'''
P-values!

Compute the probability that assuming H0 is true, would we see a value at at least as extreme as observed? 

The reason we do this is because a low p-rate shows that the data assuming the null was not by chance. Therefore
we are almost calculating the significance in the alternative hypothesis with a p-value as the lower it is the less
significance. If there is less significance in the alternative hypothesis through the p-vaue then there is significance
in the null hypothesis, we reject the null hypothesis.
'''

def two_sided_p_value(x : float, mu : float = 0, sigma : float = 1) -> float :
    """How likely are we to see a value as extreme as x if values are from N(mu, sigma)?"""

    if x >= mu :
        #x is greater than the mean, the tail is everything greater than x
        return 2 * normal_probability_above(x, mu, sigma)
    else :
        return 2 * normal_probability_below(x, mu, sigma)


two_sided_p_value(529.5, mu_0, sigma_0) #0.062 or 6.5% chance that given p =0 you see 530 heads
'''we used a continuity correction for the 0 and 1 distribution (discrete) not 0 -1 distribution. So 529.5 not 530'''

#another way to prove this :

import random
extreme_value_count = 0
for _ in range(1000) :
    num_heads = sum(1 if random.random() < 0.5 else 0 #count num heads
                    for _ in range(1000)) #in 1000 flips

    if num_heads >= 530 or num_heads <= 470 : #how often is this extreme
        extreme_value_count += 1

#assert 59 <= extreme_value_count <= 65, f"{extreme_value_count}"

"""
If the p-value (sort of the significance of the alternative hypothesis) is lower than the significance of our 
null hypothesis, reject the null hypothesis.
"""

upper_p_value = normal_probability_above
lower_p_value = normal_probability_below
print("Significance : 5%")
print("525 heads : ", upper_p_value(524.5, mu_0, sigma_0), " : acccept; > significance")
print("527 heads : ", upper_p_value(526.5, mu_0, sigma_0), " : reject; < significance")

"""ALWAYS MAKE SURE THE DATA IS NORMALLY DISTRIBUTED BEFORE CALCULATING P-VALUES"""

"""
Confidence Intervals : 

They give you an interval that spans confidence_level % of the data. It is confidence_level (usually 95%) % confident 
that the parameter is there. Always create a normal distribution centered around getting that value first. 
"""

p_hat = 525 / 1000 #our estimate of how many heads
mu = p_hat #here we get mu and sigma from the 0.525 heads rate by treating each trial out of 1000 as a bernoulli trial
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000)
confidence_interval = normal_two_sided_bounds(0.95, mu, sigma) #0.49 - 0.55
print("This is the confidence interval : ", confidence_interval)

#if we had a fair coin
p_hat = 0.5
mu = p_hat
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000)
confidence_interval = normal_two_sided_bounds(0.95, mu, sigma) #0.46 - 0.53
print("This is the confidence interval : ", confidence_interval)

"""
p-hacking : 

You can always change the data and test enough hypothesis to get a p < 0.05 so you can reject the null hypothesis.

running it over and over again ensures that you get a hypothesis with a high significance that is likely to reject
the null hypothesis. these hypotheses generated are the experiments and the number of tails and heads in them. You are
sure to find some that are significant and that disprove the null hypothesis. That way you can find hypothesis that
do disprove the null. 
"""

from typing import List

def run_experiment() -> List[bool] :
    '''Flips a fair coin 1000 times, True is head and False is tails'''
    return [random.random() < 0.5 for _ in range(1000)]

def reject_fairness(experiment : List[bool]) -> bool :
    '''using the 5% significance level'''
    num_heads = len([flip for flip in experiment if flip]) #only if the flip is true count it
    return num_heads < 469 or num_heads > 531 #62 values are extreme in the dataset so we want to see if this is in
    # the fair boundary

random.seed(0)
experiments = [run_experiment() for _ in range(1000)]
num_rejections = len([experiment
                      for experiment in experiments
                      if reject_fairness(experiment)]) #count the number of rejected experiments
assert num_rejections == 46

print("we are rejecting ", num_rejections, " points of the data, not 62 like with the null hypothesis - "
                                            "therefore bye null!")


"""
Running A/B test. 

Let's say Na people see ad A, and na click it. Each ad is a Bernoulli trial where pa is the probably 
somebody clicks it. 

That means we can represent the trials mean as pa and its standard deviation as sigmaA = sqrt(pa(1-pa) / Na)

Similarity ad B has mean pb and std sigmaB = sqrt(pb(1 - pb) / Nb)
"""

def estimated_parameters(N : int, n : int) -> Tuple[float, float] :
    p = n / N
    sigma = math.sqrt(p * (1 - p) / N)
    return p, sigma #what percent click it, std

#our null hypothesis is that pa = pb

def a_b_test_statistic(N_a : int, n_A : int, N_b : int, n_B : int) -> float :
    p_A, sigma_A = estimated_parameters(N_a, n_A)
    p_B, sigma_B = estimated_parameters(N_b, n_B)
    return (p_B - p_A) / math.sqrt(sigma_A ** 2 + sigma_B ** 2) #todo understand why this?

z = a_b_test_statistic(1000, 200, 1000, 180) #ad A got 200 / 1000 clicks and ad B got 180 / 1000 clicks
print("probability of change/importance : ", two_sided_p_value(z)) #todo understand why p-value?

z = a_b_test_statistic(1000, 200, 1000, 150)
print("probability of change/importance : ", two_sided_p_value(z)) #barely anything

"""
Bayesian Inference : 

Here you first start out with a prior distribution and use bayes theorem to update based on new data
the chance of any event happening (this updated distribution is the posterior distribution.)  

You use a beta distribution to put the probabilities from 0 to 1 to create such a distribution. 

An example would first to start out with Beta(20, 20) which expresses the belief of a fair coin. Then flip a bit more, 
count the number of heads and tails and update beta as beta + t and alpha as alpha + h where h, t are the number
of heads and tails respectively. You may get Beta(100, 101) where alpha = 100, beta = 101 - which is very true to 
our original hypothesis. Bayesian Inference is about updating past beliefs on the evidence found in new data. 
"""

def B(alpha : float, beta : float) -> float :
    '''Normalizing factor makes sure probabilities are from 0 - 1'''
    return math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)

def beta_pdf(x : float, alpha : float, beta : float) -> float :
    if x <= 0 or x >= 1 : #outside of pdf
        return 0
    return x ** (alpha - 1) * (1 - x) ** (beta - 1) / B(alpha, beta)

#the distribution is centered at alpha / (alpha + beta)
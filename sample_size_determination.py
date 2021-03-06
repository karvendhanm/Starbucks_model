# Practical Significance

# import packages
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Lets say have a baseline web portal click-through rate of 10% and want to
# see a manipulation increase this baseline to 12%. How many observations would
# we need in each group in order to detect this change with power  1−𝛽=.80
# (i.e. detect the 2% absolute increase 80% of the time), at a Type I error
# rate of  𝛼=.05 ?

# Trial and Error Method:
# -------------------------

# One way we could solve this is through trial and error. Every sample size
# will have a level of statistical power(1-𝛽) associated with it; testing
# multiple sample sizes will gradually allow us to narrow down the minimum
# sample size required to obtain our desired statistical power(1-𝛽) level. Even
# though this isn't a particularly efficient method, but it can provide an
# intuition for how experiment sizing works.


def power(p_null, p_alt, n, alpha = .05, plot = True):
    """
        Compute the power of detecting the difference in two populations with
        different proportion parameters, given a desired alpha rate.

        Input parameters:
            p_null: base success rate under null hypothesis
            p_alt : desired success rate to be detected, must be larger than
                    p_null
            n     : number of observations made in each group
            alpha : Type-I error rate
            plot  : boolean for whether or not a plot of distributions will be
                    created

        Output value:
            power : Power to detect the desired difference, under the null.
        """
    #(Refer book: Statistics for Management
    # (Seventh Edition ISBN 978-81-317-7450-2) under the topic :
    # One-Tailed Tests for  Difference between Proportions)

    se_null = np.sqrt((1/n) * (2 * p_null * (1 - p_null)))
    null_dist = stats.norm(loc = 0, scale = se_null)

    # ppf function here takes the proportion of area under the curve and
    # gives out the corresponding x value. cdf function does the reverse.
    # cdf gives out the cumulative distribution function evaluated at the
    # point x.
    p_crit = null_dist.ppf(1 - alpha)

    se_alt = np.sqrt((1/n) * ((p_null * (1 - p_null)) + (p_alt * (1 - p_alt))))
    alt_dist = stats.norm(loc = p_alt - p_null, scale = se_alt)
    beta = alt_dist.cdf(p_crit)

    if plot:
        # Compute distribution heights
        low_bound = null_dist.ppf(.01)
        high_bound = alt_dist.ppf(.99)
        x = np.linspace(low_bound, high_bound, 201)
        y_null = null_dist.pdf(x)
        y_alt = alt_dist.pdf(x)

        # Plot the distributions
        plt.plot(x, y_null)
        plt.plot(x, y_alt)
        plt.vlines(p_crit, 0,
                   np.amax([null_dist.pdf(p_crit), alt_dist.pdf(p_crit)]),
                   linestyles='--')
        plt.fill_between(x, y_null, 0, where=(x >= p_crit), alpha=.5)
        plt.fill_between(x, y_alt, 0, where=(x <= p_crit), alpha=.5)

        plt.legend(['null', 'alt'])
        plt.xlabel('difference')
        plt.ylabel('density')
        plt.show()

    # return power
    return (1 - beta)

#power(.1, .12, 1000) # Statistical power approx 44%
#power(.1, .12, 2000) # Statistical power approx 67%
power(.1, .12, 2863) # Statistical power little over 80%

# Analytic Solution:
# ------------------

# The key point to notice is that, for an  𝛼  and  𝛽  both < .5, the critical
# value for determining statistical significance will fall between our null
# click-through rate and our alternative, desired click-through rate.
# So, the difference between  𝑝0  and  𝑝1  can be subdivided into the distance
# from  𝑝0  to the critical value  𝑝∗  and the distance from  𝑝∗  to  𝑝1 .

def experiment_size(p_null, p_alt, alpha=.05, beta=.20):
    """
    Compute the minimum number of samples needed to achieve a desired power
    level for a given effect size.

    Input parameters:
        p_null: base success rate under null hypothesis
        p_alt : desired success rate to be detected
        alpha : Type-I error rate
        beta  : Type-II error rate

    Output value:
        n : Number of samples required for each group to obtain desired power
    """

    # Get necessary z-scores and standard deviations (@ 1 obs per group)
    z_null = stats.norm.ppf(1 - alpha)
    z_alt = stats.norm.ppf(beta)
    sd_null = np.sqrt(2 * p_null * (1 - p_null))
    sd_alt = np.sqrt((p_null * (1 - p_null) + (p_alt * (1 - p_alt))))

    p_diff = p_alt - p_null
    n = ((z_null*sd_null - z_alt*sd_alt) / p_diff) ** 2
    return np.ceil(n)

experiment_size(0.1, 0.12)


# Alternative Approaches
# example of using statsmodels for sample size calculation
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# leave out the "nobs" parameter to solve for it
NormalIndPower().solve_power(effect_size = proportion_effectsize(.12, .1), alpha = .05, power = 0.8,
                             alternative = 'larger')




















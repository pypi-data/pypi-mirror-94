# distributions package

The package contains modules that can be used to create Binomial and Gaussian distribution objects and perform operations on them.

# Files

Binomialdistribution.py: Contains the Binomial class that can be used to create binomial distribution objects, given the number of trials and the probablity of an event occuring, or by reading in data from a data file.

Gaussiandistribution.py: Contains the Gaussian class that can be used to create gaussian distribution objects, which can be initialized providing the distribution's mean and standard deviation or reading in data from a file.

Generaldistribution.py: Contains the Distribution class, with common dsitribution attributes and methods. Inherited by both, Binomial and Gaussian classes.

# Installation

pip install such-distribution

# Usage Example

>>> from distributions import *
>>> Binomial(0.3, 10)
mean 3.0, standard deviation 1.4491376746189437, p 0.3, n 10
>>> Gaussian(10, 80)
mean 10, standard deviation 80
>>> bd1 = Binomial(0.4, 20)
>>> bd2 = Binomial(0.4, 30)
>>> bd1 + bd2
mean 20.0, standard deviation 3.4641016151377544, p 0.4, n 50
>>> gd1 = Gaussian(8, 20)
>>> gd2 = Gaussian(7, 30)
>>> gd1 + gd2
mean 15, standard deviation 36.05551275463989

## Read line separated values from a file

>>> gd1.read_data_file('/home/numbers.txt')
>>> gd1.calculate_mean()
78.0909090909091
>>> gd1.calculate_stdev()
92.87459776004906
>>> bd1.read_data_file('/home/numbers_binomial.txt')
>>> bd1.replace_stats_with_data()
(0.6153846153846154, 13)
>>> bd1.mean
8.0
>>> bd1.stdev
1.7541160386140584
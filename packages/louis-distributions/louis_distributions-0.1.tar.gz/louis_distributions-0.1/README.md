## Binomial and Gaussian distributions in Python

This repository contains three Python classes: Generaldistribution, Gaussian and Binomial, to be used for probabilistic calculations in Python. It was built as part of the Udacity Data Science Nanodegree.

## Contents of the repository:

-  distributions folder: 
	- Binomialdistribution.py: contains the Binomial distribution class
    - Gaussiandistribution.py: contains the Gaussian distribution class
    - Generaldistribution.py: contains a parent class with shared methods, which the other two classes inherit from
    - __init__.py: required for pip packages, and includes shortcuts to allow users to directly access the classes after importing the modules
- license.txt: required for uploads to PyPi or TestPyPi: contains basic copyright information, taken from the MIT template
- setup.cfg: 

## Business questions:

We wanted to answer the following questions:
- Looking at the audio features, which ones influence popularity?
- Does this influence change over time? Ie: do we see different correlations between features and popularity for tracks released in the 60s, compared to tracks released in in 2020?
- Does this change based on the musical genre of the track? 
- How accurately can we predict a track's popularity score using its metadata and its audio features?

## Conclusions:

In summary, we found that we can indeed build a pretty accurate (r-squared > 0.75) linear model to predict track popularity. However, it seems that the main factor influencing popularity is the track's release year, with audio features such as danceability (positive impact) and speechiness (negative impact) influencing the result to a lesser degree. 
This is mostly constant over time, although we do see that explicitness becomes more important as we get closer to 2020, as does danceability. 
Regarding the musical genres, we found that restricting ourselves to a specific genre makes our models less accurate, and conclusions are harder to draw. 

## Libraries used:

import pandas as pd
import matplotlib.pyplot as plt
import sklearn as sc
from sklearn.model_selection import train_test_split
import numpy as np
import ast
from scipy import stats
import seaborn as sns
from sklearn.linear_model import LinearRegression
from collections import Counter

## Acknowledgements:

- I used this solution to be able to break up the genre column into manageable chunks: https://github.com/softhints/python/blob/master/notebooks/pandas/Pandas_count_values_in_a_column_of_type_list.ipynb
- This article (which I came across after I finished the work here) offers a different perspective, with some similar conclusions: https://towardsdatascience.com/what-makes-a-song-likeable-dbfdb7abe404
- I re-used a few functions and code snippets from the Udacity course: Introduction to Data Science

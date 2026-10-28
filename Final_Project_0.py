import pandas as pd
import numpy as np

# Load the dataset
dataset = pd.read_csv('Crime_Incidents_in_2025.csv')

#view dimensions
dataset.shape

#displays column names
dataset.columns

# view the first 5 rows
dataset.head()

# view information about the dataset
dataset.info()

#summary of the dataset
dataset.describe()

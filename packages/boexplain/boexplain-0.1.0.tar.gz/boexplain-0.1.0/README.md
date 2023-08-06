# BOExplain, Explaining Inference Queries with Bayesian Optimization 

BOExplain is a library for explaining inference queries with Bayesian optimization.

## Installation


## Documentation

The documentation can be found [here](https://sfu-db.github.io/BOExplain/). (shortcut to [fmin](https://sfu-db.github.io/BOExplain/api_reference/boexplain.files.search.html#boexplain.files.search.fmin), [fmax](https://sfu-db.github.io/BOExplain/api_reference/boexplain.files.search.html#boexplain.files.search.fmax))

## Getting Started

Derive an explanation for why the predicted rate of having an income over $50K is higher for men compared to women in the UCI ML [Adult dataset](https://archive.ics.uci.edu/ml/datasets/adult).

1. Load the data and prepare it for ML.
``` python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# read the data
df = pd.read_csv("adult.data",
                 names=[
                     "Age", "Workclass", "fnlwgt", "Education",
                     "Education-Num", "Marital Status", "Occupation",
                     "Relationship", "Race", "Gender", "Capital Gain",
                     "Capital Loss", "Hours per week", "Country", "Income"
                 ],
                 na_values=" ?")
# feature engineer
df['Income'].replace({" <=50K": 0, ' >50K': 1}, inplace=True)
df['Gender'].replace({" Male": 0, ' Female': 1}, inplace=True)
df = pd.get_dummies(df)
# split into training and testing data
train, test = train_test_split(df, test_size=0.2)
test = test.drop(columns='Income')
```

2. Define the objective function that trains a random forest classifier and queries the ratio of predicted rates of having an income over $50K.
``` python
def obj(train_filtered):
    # create and train a random forest classifier
    rf = RandomForestClassifier(n_estimators=13, random_state=0)
    rf.fit(train_filtered.drop(columns='Income'), train_filtered['Income'])
    # update the inference data with the predictions
    test["prediction"] = rf.predict(test)
    # query the ratio of the high income rates for men and women
    rates = test.groupby("Gender")["prediction"].sum() / test.groupby("Gender")["prediction"].size()
    test.drop(columns='prediction', inplace=True)
    return rates[0] / rates[1]
```


3. Use the function `fmin` to minimize the objective function.
``` python
from boexplain import fmin

# train_filtered is the training data after removing tuples that satisfy the predicate
train_filtered = fmin(
    data=train,  # the data
    f=obj,  # the objective function
    columns=["Age", "Education-Num"],  # columns to derive a predicate from
    runtime=30,  # run for 30 seconds
)
```
<!-- which returns a predicate 28 <= Age <= 59 and 6 <= Education-Num <= 16. Removing the tuples satisfying the returned predicate reduces the ratio from 3.54 to 2.7. -->

## Reproduce the Experiments

To reproduce the experiments, you can clone the repo and create a poetry environment (install [Poetry](https://python-poetry.org/docs/#installation)). Run

```bash
cd BOExplain
poetry install
```

To setup the poetry environment for jupyter notebook run

```bash
poetry run ipython kernel install --name=boexplain
```

An ipython kernel has been created for this environemnt.

### Adult Experiment

To reproduce the results of the Adult experiment and recreate Figure 6, follow the instruction in adult.ipynb.

### Credit Experiment

To reproduce the results of the Credit experiment and recreate Figure 8, follow the instruction in credit.ipynb.

### House Experiment

To reproduce the results of the House experiment and recreate Figure 7, follow the instruction in house.ipynb.

### Scorpion Synthetic Data Experiment

To reproduce the results of the experiment with Scorpion's synthetic data corresponding query and recreate Figure 4, follow the instruction in scorpion.ipynb. 

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boexplain',
 'boexplain.files',
 'boexplain.optuna',
 'boexplain.optuna.optuna',
 'boexplain.optuna.optuna.pruners',
 'boexplain.optuna.optuna.samplers',
 'boexplain.optuna.optuna.samplers.tpe',
 'boexplain.optuna.optuna.storages',
 'boexplain.optuna.optuna.trial']

package_data = \
{'': ['*'],
 'boexplain.files': ['.ipynb_checkpoints/*'],
 'boexplain.optuna': ['.ipynb_checkpoints/*']}

install_requires = \
['altair==4.1.0',
 'colorlog==4.4.0',
 'imblearn==0.0',
 'numpy==1.20.0',
 'numpyencoder==0.3.0',
 'pandas==1.2.1',
 'scikit-learn==0.24.1',
 'scipy==1.6.0',
 'tqdm==4.51.0']

setup_kwargs = {
    'name': 'boexplain',
    'version': '0.1.0',
    'description': 'BOExplain',
    'long_description': '# BOExplain, Explaining Inference Queries with Bayesian Optimization \n\nBOExplain is a library for explaining inference queries with Bayesian optimization.\n\n## Installation\n\n\n## Documentation\n\nThe documentation can be found [here](https://sfu-db.github.io/BOExplain/). (shortcut to [fmin](https://sfu-db.github.io/BOExplain/api_reference/boexplain.files.search.html#boexplain.files.search.fmin), [fmax](https://sfu-db.github.io/BOExplain/api_reference/boexplain.files.search.html#boexplain.files.search.fmax))\n\n## Getting Started\n\nDerive an explanation for why the predicted rate of having an income over $50K is higher for men compared to women in the UCI ML [Adult dataset](https://archive.ics.uci.edu/ml/datasets/adult).\n\n1. Load the data and prepare it for ML.\n``` python\nimport pandas as pd\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\n\n# read the data\ndf = pd.read_csv("adult.data",\n                 names=[\n                     "Age", "Workclass", "fnlwgt", "Education",\n                     "Education-Num", "Marital Status", "Occupation",\n                     "Relationship", "Race", "Gender", "Capital Gain",\n                     "Capital Loss", "Hours per week", "Country", "Income"\n                 ],\n                 na_values=" ?")\n# feature engineer\ndf[\'Income\'].replace({" <=50K": 0, \' >50K\': 1}, inplace=True)\ndf[\'Gender\'].replace({" Male": 0, \' Female\': 1}, inplace=True)\ndf = pd.get_dummies(df)\n# split into training and testing data\ntrain, test = train_test_split(df, test_size=0.2)\ntest = test.drop(columns=\'Income\')\n```\n\n2. Define the objective function that trains a random forest classifier and queries the ratio of predicted rates of having an income over $50K.\n``` python\ndef obj(train_filtered):\n    # create and train a random forest classifier\n    rf = RandomForestClassifier(n_estimators=13, random_state=0)\n    rf.fit(train_filtered.drop(columns=\'Income\'), train_filtered[\'Income\'])\n    # update the inference data with the predictions\n    test["prediction"] = rf.predict(test)\n    # query the ratio of the high income rates for men and women\n    rates = test.groupby("Gender")["prediction"].sum() / test.groupby("Gender")["prediction"].size()\n    test.drop(columns=\'prediction\', inplace=True)\n    return rates[0] / rates[1]\n```\n\n\n3. Use the function `fmin` to minimize the objective function.\n``` python\nfrom boexplain import fmin\n\n# train_filtered is the training data after removing tuples that satisfy the predicate\ntrain_filtered = fmin(\n    data=train,  # the data\n    f=obj,  # the objective function\n    columns=["Age", "Education-Num"],  # columns to derive a predicate from\n    runtime=30,  # run for 30 seconds\n)\n```\n<!-- which returns a predicate 28 <= Age <= 59 and 6 <= Education-Num <= 16. Removing the tuples satisfying the returned predicate reduces the ratio from 3.54 to 2.7. -->\n\n## Reproduce the Experiments\n\nTo reproduce the experiments, you can clone the repo and create a poetry environment (install [Poetry](https://python-poetry.org/docs/#installation)). Run\n\n```bash\ncd BOExplain\npoetry install\n```\n\nTo setup the poetry environment for jupyter notebook run\n\n```bash\npoetry run ipython kernel install --name=boexplain\n```\n\nAn ipython kernel has been created for this environemnt.\n\n### Adult Experiment\n\nTo reproduce the results of the Adult experiment and recreate Figure 6, follow the instruction in adult.ipynb.\n\n### Credit Experiment\n\nTo reproduce the results of the Credit experiment and recreate Figure 8, follow the instruction in credit.ipynb.\n\n### House Experiment\n\nTo reproduce the results of the House experiment and recreate Figure 7, follow the instruction in house.ipynb.\n\n### Scorpion Synthetic Data Experiment\n\nTo reproduce the results of the experiment with Scorpion\'s synthetic data corresponding query and recreate Figure 4, follow the instruction in scorpion.ipynb. \n',
    'author': 'Brandon Lockhart',
    'author_email': 'brandon_lockhart@sfu.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sfu-db/BOExplain',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

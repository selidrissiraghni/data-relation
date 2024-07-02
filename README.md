# Data Relation
![cov](https://github.com/selidrissiraghni/data-relation/blob/coverage-badge/coverage.svg)

## Getting started
```python
https://github.com/eurobios-mews-labs/data-relation.git
```
This package can be used to identify relationships between different indexes in different tables.

This package allows you to determine, for a given table, which columns represent an index and which columns represent data.

## Basic usage 


* **Identification of columns index**

```python

from data_relation import Variable
from data_relation import Table

import openml

dataset = openml.datasets.get_dataset('SpeedDating')
X, y, _, _ = dataset.get_data(dataset_format="dataframe")

df1 = X[['gender', 'age', 'age_o', 'd_age', 'd_d_age', 'race', 'race_o', 'pref_o_ambitious', 
        'pref_o_shared_interests']].drop_duplicates()

df2 = X[['race', 'race_o', 'exercise', 'dining']].drop_duplicates()


t1 = Table(df1)
t2 = Table(df2)
```
```shell
print(t1)
                             0               1
gender                   index     not nunique
age                       data  Float variable
age_o                     data  Float variable
d_age                     data   Date variable
d_d_age                  index     not nunique
race                     index     not nunique
race_o                   index     not nunique
pref_o_ambitious          data  Float variable
pref_o_shared_interests   data  Float variable

print(t2)
              0               1
race      index     not nunique
race_o    index     not nunique
exercise   data  Float variable
dining     data  Float variable

```

* **Identification of relations between index**


```python

relations_by_name = t1.get_relations_by_name(t2)

relations_by_pairs = t1.get_relations_by_pairs(t2)

```
```shell
print(relations_by_name)
       relation constraint_on_column_1 constraint_on_column_2
race        N:M              mandatory              mandatory
race_o      N:M              mandatory              mandatory

print(relations_by_pairs)
                 relation constraint_on_column_1 constraint_on_column_2
(race, race)          N:M              mandatory              mandatory
(race, race_o)        N:M              mandatory              mandatory
(race_o, race)        N:M              mandatory              mandatory
(race_o, race_o)      N:M              mandatory              mandatory

```
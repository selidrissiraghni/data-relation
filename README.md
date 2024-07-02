# Data Relation

## Getting started

```python

from data_relation import Variable
from data_relation import Table

import openml

dataset = openml.datasets.get_dataset('SpeedDating')
X, y, _, _ = dataset.get_data(dataset_format="dataframe")

df1 = X[['wave', 'gender', 'age', 'age_o', 'd_age', 'd_d_age', 'race', 'race_o', 'samerace', 
        'importance_same_race', 'importance_same_religion', 'd_importance_same_race', 
        'd_importance_same_religion', 'field','pref_o_attractive','pref_o_sincere',
        'pref_o_intelligence','pref_o_funny','pref_o_ambitious','pref_o_shared_interests']].drop_duplicates()

df2 = X[['funny_partner', 'ambition_partner', 'shared_interests_partner', 'd_attractive_partner', 
         'd_sincere_partner', 'd_intelligence_partner', 'd_funny_partner', 'd_ambition_partner', 'd_shared_interests_partner', 'tvsports','gender','race', 'race_o', 'exercise', 'dining',
          'museums', 'art', 'hiking', 'gaming', 'clubbing', 'reading', 'tv', 'theater', 'movies', 
          'concerts', 'music', 'shopping', 'yoga', 'd_sports']].drop_duplicates()

del X
del y  

t1 = Table(df1)
t2 = Table(df2)

print(t1)
print(t2)

relations_by_name = t1.get_relations_by_name(t2)
print(relations_by_name)

relations_by_pairs = t1.get_relations_by_pairs(t2)
print(relations_by_pairs)

```
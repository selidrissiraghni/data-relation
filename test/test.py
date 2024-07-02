# Copyright 2023 Eurobios
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd

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
         'd_sincere_partner', 'd_intelligence_partner', 'd_funny_partner', 'd_ambition_partner', 'd_shared_interests_partner', 
         'tvsports','gender','race', 'race_o', 'exercise', 'dining', 'museums', 'art', 'hiking', 'gaming', 'clubbing', 'reading',
           'tv', 'theater', 'movies', 'concerts', 'music', 'shopping', 'yoga', 'd_sports']].drop_duplicates()

del X
del y    

def test_is_data():
    
    c = df1['age']
    v = Variable(c)

    assert v.is_data == True

def test_is_index():
    
    c = df1['gender']
    v = Variable(c)

    assert v.is_index == True

def test_is_data_is_index_in_table():

    t = Table(df1[['age', 'gender']])

    assert t.d_variables['gender'].is_index == True
    assert 'gender' in t.index_columns

    assert t.d_variables['age'].is_data == True
    assert 'age' in t.data_columns

def test_is_data_is_index_in_table_infered_data_type():

    t = Table(df1[['age', 'gender']], 
              data_columns=['gender'], index_columns=['age'])

    assert t.d_variables['gender'].is_data == True
    assert t.d_variables['age'].is_index == True

def test_table_relation_by_name():
    
    t1 = Table(df1)
    t2 = Table(df2)

    ret = t1.get_relations_by_name(t2)

    assert ret.to_dict(orient='index') == {'gender': {'relation': 'N:M', 
                                                      'constraint_on_column_1': 'mandatory', 
                                                      'constraint_on_column_2': 'mandatory'
                                                      },
                                        'race_o': {'relation': 'N:M',
                                                   'constraint_on_column_1': 'mandatory',
                                                   'constraint_on_column_2': 'mandatory'},
                                        'race': {'relation': 'N:M',
                                                 'constraint_on_column_1': 'mandatory',
                                                 'constraint_on_column_2': 'mandatory'}}


def test_relation_N_M_opt_opt():

    c1 = pd.Series([1, 2, 3, 4, 5, 5, 6, 7], name='c1')
    c2 = pd.Series([1, 2, 3, 4, 5, 6, 6, 8], name='c2')
    
    v1 = Variable(c1)
    v2 = Variable(c2)

    assert v1 @ v2 == ('N:M', 'optional', 'optional')

def test_relation_N_M_mand_mand():

    c1 = pd.Series([1, 2, 3, 4, 5, 5, 6], name='c1')
    c2 = pd.Series([1, 2, 3, 4, 5, 6, 6], name='c2')
    
    v1 = Variable(c1)
    v2 = Variable(c2)

    assert v1 @ v2 == ('N:M', 'mandatory', 'mandatory')

def test_relation_N_M_mand_opt():

    c1 = pd.Series([1, 2, 3, 4, 5, 5, 6], name='c1')
    c2 = pd.Series([1, 2, 3, 4, 5, 6, 6, 7], name='c2')
    
    v1 = Variable(c1)
    v2 = Variable(c2)

    assert v1 @ v2 == ('N:M', 'mandatory', 'optional')

def test_relation_N_M_opt_mand():

    c1 = pd.Series([1, 2, 3, 4, 5, 6, 6, 7], name='c1')
    c2 = pd.Series([1, 2, 3, 4, 5, 5, 6], name='c2')
    
    v1 = Variable(c1)
    v2 = Variable(c2)

    assert v1 @ v2 == ('N:M', 'optional', 'mandatory')

def test_relation_1_1_mand_mand():

    c1 = pd.Series([1, 2, 3, 4], name='c1')
    c2 = pd.Series([1, 2, 3, 4], name='c2')
    
    v1 = Variable(c1)
    v2 = Variable(c2)

    assert v1 @ v2 == ('1:1', 'mandatory', 'mandatory')

def test_relation_1_1_mand_opt():

    c1 = pd.Series([1, 2, 3, 4], name='c1')
    c2 = pd.Series([1, 2, 3, 4, 5], name='c2')
    
    v1 = Variable(c1)
    v2 = Variable(c2)

    assert v1 @ v2 == ('1:1', 'mandatory', 'optional')

def test_relation_1_1_opt_mand():

    c1 = pd.Series([1, 2, 3, 4, 5], name='c1')
    c2 = pd.Series([1, 2, 3, 4], name='c2')
    
    v1 = Variable(c1)
    v2 = Variable(c2)

    assert v1 @ v2 == ('1:1', 'optional', 'mandatory')
    
def test_relation_1_N_mand_mand():

    c1 = pd.Series([1, 2, 3, 4], name='c1')
    c2 = pd.Series([1, 2, 3, 4, 4], name='c2')
    
    v1 = Variable(c1)
    v2 = Variable(c2)

    assert v1 @ v2 == ('1:N', 'mandatory', 'mandatory')
    assert v2 @ v1 == ('N:1', 'mandatory', 'mandatory')

def test_relation_1_N_opt_opt():

    c1 = pd.Series([1, 2, 3, 4, 5], name='c1')
    c2 = pd.Series([1, 2, 3, 4, 4, 6], name='c2')
    
    v1 = Variable(c1)
    v2 = Variable(c2)

    assert v1 @ v2 == ('1:N', 'optional', 'optional')
    assert v2 @ v1 == ('N:1', 'optional', 'optional')

def test_relation_1_N_opt_mand():

    c1 = pd.Series([1, 2, 3, 4, 5], name='c1')
    c2 = pd.Series([1, 2, 3, 4, 4], name='c2')
    
    v1 = Variable(c1)
    v2 = Variable(c2)

    assert v1 @ v2 == ('1:N', 'optional', 'mandatory')
    assert v2 @ v1 == ('N:1', 'mandatory', 'optional')

def test_relation_1_N_mand_opt():

    c1 = pd.Series([1, 2, 3, 4], name='c1')
    c2 = pd.Series([1, 2, 3, 4, 4, 5], name='c2')
    
    v1 = Variable(c1)
    v2 = Variable(c2)

    assert v1 @ v2 == ('1:N', 'mandatory', 'optional')
    assert v2 @ v1 == ('N:1', 'optional', 'mandatory')


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

from data_relation import Table
import openml

if __name__ == '__main__':

    dataset = openml.datasets.get_dataset('SpeedDating')
    X, y, _, _ = dataset.get_data(dataset_format="dataframe")

    df1 = X[['wave', 'gender', 'age', 'age_o', 'd_age', 'd_d_age', 'race', 'race_o', 'samerace', 
            'importance_same_race', 'importance_same_religion', 'd_importance_same_race', 
            'd_importance_same_religion', 'field','pref_o_attractive','pref_o_sincere',
            'pref_o_intelligence','pref_o_funny','pref_o_ambitious','pref_o_shared_interests']].drop_duplicates()

    df2 = X[['funny_partner', 'ambition_partner', 'shared_interests_partner', 'd_attractive_partner', 
            'd_sincere_partner', 'd_intelligence_partner', 'd_funny_partner', 'd_ambition_partner', 
            'd_shared_interests_partner', 'tvsports','gender','race', 'race_o', 'exercise', 'dining',
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
    print(len(relations_by_pairs))
    
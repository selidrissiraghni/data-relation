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

    df1 = X[['gender', 'age', 'age_o', 'd_age', 'd_d_age', 'race', 'race_o', 'pref_o_ambitious', 
        'pref_o_shared_interests']].drop_duplicates()
    df2 = X[['race', 'race_o', 'exercise', 'dining']].drop_duplicates()

    t1 = Table(df1)
    t2 = Table(df2)

    print(t1)
    print(t2)

    relations_by_name = t1.get_relations_by_name(t2)
    print(relations_by_name)

    relations_by_pairs = t1.get_relations_by_pairs(t2)
    print(relations_by_pairs)
    print(len(relations_by_pairs))
    
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

from itertools import product

import pandas as pd

from data_relation.utils import true_or_none
from data_relation.variables.base import Variable

class Table:

    def __init__(self, table: pd.DataFrame, 
                 data_columns: list = None, index_columns: list = None) -> None:

        self.data_columns = [] if data_columns is None else data_columns
        self.index_columns = [] if index_columns is None else index_columns

        self.table = table.copy()

        self.d_variables = {k: Variable(self.table[k],
                                        isdata=true_or_none(k in self.data_columns),
                                        isindex=true_or_none(k in self.index_columns))
                            for k in self.table.columns}
        self.__update_data_index_columns()

    def __update_data_index_columns(self):
        for k in self.d_variables:
            if self.d_variables[k].is_index and k not in self.index_columns:
                self.index_columns.append(k)
            if self.d_variables[k].is_data and k not in self.data_columns:
                self.data_columns.append(k)

    def get_relations_by_name(self, other):

        common_index = self.__get_common_columns(self.index_columns, other.index_columns)

        if len(common_index) == 0:
            return {}

        res = {}
        for c in common_index:
            res[c] = (self.d_variables[c] @ other.d_variables[c])

        df_res = pd.DataFrame.from_dict(res, orient='index')
        df_res.columns = ['relation', 'constraint_on_column_1', 'constraint_on_column_2']

        return df_res

    def get_relations_by_pairs(self, other):

        assert self.index_columns != [], "no index columns detected in table 1"
        assert other.index_columns != [], "no index columns detected in table 2"

        pairs = list(product(self.index_columns, other.index_columns))

        res = {}

        for pair in pairs:
            relation_pair = (self.d_variables[pair[0]] @ other.d_variables[pair[1]])
            if relation_pair:
                res[pair] = relation_pair

        df_res = pd.DataFrame.from_dict(res, orient='index')
        df_res.columns = ['relation', 'constraint_on_column_1', 'constraint_on_column_2']

        return df_res

    def __str__(self) -> str:
        return str(pd.DataFrame.from_dict({k: [self.d_variables[k],
                                               self.d_variables[k].critere_arret] 
                                               for k in self.d_variables}, orient='index'))

    def __repr__(self) -> str:
        return self.__str__()

    def __get_common_columns(self, columns1: list, columns2: list):
        return list(set(columns1).intersection(columns2))

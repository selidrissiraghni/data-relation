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

from data_relation.utils import get_relation
from data_relation.variables.compute import VariableCalcul
from data_relation.parameters import *

class Variable(VariableCalcul):

    def __init__(self, values: pd.Series, isdata: bool = None, isindex: bool = None,
                 threshold_nunique: float = DEFAULT_THRESHOLD_NUNIQUE,
                 threshold_missing: float = DEFAULT_THRESHOLD_MISSING,
                 max_str_length: float = DEFAULT_MAX_STR_LENGTH,
                 std_str_length: float = DEFAULT_STD_STR_LENGTH) -> None:

        self.__isdata = isdata
        self.__isindex = isindex

        self.critere_arret = None

        if self.__isdata is None and self.__isindex is None:
            super().__init__(values, threshold_nunique, threshold_missing, 
                             max_str_length, std_str_length)
            self.__infer_type()

        elif self.__isdata is not None and self.__isindex is not None:
            assert self.__isdata == (not self.__isindex), \
                'isdata and isindex should be complementary'
            self.values = values
            self.is_data
            self.is_index

        else:
            self.values = values
            self.is_data
            self.is_index

    def __matmul__(self, other):
        return get_relation(self.values, other.values)

    def __str__(self):
        if self.is_index:
            return 'index'
        if self.is_data:
            return 'data'
        return None
    
    def __repr__(self):
        return self.__str__()

    def __infer_type(self):

        if self.is_float:
            self.__isdata = True
            self.critere_arret = 'Float variable'
            self.is_data

        elif self.is_date and not self.is_int and not self.is_float:
            self.__isdata = True
            self.critere_arret = 'Date variable'
            self.is_data

        elif self.is_int and self.is_cst_length:
            self.__isindex = True
            self.critere_arret = 'Int cst length'
            self.is_index

        elif self.is_missing or self.is_nunique:
            self.__isdata = True
            self.critere_arret = 'missing or unique'
            self.is_data

        elif not self.is_nunique:
            self.__isindex = True
            self.critere_arret = 'not nunique'
            self.is_index

    @property
    def is_data(self):
        return self.__isdata

    @property
    def is_index(self):
        return self.__isindex
    
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

import warnings
import pandas as pd
import numpy as np

warnings.simplefilter(action='ignore', category=UserWarning)

class VariableCalcul:

    def __init__(self, values: pd.Series, threshold_nunique: float, threshold_missing: float,
                 max_str_length: float, std_str_length: float) -> None:

        self.values = values

        self.__threshold_nunique = threshold_nunique
        self.__threshold_missing = threshold_missing
        self.__max_str_length = max_str_length
        self.__std_str_length = std_str_length

        self.lengths = None

        self.d_lengths = self.__get_stat_length()

        self.is_float = self.__is_float_var()

        if not self.is_float :

            self.is_int = self.__is_int_var()
            self.is_nunique = self.__is_nunique()
            self.is_missing = self.__is_missing()
            self.is_cst_length = self.__is_cst_length()
            self.is_date = self.__is_date_var()
            self.is_free_text = self.__is_free_text()

    def __calculate_lengths(self):
        self.lengths = self.values.astype(str).str.len()

    def __get_stat_length(self):

        self.__calculate_lengths()

        d_lengths = {}

        d_lengths['std'] = np.std(self.lengths)
        d_lengths['max'] = np.max(self.lengths)
        d_lengths['mean'] = np.mean(self.lengths)

        return d_lengths

    def __is_cst_length(self):
        if self.d_lengths['std'] == 0:
            return True
        return False

    def __is_float_var(self):
        return self.values.infer_objects().dtype == float

    def __is_int_var(self):
        return self.values.infer_objects().dtype == int

    def __is_nunique(self):
        return (self.values.nunique()/self.values.size) > self.__threshold_nunique

    def __is_missing(self):
        return (self.values.isna().sum()/self.values.size) > self.__threshold_missing

    def __is_date_var(self):
        return pd.to_datetime(self.values, errors='ignore').infer_objects().dtype \
            == 'datetime64[ns]'

    def __is_free_text(self):
        if self.d_lengths['max'] > self.__max_str_length and \
            self.d_lengths['std'] > self.__std_str_length:
            return True
        return False
    
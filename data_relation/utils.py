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

def get_relation(column1: pd.Series, column2: pd.Series):

    column1 = column1.dropna()
    column2 = column2.dropna()

    intersection = set(column1.values).intersection(column2.values)

    if len(intersection) == 0:
        return None

    column1_inclusion = sum([1 for e in column1 if e in intersection])
    column2_inclusion = sum([1 for e in column2 if e in intersection])

    if column1_inclusion == column1.shape[0]:
        cons12 = 'mandatory'
    else:
        cons12 = 'optional'

    if column2_inclusion == column2.shape[0]:
        cons21 = 'mandatory'
    else:
        cons21 = 'optional'

    if column1_inclusion > len(intersection) and column2_inclusion > len(intersection):
        return 'N:M', cons12, cons21
    elif column1_inclusion > len(intersection) and column2_inclusion <= len(intersection):
        return 'N:1', cons12, cons21
    elif column1_inclusion <= len(intersection) and column2_inclusion > len(intersection):
        return '1:N', cons12, cons21
    else:
        return '1:1', cons12, cons21

def true_or_none(b):
    if b:
        return True
    return None

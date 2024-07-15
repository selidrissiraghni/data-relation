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
import pandas as pd
from faker import Faker
import random
from random import randint

if __name__ == '__main__':

    fake=Faker(locale='fr_FR')

    # Generate account table
    def create_account(num_account):
        account=pd.DataFrame()
        for i in range(0,num_account):
            account.loc[i,'user_id']= str(randint(1245968, 9857483))
            account.loc[i,'first_name']=fake.first_name()
            account.loc[i,'last_name']=fake.last_name()
            account.loc[i,'email']=fake.ascii_free_email()
            account.loc[i,'is_verified']=fake.random_element(elements=("yes","no"))
        return account

    # Create 100 account
    acc = create_account(100)

    # Divide into 2 tables for 1:1 relation
    account = acc[['user_id', 'is_verified', 'email']].copy()
    account_personal = acc[['user_id', 'first_name', 'last_name']].copy()

    table_account = Table(account)
    table_account_personal = Table(account_personal)
    
    print(account)
    print(table_account)

    print('-'*50)
    print('-'*50)
    
    print(account_personal)
    print(table_account_personal)

    print('-'*50)
    print('-'*50)

    # Generate Transaction Table
    def transaction(num_trans):
        trans=pd.DataFrame()
        for i in range(0,num_trans):
            trans.loc[i,'transaction_id']= fake.bothify(text='FT#########')
            trans.loc[i,'recipient_bank']=fake.random_element(elements=("Dana","Gopay","LinkAja","Ovo","Shopeepay","BRI","BNI","BSI","BCA",
                                                                    "Mandiri","JAGO","Maybank","Permata","Seabank","Muamalat","BJB"))
            trans.loc[i,'account_number']=fake.aba()
            trans.loc[i,'amount']=fake.random_int(min=10000, max=5000000, step=1000)
            trans.loc[i,'unique_code']=fake.random_int(min=50, max=999)
            trans.loc[i,'transaction_status']=fake.random_element(elements=("Need Confirmation","Checking","Processed","Success","Failed","Cancelled"))
        return trans

    # Generate 1000 transaction 
    trans=transaction(1000)

    # Generate admin fee based on random 0 or 1500
    trans['admin_fee']=random.choices([0,1500],k=len(trans))

    # Generate relational user id in account table and transaction table
    trans['user_id']=random.choices(account["user_id"], k=len(trans))

    table_trans = Table(trans)
    
    print(trans)
    print(table_trans)

    print('-'*50)
    print('-'*50)

    # Generate Payment table
    def payment(num_trans):
        payment=pd.DataFrame()
        for i in range(0,num_trans):
            payment.loc[i,'payment_id']= fake.bothify(text='FP#####')
            payment.loc[i,'payment_method']=fake.random_element(elements=("BCA","BNI","BRI","BSI","CIMB","Danamon","Digibank","Mandiri","Muamalat","Permata","Jenius"))
            payment.loc[i,'account_number']=fake.aba()
            payment.loc[i,'payment_status']=fake.random_element(elements=("Success","Failed","Cancelled"))
        return payment

    # Generate 1000 payment process
    pay=payment(1000)
    
    # Generate relational transaction id in trans table and payment table
    pay['transaction_id']=random.choices(trans["transaction_id"], k=len(pay))

    table_pay = Table(pay)

    print(pay)
    print(table_pay)

    print('-'*50)
    print('-'*50)

    print(table_account.get_relations_by_name(table_account_personal))
    print(table_account.get_relations_by_name(table_trans))
    print(table_trans.get_relations_by_name(table_pay))
    print(table_account.get_relation_two_columns(table_account_personal, left_on='user_id', right_on='user_id'))

    
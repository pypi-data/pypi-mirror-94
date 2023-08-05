
# 추후 ORM으로 대체
import pandas as pd
import shutil
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from .config import MDB, PROJECTDB_TABLES, DATETIME_FIELDS


################################################################################################################################
## Basic ORMs
################################################################################################################################

################################################################
## show tables
################################################################
def list_tables(DB):
    return DB.table_names()


################################################################
## read table
################################################################
def read_table(DB, table_name=None):
    '''
    sqlite 자료형 한정적으로, 자료형 유지하며 table 읽기 위해 사용하는 함수
    table_name 입력하지 않으면 DB에 존재하는 table의 이름을 pring하고 None 반환
    
    params
      DB
      table_name
    
    return
      table <pd.DataFrame>
    '''
    
    # list tables if table_name is not given
    if table_name is None:
        print(f"Please select a table! - {DB.table_names()}")
        return
    
    # read table
    tbl = pd.read_sql_table(table_name, DB)
    
    # for pandas+sqlite datetime type consistency
    for field in [field for field in tbl.columns if field in DATETIME_FIELDS]:
        tbl[field] = tbl[field].astype(str)
        
    # for pandas+sqlite Null consistency
    tbl = tbl.replace(['None'], [None])
    
    # for pandas+sqlite int type consistency
    for c in tbl.filter(like='n_').columns:
        tbl[c] = tbl[c].astype(int)
    
    return tbl


################################################################
## update sqlite table
################################################################
def update_table(DB, table_name, df, key):
    '''
    update table value by value (insert if key not exists)
    key는 table과 df 양쪽에 모두 포함되어 있어야 함
    
    params
      DB           sqlalchemy database engine
      table_name   table name in database
      df           dataframe to update
      key          primary key - field name of df
      
    return
      (void)
    '''
    
    # set key as index
    df_ = df.set_index(key)
    
    # update value by value
    with DB.connect() as conn:
        for k in df_.index:
            _k_ = f"__{k}__" if type(k) is str else k
            query = f"SELECT {key} FROM {table_name} WHERE {key} == {_k_};".replace("__", "'")
            
            # insert data if key is not in table
            if conn.execute(query).fetchone() is None:
                
                # insert key
                query = f"INSERT INTO {table_name} ({key}) VALUES ({_k_});".replace("__", "'")
                conn.execute(query)
            
            # update data if key is in table
            for field in df_.columns:
                value = df_.at[k, field]
                value = f"__{value}__" if type(value) is str else value
                query = f"UPDATE {table_name} SET {field} = {value} WHERE {key} = {_k_};".replace("__", "'")
                conn.execute(query)

                
################################################################
## delete rows
################################################################
def delete_rows(DB, table_name, delete_dict):
    '''
    Delete rows from database table.
    
    delete_dict = {
        <field1>: [value1, value2, value3, ...],
        <field2>: [valuea, valueb, ...],
    }
    '''
    
    with DB.connect() as conn:
        for field, values in delete_dict.items():
            if type(values) is not list:
                values = [values]
            for value in values:
                conn.execute(f"DELETE FROM {table_name} WHERE {field} = '{value}'")
                
################################################################
## delete table
################################################################
def create_table(DB, table_name, table_dict, verbose=False):
    '''
    Create new table.
    
    table_dict = {
        'field1': {
            dtype: 'INTEGER',
            key: 'PRIMARY KEY AUTOINCREMENT'
        },
        'field2': {
            dtype: 'TEXT'
        }
        'field3': {
            dtype: 'CHARACTER'
        }
    }
    '''
    fields = []
    for field, values in table_dict.items():
        words = []
        words.append(field)
        words.append(values['dtype'])
        if 'key' in values.keys():
            words.append(values['key'])
        words = ' '.join(words)
        fields.append(words)
    fields = ', '.join(fields)
    query = f"CREATE TABLE {table_name} ({fields});"
    
    if verbose:
        print(query)
        
    with DB.connect() as conn:
        DB.execute(query)

                
################################################################################################################################
## FOR PROJECT
################################################################################################################################        

################################################################
## init database
################################################################
def init_database(DB, forced=False):
    '''
    database 없을 경우 생성
    
    params
      DB         <sqlalchemy.engine.base.Engine>
      forced     기존 database를 삭제 후 다시 생성
      
    return
      (void)
    '''    
    db_name = str(DB.url).rsplit('/', 1)[-1].replace('.db', '')
    print(f"Initialize {db_name} database.")
    
    # initiate or load database
    if not database_exists(DB.url):
        create_database(DB.url)
        print("  - new database created.")
    else:
        if forced:
            # backup & remove current database
            db_path = str(DB.url).replace('sqlite:///', '')
            bak_path = db_path.replace('.db', f'_{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}.db')
            shutil.move(db_path, bak_path)
            print(f"  - current {db_name} database is removed by force.")
            print(f"  - old database is backed up before removed '{bak_path}'.")
        else:
            print(f"  - database already exists.")

    # initiate tables
    n_tables_initiated = 0 
    for table_name, table_dict in PROJECTDB_TABLES.items():
        if not DB.has_table(table_name):
            create_table(DB, table_name, table_dict)
            print(f"  - table '{table_name}' initiated.")
            n_tables_initiated += 1
    
    # nothing changed
    if n_tables_initiated == 0:
        print(f"  - All tables ({', '.join(DB.table_names())}) are already exists.")
        
    # line break
    print('')

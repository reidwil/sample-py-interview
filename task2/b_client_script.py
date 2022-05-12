# It is highly encouraged to not put your snowflake password in plain text
# Instead you should save your password as an environment variable
# You can reference an env var in python using os.environ.get()
# Read more here: https://docs.python.org/3/library/os.html#os.environ

import os
import sys
from snowflake.connector.connection import SnowflakeConnection
from a_main_script import main

csv_file_path = sys.argv[1]
fully_qualified_table_name = sys.argv[2]

def create_snowflake_connections(user, password, account, **kwargs):
    return SnowflakeConnection(user=user, password=password, account=account, **kwargs)

conn = create_snowflake_connections(
    user=os.environ.get('SNOWFLAKE_USERNAME'),
    password=os.environ.get('SNOWFLAKE_PASSWORD'),
    account=os.environ.get('SNOWFLAKE_ACCOUNT'),
)

if __name__=='__main__':
    main(conn, fully_qualified_table_name, csv_file_path)
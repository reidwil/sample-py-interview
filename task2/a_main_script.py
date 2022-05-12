import os
import gzip
import shutil
import snowflake.connector

from os import PathLike
from typing import List, Union
from snowflake.connector.connection import SnowflakeConnection


class Snowflake(SnowflakeConnection):
    def __init__(self, SnowflakeConnection):
        self.conn = SnowflakeConnection
        self.engine = snowflake.connector.connect(
            user=self.conn.user,
            password=self.conn.password,
            account=self.conn.account,
        )

    def _run(self, sql: str):
        with self.engine.cursor() as cur:
            cur.execute(sql)

    def _cwd(self):
        return os.path.dirname(os.path.abspath(__file__))

    def stage_file(self, file_name: Union[PathLike, None], table_name: str):
        # Error handling remove leading '/' from filename
        if file_name.startswith('/'):
            full_file_name = self._cwd() + file_name[1:]
        else:
            full_file_name = self._cwd() + file_name

        stage_sql = f"PUT file:///{full_file_name} @%{table_name}_tmp"
        self._run(stage_sql)

    def copy_into(self, table_name: str = None):
        copy_sql = f"copy into {table_name} from @{table_name}_tmp"
        self._run(copy_sql)

def compress(file: str):
    # Snowflake doesn't like large files so we should compress
    # https://docs.snowflake.com/en/user-guide/data-load-considerations-prepare.html#general-file-sizing-recommendations
    # Taken from https://docs.python.org/3/library/gzip.html#examples-of-usage
    with open(file, 'rb') as f_in:
        with gzip.open(os.path.join(file, '.gz'), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def load_csvs_to_snowflake_table(
    conn: snowflake.connector.connection.SnowflakeConnection,
    fully_qualified_table_name: str,
    csv_file_paths: List[str],
):

    with Snowflake(conn) as snowflake:
        # We could thread right here to copy multiple files
        for file in csv_file_paths:
            compressed_file = compress(file)
            print(f"Copying {file=} into {fully_qualified_table_name}")
            snowflake.stage_file(compressed_file, fully_qualified_table_name)
            snowflake.copy_into(fully_qualified_table_name)

def main():
    load_csvs_to_snowflake_table(
        conn,
        fully_qualified_table_name,
        csv_file_paths
    )

if __name__=='__main__':
    main()
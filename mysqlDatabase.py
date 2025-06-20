import mysql.connector
import logging
import traceback

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler()]  # 输出到控制台
)


class mysql_connection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            logging.info("MySQL connection is closed")

    def isNotRepetitive(self, table_name, column, value):
        query = f"SELECT * FROM {self.database}.{table_name} WHERE {column} LIKE {value}"
        # print(query)
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            if len(result) == 0:
                return True
            else:
                return False

        except Exception as e:
            logging.error(e)
            traceback.print_exc()

    def insert(self, table_name, **kwargs):
        columns = tuple(kwargs.keys())
        values = tuple(kwargs.values())

        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))

        query = f"INSERT INTO {self.database}.{table_name} ({columns_str}) VALUES ({placeholders})"

        logging.info(f"Executing query: {query} with values: {values}")
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
            self.connection.rollback()

    def insert_many(self, table_name, columns: tuple, values: list):
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))

        query = f"INSERT INTO {self.database}.{table_name} ({columns_str}) VALUES ({placeholders})"
        try:
            self.cursor.executemany(query, values)
            self.connection.commit()
            logging.info("Batch insert data")
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
            self.connection.rollback()

    def clear_table(self, table_name):
        query = f"TRUNCATE TABLE {self.database}.{table_name}"
        try:
            self.cursor.execute(query)
            self.connection.commit()
            logging.info("Table cleared")
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
            self.connection.rollback()

    def delete_row(self, table_name, **condition):
        placeholders = ' AND '.join(['{} = %s'.format(key) for key in condition.keys()])
        query = f'DELETE FROM {self.database}.{table_name} WHERE ' + placeholders
        print(query)
        try:
            self.cursor.execute(query, tuple(condition.values()))
            self.connection.commit()
            logging.info("delete row successful")
        except Exception as e:
            logging.error(e)
            traceback.print_exc()
            self.connection.rollback()

import sqlite3
from sqlite3 import Error
import json

class SqliteConn:
    def __init__(self):
        self.conn = None

    def create_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            self.conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
        except Error as e:
            print(e)
            raise

    '''
    def select_rows_from_table(self, table_name):
        cur = self.conn.cursor()
        statement = "SELECT * FROM " + table_name
        print("Executing: " + statement)
        cur.execute(statement)
        rows = cur.fetchall()
        for row in rows:
            yield row
    '''

    def select_rows_from_table(self, table_name, condition=None, json_str=False):
        cur = self.conn.cursor()
        statement = "SELECT * FROM " + table_name
        if condition:
            statement = statement + " WHERE " + condition
        print("Executing: " + statement)
        rows = cur.execute(statement)
        if json_str:
            return json.dumps( [dict(ix) for ix in rows] ) #Create JSON string

        return rows

    def close(self):
        if self.conn:
            self.conn.close()

def main():
    database = r"../test/resources/2node_plan.db"
    sqlConn = SqliteConn()
    sqlConn.create_connection(database)
    print("1. Getting Nodes\n")
    for row in sqlConn.select_rows_from_table("Nodes"):
        print(row)
        print(type(row))
    print("\n2. Getting NetIntInterfaces of a particular Node\n")
    for row in sqlConn.select_rows_from_table("NetIntInterfaces", '''Node="XR-Emul-1"'''):
        print(row)
        print(type(row))
    print("\n3. Getting Nodes as JSON\n")
    data = sqlConn.select_rows_from_table("Nodes", None, True)
    print(data)
    print(type(data))
    print("\n4. Getting NetIntInterfaces of a particular Node as JSON\n")
    data = sqlConn.select_rows_from_table("NetIntInterfaces", '''Node="XR-Emul-1"''', True)
    print(data)
    print(type(data))
    sqlConn.close()

if __name__ == '__main__':
    main()

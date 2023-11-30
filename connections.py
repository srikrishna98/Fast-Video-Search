import psycopg2

class DbConnect:
    def __init__(self, db_info):
        self.db_info = db_info
        self.table_name = self.db_info['table_name']
        self.conn_str = "dbname='{db_name}' user='{db_user}' host='{db_host}' password='{db_password}'".format(
                        db_name=self.db_info['db_name'],
                        db_user=self.db_info['db_user'],
                        db_host=self.db_info['db_host'],
                        db_password=self.db_info['db_password']
        )
        self.conn = None
        
    def connect_to_db(self):
        """Connect to the postgres instance.
        """
        self.conn = psycopg2.connect(self.conn_str)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
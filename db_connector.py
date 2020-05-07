import sqlite3
from sqlite3 import Error

class RedditDB:
    def __init__(self, db):
        self.conn = self.create_connection(db)
        self.init_tables()

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(f'sqlite3 {sqlite3.version}')
        except Error as e:
            print(e)
        return conn

    def init_tables(self):
        sql_create_comments_table = """ CREATE TABLE IF NOT EXISTS comments (
                                            id TEXT NOT NULL PRIMARY KEY,
                                            url TEXT NOT NULL,
                                            title TEXT NOT NULL,
                                            date TEXT NOT NULL
                                        ); """
        # create comments table
        self.create_table(sql_create_comments_table)

    def create_table(self, create_table_sql):
        """ 
        create a table from the create_table_sql statement
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            self.conn.commit()
        except Error as e:
            print(e)

    def create_comment(self, comment):
        """
        Create a new comment into the comments table
        """
        sql = ''' INSERT INTO comments(id,url,title,date)
                VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, comment)
        self.conn.commit()
        return cur.lastrowid

    def select_all_comments(self):
        """
        Query all rows in the comments table
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM comments")
        rows = cur.fetchall()
        return rows

    def comment_exists(self, comment_id):
        """
        Check if comment already exists in table
        """
        cur = self.conn.cursor()
        sql = f"SELECT EXISTS(SELECT 1 FROM comments WHERE id='{comment_id}');"
        cur.execute(sql)
        comment_found = cur.fetchone()
        return comment_found[0]

    def select_comment(self, comment_id):
        """
        Query for comment by id
        """
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM comments WHERE id='{comment_id}';")
        comment_row = cur.fetchone()
        return comment_row

        
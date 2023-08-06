import sqlite3

class lite:
    def __init__(self, database, connection, cursor):
        self.database = database
        self.connection = connection
        self.cursor = cursor
        self.dbd()
        self.cursors()

    def dbd(self):
        self.connection = sqlite3.connect(f'{self.database}')

    def cursors(self):
        self.cursor = self.connection.cursor()

    def execute(self, table, columns):
        c = self.cursor

        for i in columns:
            k = len(i)

        quest_len = len(columns)

        global nums
        nums = quest_len

        if type(columns) == list:

            def stringer():
                var = ','.join(columns)
                return var

            try:
                c.execute(f'CREATE TABLE {table} ( {stringer()} )')
                self.connection.commit()
            except:
                pass

    def insert(self, table, rows):
        c = self.cursor

        def quest():
            for uni in range(1, nums):
                l = '? ' * (uni + 1)
            val = l.split(' ')
            val = ','.join(val)
            val = val.split(',')
            val.pop()
            val = ','.join(val)
            return val

        if type(rows) == list:
            c.executemany(f'INSERT INTO {table} VALUES ({quest()})', rows)
            self.connection.commit()
        else:
            c.execute(f'INSERT INTO {table} VALUES {rows}')
            self.connection.commit()

    def fetchone(self, table):
        c = self.cursor
        c.execute(f'SELECT * FROM {table}')
        self.connection.commit()
        return c.fetchone()

    def fetchmany(self, table, amount):
        c = self.cursor
        c.execute(f'SELECT * FROM {table}')
        self.connection.commit()
        return c.fetchmany(amount)

    def fetchall(self, table):
        c = self.cursor
        c.execute(f'SELECT * FROM {table}')
        self.connection.commit()
        return c.fetchall()

    def id_fetchone(self, table):
        c = self.cursor
        c.execute(f'SELECT rowid, * FROM {table}')
        self.connection.commit()
        return c.fetchone()

    def id_fetchmany(self, table, amount):
        c = self.cursor
        c.execute(f'SELECT rowid, * FROM {table}')
        self.connection.commit()
        return c.fetchmany(amount)

    def id_fetchall(self, table):
        c = self.cursor
        c.execute(f'SELECT rowid, * FROM {table}')
        return c.fetchall()

    def find_one(self, table):
        c = self.cursor
        c.execute(f'SELECT rowid, * FROM {table}')
        self.connection.commit()
        return c.fetchone()

    def find_many(self, table, amount):
        c = self.cursor
        c.execute(f'SELECT rowid, * FROM {table}')
        self.connection.commit()
        return c.fetchmany(amount)

    def find_all(self, table, col, ope, query):
        c = self.cursor

        def colly():
            return col

        def quer():
            return query

        c.execute(f'SELECT * FROM {table} WHERE {colly()} {ope} "{quer()}" ')
        self.connection.commit()
        return c.fetchall()

    def find_like_start(self, table, col, query):
        c = self.cursor

        def colly():
            return col

        def quer():
            return query

        c.execute(f'SELECT * FROM {table} WHERE {colly()} LIKE "{quer()}%" ')
        self.connection.commit()
        return c.fetchall()

    def find_like_end(self, table, col, query):
        c = self.cursor

        def colly():
            return col

        def quer():
            return query

        c.execute(f'SELECT * FROM {table} WHERE {colly()} LIKE "%{quer()}" ')
        self.connection.commit()
        return c.fetchall()

    def find_like_any(self, table, col, query):
        c = self.cursor

        def colly():
            return col

        def quer():
            return query

        c.execute(f'SELECT * FROM {table} WHERE {colly()} LIKE "%{quer()}%" ')
        self.connection.commit()
        return c.fetchall()

    def find_no_query(self, table, lis):
        c = self.cursor
        c.execute(f'SELECT * FROM {table} WHERE {lis}')
        self.connection.commit()
        return c.fetchall()

    def update(self, table, col, query, col2, query2):
        c = self.cursor

        def qu():
            return query

        def quq():
            return query2

        if col2 == 'rowid':
            c.execute(f'UPDATE {table} SET {col} = "{qu()}" WHERE rowid = {quq()}')
            self.connection.commit()
        elif type(col2) == str:
            c.execute(f'UPDATE {table} SET {col} = "{qu()}" WHERE "{col2}" = "{quq()}"')
            self.connection.commit()

    def delete(self, table, what):
        c = self.cursor

        if type(what) == tuple:
            c.execute(f'DELETE from {table} WHERE {what[0]} {what[1]} "{what[2]}"')
            self.connection.commit()
        elif type(what) == int:
            c.execute(f'DELETE from {table} WHERE rowid = {what}')
            self.connection.commit()
        elif type(what) == str:
            c.execute(f'DELETE from {table} WHERE {what}')
        else:
            pass

    def order(self, table, order, number=None):
        c = self.cursor
        if order == 'D':
            if number != None:  # not None:
                c.execute(f'SELECT rowid, * FROM {table} ORDER BY rowid DESC LIMIT {number}')
                prod = c.fetchall()
                self.connection.commit()
            else:
                c.execute(f'SELECT rowid, * FROM {table} ORDER BY rowid DESC')
                prod = c.fetchall()
                self.connection.commit()

        elif order == 'A':
            if number != None:
                c.execute(f'SELECT rowid, * FROM {table} ORDER BY rowid ASC LIMIT {number}')
                prod = c.fetchall()
                self.connection.commit()
            else:
                c.execute(f'SELECT rowid, * FROM {table} ORDER BY rowid ASC')
                prod = c.fetchall()
                self.connection.commit()

        elif type(order) == list:
            if order[1] == 'D':
                order[1] = 'DESC'
            elif order[1] == 'A':
                order[1] = 'ASC'
            if number != None:
                c.execute(f'SELECT rowid, * FROM {table} ORDER BY {order[0]} {order[1]} LIMIT {number}')
                prod = c.fetchall()
                self.connection.commit()
            else:
                c.execute(f'SELECT rowid, * FROM {table} ORDER BY {order[0]} {order[1]}')
                prod = c.fetchall()
                self.connection.commit()
        return prod

    def limit(self, table, number):
        c = self.cursor
        c.execute(f'SELECT * FROM {table} LIMIT {number}')
        self.connection.commit()
        return c.fetchall()

    def id_limit(self, table, number):
        c = self.cursor
        c.execute(f'SELECT rowid, * FROM {table} LIMIT {number}')
        self.connection.commit()
        return c.fetchall()

    def drop_table(self, table):
        c = self.cursor
        c.execute(f'DROP TABLE {table}')
        self.connection.commit()

    def close(self):
        self.connection.close()

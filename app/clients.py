import os
import json
import uuid
from sqlite3.dbapi2 import Connection, Error
import sqlite3
import sys
from typing import List
from app.book.book_models import Book

# =================================================================================================================
##################################################    CLIENT   ##################################################
# =================================================================================================================


class Client:
    def __init__(self) -> None:
        pass

    def find() -> List[Book]:
        pass

    def findOne(id) -> Book:
        pass

    def delete(id) -> bool:
        pass

    def update(book: Book) -> bool:
        pass

    def create(book: Book) -> Book:
        pass

# =================================================================================================================
##################################################    JsonClient   ##################################################
# =================================================================================================================


class JsonClient(Client):
    def __init__(self, file_path) -> None:
        self.model_name = 'books'
        self.cache = dict()

        if os.path.exists(file_path):
            self.file_path = file_path
            self._load()
        else:
            sys.exit("Error the file does not exist")

    def _load(self) -> None:
        with open(self.file_path, 'r') as file:
            self.cache = json.load(file)

            if not self.model_name in self.cache:
                self.cache[self.model_name] = []

    def _save(self) -> None:
        with open(self.file_path, 'w') as outfile:
            json.dump(self.cache, outfile)

    def create(self, book: Book) -> Book:
        id = uuid.uuid1()
        book['isbn'] = id.int
        self.cache[self.model_name].append(book)
        self._save()
        return book

    def update(self, book: Book) -> bool:
        data = self.find()
        for i in range(len(data)):
            if data[i]['isbn'] == str(book['isbn']):
                self.cache[self.model_name][i] = book
                self._save()
                return True
        return False

    def find(self) -> List[Book]:
        if not self.cache or len(self.cache[self.model_name]) == 0:
            self._load()
        return list(self.cache[self.model_name])

    def findOne(self, isbn) -> Book:
        data = self.find()
        for i in range(len(data)):
            if data[i]['isbn'] == str(isbn):
                return data[i]

    def delete(self, isbn) -> bool:
        data = self.find()
        for i in range(len(data)):
            if data[i]['isbn'] == str(isbn):
                self.cache[self.model_name].pop(i)
                self._save()
                return True
        return False

# =================================================================================================================
##################################################    SQLiteClient   ##################################################
# =================================================================================================================


class SQLiteClient(Client):
    def __init__(self, file_path) -> None:
        # create a database connection
        self.conn = self._create_connection(file_path)

        # init book sql script
        sql_create_bookstable = """ CREATE TABLE IF NOT EXISTS books (
                                        isbn integer PRIMARY KEY,
                                        title text NOT NULL,
                                        subtitle text,
                                        author text NOT NULL,
                                        published text NOT NULL,
                                        publisher text NOT NULL,
                                        pages integer NOT NULL,
                                        description text NOT NULL,
                                        website text
                                    ); """

        # create books table
        self._create_table(sql_create_bookstable)

    def _create_connection(self, db_file) -> Connection:
        """ create a database connection to a SQLite database """

        conn = None
        try:
            if os.path.exists(db_file):
                conn = sqlite3.connect(db_file)
            else:
                print("Error! the file does not exist")

            print(sqlite3.version)

        except Error as e:
            sys.exit(e)

        return conn

    def _create_table(self, script) -> None:
        """ create a table from the create_table_sql statement """
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute(script)
            except Error as e:
                print(e)
        else:
            print("Error! cannot create the database connection.")

    def _execute(self, sql, data=None):
        """ Create a new data into table """
        try:
            with self.conn:
                cur = self.conn.cursor()
                if data:
                    cur.execute(sql, data)
                    self.conn.commit()
                else:
                    cur.execute(sql)
                return cur
            return None
        except Error as e:
            print(e)

    def _book_format(self, data) -> Book:
        book = {}
        book['isbn'] = data[0]
        book['title'] = data[1]
        book['subtitle'] = data[2]
        book['author'] = data[3]
        book['published'] = data[4]
        book['publisher'] = data[5]
        book['pages'] = data[6]
        book['description'] = data[7]
        book['website'] = data[8]

        return book

    def create(self, book: Book) -> Book:
        """ Create a new book into the books table """

        sql = ''' INSERT INTO books(title, subtitle, author, published, publisher, pages, description, website)
                  VALUES(?,?,?,?,?,?,?,?) '''

        book_data = (book['title'], book['subtitle'], book['author'], book['published'],
                     book['publisher'], book['pages'], book['description'], book['website'])
        book_id = self._execute(sql, book_data).lastrowid

        with book_id:
            book['isbn'] = book_id
            return book

        return None

    def update(self, book: Book) -> bool:
        """ Update a book into the books table """

        if bool(book['isbn']):
            sql = ''' UPDATE books 
                    SET title = ? , 
                        subtitle = ? , 
                        author = ? , 
                        published = ? , 
                        publisher = ? , 
                        pages = ? , 
                        description = ? , 
                        website = ? 
                    WHERE isbn = ?'''

            book_data = (book['title'], book['subtitle'], book['author'], book['published'],
                         book['publisher'], book['pages'], book['description'], book['website'], book['isbn'])

            self._execute(sql, book_data)

            return True
        return False

    def delete(self, isbn) -> bool:
        """ Delete a book by task isbn """

        sql = 'DELETE FROM books WHERE isbn=?'

        self._execute(sql, (isbn,))

        return True

    def find(self) -> List[Book]:
        """ Query all rows in the books table """

        sql = 'SELECT * FROM books'

        cur = self._execute(sql)

        rows = cur.fetchall()

        data = []
        for row in rows:
            book = self._book_format(row)
            data.append(book)

        return data

    def findOne(self, isbn) -> Book:
        """ Query books by isbn """

        sql = 'SELECT * FROM books WHERE isbn=?'

        cur = self._execute(sql, (isbn,))

        rows = cur.fetchall()

        if len(rows):
            book = self._book_format(rows[0])
            return book
        else:
            return None

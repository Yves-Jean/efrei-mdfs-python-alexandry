from app.db import Database
from app.clients import SQLiteClient

if __name__ == "__main__":
    client = SQLiteClient('./storage/database.sqlite')

    db = Database(client)

    db1 = Database(client)

    if id(db) == id(db1):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")

    books = db.get_client().find()
    print(books)

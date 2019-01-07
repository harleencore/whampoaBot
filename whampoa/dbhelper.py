import sqlite3

class DBHelper:

    # just takes a db name and creates a db connection
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # creates a new table called items in the db
    # it has one column, description
    def setup(self):
        print("creating table")
        stmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        self.conn.execute(stmt)
        self.conn.commit()

    # takes the text for the item and inserts it into the db table
    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    # takes the text for an item and removes it from the database
    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner )
        self.conn.execute(stmt, args)
        self.conn.commit()

    # returns a list of all items in our database
    # use a list comprehension to take the first element of each item
    # SQLite will always return data in tuple format, even when there is only
    # one column
    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]

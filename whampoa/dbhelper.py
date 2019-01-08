import sqlite3

class DBHelper:

    # just takes a db name and creates a db connection
    def __init__(self, dbname="feedback.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # creates a new table called items in the db
    # it has one column, description
    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text, kid_name text)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    # takes the text for the item and inserts it into the db table
    def add_item(self, item_text, owner, kid_name):
        stmt = "INSERT INTO items (description, owner, kid_name) VALUES (?, ?, ?)"
        args = (item_text, owner, kid_name)
        self.conn.execute(stmt, args)
        self.conn.commit()

    # takes the text for an item and removes it from the database
    def delete_item(self, item_text, owner, kid_name):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?) AND kid_name = (?)"
        args = (item_text, owner, kid_name)
        self.conn.execute(stmt, args)
        self.conn.commit()

    # returns a list of all items in our database
    # use a list comprehension to take the first element of each item
    # SQLite will always return data in tuple format, even when there is only
    # one column
    def get_items(self, owner, kid_name):
        stmt = "SELECT description FROM items WHERE owner = (?) AND kid_name = (?)"
        args = (owner, kid_name)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_kids(self, owner, kid_name):
        stmt = "SELECT kid_name FROM items WHERE kid_name = (?)"
        args = (owner, kid_name)
        return [x[0] for x in self.conn.execute(stmt, args)]

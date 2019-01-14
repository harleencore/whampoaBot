import sqlite3

class DBHelper:

    # just takes a db name and creates a db connection
    def __init__(self, dbname="whampoa.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # creates a new table called feedback in the db
    # it has  columns, observations, owner, child, subject
    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS feedback (observations text, owner text, child text, subject text)"
        # adding indexing
        feedbackidx = "CREATE INDEX IF NOT EXISTS feedbackIndex ON feedback (observations ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON feedback (owner ASC)"
        self.conn.execute(tblstmt) # create the table
        self.conn.execute(feedbackidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    # takes the text for the feedback and inserts it into the db table
    def add_feedback(self, feedback_text, owner, child, subject):
        stmt = "INSERT INTO feedback (observations, owner, child, subject) VALUES (?, ?)"
        args = (feedback_text, owner, child, subject)
        self.conn.execute(stmt, args)
        self.conn.commit()

    # removing delete function temporarily
    # # takes the text for an feedback and removes it from the database
    # def delete_feedback(self, feedback_text, owner):
    #     stmt = "DELETE FROM feedback WHERE observations = (?) AND owner = (?)"
    #     args = (feedback_text, owner )
    #     self.conn.execute(stmt, args)
    #     self.conn.commit()

    # check syntax
    def get_feedback(self, owner, child, subject):
        stmt = "SELECT observations FROM feedback WHERE owner = (?) AND child = (?) AND subject = (?)"
        args = (owner, child, subject, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_kids(self, owner, child):
        stmt = "SELECT child FROM feedback WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]

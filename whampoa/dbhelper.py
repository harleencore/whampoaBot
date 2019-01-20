import sqlite3

class DBHelper:

    # just takes a db name and creates a db connection
    def __init__(self, dbname="whampoa.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # creates a new table called feedback in the db
    # it has  columns: observations, owner, children, subjects
    def setup(self):
        # tblstmt = "CREATE TABLE IF NOT EXISTS feedback (observations text, owner text, children text, subjects text)"
        # # adding indexing
        # feedbackidx = "CREATE INDEX IF NOT EXISTS feedbackIndex ON feedback (observations ASC)"
        # ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON feedback (owner ASC)"
        #
        # self.conn.execute(tblstmt) # create the table
        # self.conn.execute(feedbackidx)
        # self.conn.execute(ownidx)
        # self.conn.commit()

        tblstmt_children = "CREATE TABLE IF NOT EXISTS children_table (children text, owner text)"
        feedbackidx_children = "CREATE INDEX IF NOT EXISTS childrenIndex ON children_table (children ASC)"
        ownidx_children = "CREATE INDEX IF NOT EXISTS ownIndex_children ON children_table (owner ASC)"

        self.conn.execute(tblstmt_children)
        self.conn.execute(feedbackidx_children)
        self.conn.execute(ownidx_children)
        self.conn.commit()

    # # takes the text for the feedback and inserts it into the db table
    # def add_feedback(self, feedback_text, owner, children, subjects):
    #     stmt = "INSERT INTO feedback (observations, owner, children, subjects) VALUES (?, ?)"
    #     args = (feedback_text, owner, children, subjects)
    #     self.conn.execute(stmt, args)
    #     self.conn.commit()
    #
    # # removing delete function temporarily
    # # # takes the text for an feedback and removes it from the database
    # # def delete_feedback(self, feedback_text, owner):
    # #     stmt = "DELETE FROM feedback WHERE observations = (?) AND owner = (?)"
    # #     args = (feedback_text, owner )
    # #     self.conn.execute(stmt, args)
    # #     self.conn.commit()
    #
    # # check syntax
    # def get_feedback(self, owner, children, subjects):
    #     stmt = "SELECT observations FROM feedback WHERE owner = (?) AND children = (?) AND subjects = (?)"
    #     args = (owner, children, subjects, )
    #     return [x[0] for x in self.conn.execute(stmt, args)]
    #
    # def get_children(self, owner):
    #     stmt = "SELECT children FROM feedback WHERE owner = (?)"
    #     args = (owner, )
    #     return [x[0] for x in self.conn.execute(stmt, args)]
    #
    # def get_subjects(self, owner, kid):
    #     stmt = "SELECT subjects FROM feedback WHERE owner = (?) AND children = (?)"
    #     args = (owner, )
    #     return [x[0] for x in self.conn.execute(stmt, args)]

    def get_children(self, owner):
        stmt = "SELECT children from children_table WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    def add_child(self, children, owner):
        stmt = "INSERT INTO children_table(children, owner) VALUES (?, ?)"
        args = (children, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

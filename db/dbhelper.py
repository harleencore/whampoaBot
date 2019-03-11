import sqlite3



class DBHelper:

    token = "679424726:AAFhyVf602gZxaS0pEIfyiVwqOA7KASWbmw"
    password = "learningisfunandexciting"

    # just takes a db name and creates a db connection
    def __init__(self, dbname="whampoa.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # creates a new table called feedback in the db
    # it has  columns: observations,  children, subjects
    def setup(self):
        ##### FIGURE OUT FOREIGN KEYS!!!
        tblstmt = "CREATE TABLE IF NOT EXISTS feedback (observations text, children text, subjects text)"
        # adding indexing
        feedbackidx = "CREATE INDEX IF NOT EXISTS feedbackIndex ON feedback (observations ASC)"

        self.conn.execute(tblstmt) # create the table
        self.conn.execute(feedbackidx)
        self.conn.commit()

        tblstmt_children = "CREATE TABLE IF NOT EXISTS children_table (children text)"
        feedbackidx_children = "CREATE INDEX IF NOT EXISTS childrenIndex ON children_table (children ASC)"

        self.conn.execute(tblstmt_children)
        self.conn.execute(feedbackidx_children)
        self.conn.commit()

        tblstmt_volunteers = "CREATE TABLE IF NOT EXISTS volunteers_table (volunteers numeric)"
        volunteeridx = "CREATE INDEX IF NOT EXISTS volunteerIndex ON volunteers_table (volunteers ASC)"

        self.conn.execute(tblstmt_volunteers)
        self.conn.execute(volunteeridx)
        self.conn.commit()

    # takes the text for the feedback and inserts it into the db table
    def add_feedback(self, feedback_text, children, subjects):
        stmt = "INSERT INTO feedback (observations, children, subjects) VALUES (?, ?, ?)"
        args = (feedback_text, children, subjects)
        self.conn.execute(stmt, args)
        self.conn.commit()
    #
    # # removing delete function temporarily
    # # # takes the text for an feedback and removes it from the database
    # # def delete_feedback(self, feedback_text, owner):
    # #     stmt = "DELETE FROM feedback WHERE observations = (?) AND owner = (?)"
    # #     args = (feedback_text, owner )
    # #     self.conn.execute(stmt, args)
    # #     self.conn.commit()
    #
    # check syntax
    def get_feedback(self, children, subjects):
        stmt = "SELECT observations FROM feedback WHERE children = (?) AND subjects = (?)"
        args = (children, subjects )
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_all_feedback(self, children):
        stmt = "SELECT observations FROM feedback children = (?)"
        args = (children, )
        return [x[0] for x in self.conn.execute(stmt, args)]


    def get_children(self):
        stmt = "SELECT children from children_table"
        return [x[0] for x in self.conn.execute(stmt)]

    def add_child(self, children):
        stmt = "INSERT INTO children_table(children) VALUES (?)"
        args = (children,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_volunteers(self):
        stmt = "SELECT volunteers FROM volunteers_table"
        return [x[0] for x in self.conn.execute(stmt)]

    def add_volunteer(self, volunteers):
        stmt = "INSERT INTO volunteers_table(volunteers) VALUES (?)"
        args = (volunteers,)
        self.conn.execute(stmt, args)
        self.conn.commit()

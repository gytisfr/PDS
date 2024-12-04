#I genuinely hate this stupid stupid database thing
#Who let SQL Exist, it works like it was invented 300 years ago
#a woi jse ujgiugs igseiufhiifuwa ofahu

import sqlite3, os

os.chdir(os.getcwd())

class interact:
    def __init__(self, db):
        self.db = db
        super().__init__()
        #"solitary" or "ban" for db

    def insert(self, userid, time):
        conn = sqlite3.connect("db")
        c = conn.cursor()
        
        c.execute(f"INSERT INTO {self.db} VALUES({userid}, '{time}')")
        
        conn.commit()
    
    def update(self, userid, time):
        conn = sqlite3.connect("db")
        c = conn.cursor()
        
        c.execute(f"UPDATE {self.db} SET time = '{time}' WHERE userid = {userid}")

        conn.commit()

    def remove(self, userid):
        conn = sqlite3.connect("db")
        c = conn.cursor()
        
        c.execute(f"DELETE FROM {self.db} WHERE userid = {userid}")
        
        conn.commit()
    
    def get(self, userid):
        conn = sqlite3.connect("db")
        c = conn.cursor()
        
        d = c.execute(f"SELECT * FROM {self.db} WHERE userid = {userid}")
        
        #no idea why I have to create a var, but I do
        #tried d.fetchall()[0][1] and [0] is out of the index's range for some reason despite the object being a list and having that index
        theget = d.fetchall()
        
        return theget[0][1] if theget else False
    
    def fetch(self):
        conn = sqlite3.connect("db")
        c = conn.cursor()
        
        d = c.execute(f"SELECT * FROM {self.db}")
        
        return d.fetchall()
        
    def check(self, userid):
        db = self.fetch()
        userids = [el[0] for el in db]
        return (userid in userids)


#This is the only part of the entire project anyone helped me
#Thank you Tallis for knowing SQL, But where the hell is the rest of the team

def createdb(which):
    conn = sqlite3.connect("db")
    c = conn.cursor()
    
    c.execute(f"CREATE TABLE data ([userid] INTEGER PRIMARY KEY NOT NULL, [time] TEXT NOT NULL)")
    c.execute(f"CREATE TABLE actives ([userid] INTEGER PRIMARY KEY NOT NULL, [time] TEXT NOT NULL)")
    c.execute(f"CREATE TABLE used ([userid] INTEGER PRIMARY KEY NOT NULL, [time] TEXT NOT NULL)")
    
    conn.commit()
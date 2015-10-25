#Account_Management.py
#-------------------------------------------------------------------------------
#CONTRIBUTORS: Joyce Scalettar, Sarah Borland

import sqlite3 as lite
import sys
from array import array
import random
#from sys import argv

#--- STRUCT FOR PERSON OBJECT ---------------------------------------------------
class person(object):
    def __init__(self, AcNum, mathP, spanishP, CurrProb, CurrSubj):
        self.AcNum = AcNum
        self.mathP = mathP
        self.spanishP = spanishP
        self.CurrProb = CurrProb
        self.CurrSubj = CurrSubj

#--- Connect to database file ---------------------------------------------------
#def runCommand(self, sql, params=(), commit=True):
#    self.cursor.execut(sql, params)
#    if commit:
#        self.connector.commit()
#cmd = "attach ? as toMerge"
#cursor.execute(cmd, ('text2learn.db',))
#cmd = "attach ? as toMerge"
#cursor.execute(cmd, ('subscribers.db',))
#cmd = "attach ? as toMerge"
#cursor.execute(cmd, ('account.db',))

#con = lite.connect('text2learn.db')

#--- Adds user to account table and initializes variables ------------------------
#----To Use: init_subscribe(user account number)
#----For first subscribers, however it has checking to make sure for no duplicate subscribers
def init_subscribe(user):
    con = lite.connect('account.db')
    cursor = con.cursor() 
    account = person(user,0,0,None,None)
    cursor.execute("CREATE TABLE IF NOT EXISTS account(UserID TEXT, MathPoint INT, SpanishPoint INT, ProblemID INT, SubjectID TEXT)")  
    cursor.execute("SELECT UserID FROM account WHERE UserID=?",(user,))
    check= cursor.fetchone()
    if check==None:
        cursor.execute("INSERT INTO account VALUES(?, ?, ?, ?, ?)", (account.AcNum, account.mathP, account.spanishP,account.CurrProb,account.CurrSubj,))
    #test to see if user is in account table
    #cursor.execute("SELECT * FROM account")
    #print(cursor.fetchall())
    con.commit()
    con.close() 
	
#----Subscribes the user to the subject specified
#----To Use: send_problem(user account number, either learn spanish or math string)
#----Returns: string that contains the problem
def send_problem(user, subject):
    qNum = 0
    maxTable=-1
    sendQ =''
    category ='null'
    con = lite.connect('account.db')
    cursor = con.cursor() 
    c = lite.connect('text2learn.db')
    cur = c.cursor()
    print subject
    if subject == 'learn spanish':
        category = 'spanish'
    elif subject == 'learn math':
        category = 'math'
    print category
    cur.execute("SELECT * FROM "+category)
    for row in cur:
        maxTable=maxTable+1
        #print cur.fetchall()
    print maxTable
    qNum = random.randint(0,maxTable)
    cursor.execute("UPDATE account SET ProblemID = ? WHERE UserID = ?", (qNum,user,))
    cursor.execute("UPDATE account SET SubjectID = ? WHERE UserID = ?", (category,user,))
    cur.execute("SELECT Question FROM "+category+" WHERE Id=?",(qNum,))
    sendQ= cur.fetchone()
    cursor.execute("SELECT * FROM account")
    print(cursor.fetchall())
    con.commit()
    con.close() 
    c.commit()
    c.close() 
    
    return sendQ    
    
#def recieve_answer(user, answer):
    
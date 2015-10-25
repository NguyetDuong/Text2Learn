#Account_Management.py
#Python file that is in charge of maintaining the user data and changes in the account database
# user == phone number
#-------------------------------------------------------------------------------
#TO USE: Account_Management.METHODS(args)
#Available Methods:
#init_subscribe(user) - Takes in a user account number and intializes an account on the account database
#del_subscribe(user) - Takes in user account number and removes account from account database
#send_problem(user, subject) - Takes in a user account number as well as appropiate input flags 
#                             ('learn math' or 'learn spanish') to return a question from the text2learn database.
#                              Returns a congratulations string!
#recieve_answer(user,answer) - Takes in a user account number as well as their inputted answer 
#                              and updates their points depending if their answer is correct (according to text2learn.db)
#                              Returns string that states win or loss condition.
#check_points(user)         - Takes in a user account number and returns a string describing their points in all categories 
#Test file: testAccount.py (prints to terminal)
#CONTRIBUTORS: Joyce Scalettar, Sarah Borland

import sqlite3 as lite
import sys
from array import array
import random
import math
MAXPOINTS = 300

#--- STRUCT FOR PERSON OBJECT ---------------------------------------------------
class person(object):
    def __init__(self, AcNum, mathP, spanishP, CurrProb, CurrSubj,CurrLev):
        self.AcNum = AcNum
        self.mathP = mathP
        self.spanishP = spanishP
        self.CurrProb = CurrProb
        self.CurrSubj = CurrSubj
        self.CurrLev = CurrLev

#--- Adds user to account table and initializes variables ------------------------
#----To Use: init_subscribe(user account number)
#----Returns: String containing welcome message
def init_subscribe(user):
    con = lite.connect('account.db')
    cursor = con.cursor() 
    account = person(user,0,0,None,None,None)
	#Creates table if account table does not exist and adds user to it if user has not previously subscribed
    cursor.execute("CREATE TABLE IF NOT EXISTS account(UserID TEXT, MathPoint INT, SpanishPoint INT, ProblemID INT, SubjectID TEXT, LevelID TEXT)")  
    cursor.execute("SELECT UserID FROM account WHERE UserID=?",(user,))
    check= cursor.fetchone()
    if check==None:
        cursor.execute("INSERT INTO account VALUES(?, ?, ?, ?, ?, ?)", (account.AcNum, account.mathP, account.spanishP,account.CurrProb,account.CurrSubj,account.CurrLev))
    subString = "Congratlations! You have successfully subscribed! Text 'learn math' or 'learn spanish' for quiz questions."
	#Test to see if user is in account table
    #cursor.execute("SELECT * FROM account")
    #print(cursor.fetchall())
    con.commit()
    con.close()
    return subString

#--- Removes user to account table------------------------
#----To Use: del_subscribe(user account number)
#----Returns: String containing goodbye message
def del_subscribe(user):
    con = lite.connect('account.db')
    cursor = con.cursor()
    cursor.execute("DELETE FROM account WHERE UserID=?",(user,))
    #Test to see if the user has unsubscribed
	#cursor.execute("SELECT * FROM account")
    #print(cursor.fetchall())
    dString ="You've successfully unsubscribed to Text2Learn! Hope you come back soon!"
    return dString
	
#----Sends user a quiz question from quiz database
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

    level = str((MAXPOINTS/100)-1)
    # print subject

    if subject == 'learn spanish':
        cursor.execute("SELECT SpanishPoint FROM account WHERE UserID = ?", (user,))
        sPnt = int(''.join(map(str,cursor.fetchone())))
        if sPnt != MAXPOINTS:
            sPnt = sPnt/100
            level = str(int(math.floor(sPnt)))
        category = 'spanish'+level
        subject = 'spanish'
    elif subject == 'learn math':
        cursor.execute("SELECT MathPoint FROM account WHERE UserID = ?", (user,))
        mPnt = int(''.join(map(str,cursor.fetchone())))
        if mPnt != MAXPOINTS:
            mPnt = mPnt/100
            level = str(int(math.floor(mPnt)))
        category = 'math'+level
        subject = 'math'
	#print level
    # print category
        category = 'math'
    cur.execute("SELECT * FROM "+category)
    for row in cur:
        maxTable=maxTable+1
    qNum = random.randint(0,maxTable)
    cursor.execute("UPDATE account SET ProblemID = ? WHERE UserID = ?", (qNum,user,))
    cursor.execute("UPDATE account SET SubjectID = ? WHERE UserID = ?", (subject,user,))
    cursor.execute("UPDATE account SET LevelID = ? WHERE UserID = ?", (category,user,))
    cur.execute("SELECT Question FROM "+category+" WHERE Id=?",(qNum,))
    sendQ= cur.fetchone()
    cursor.execute("SELECT * FROM account")
    con.commit()
    con.close() 
    c.commit()
    c.close() 
    
    return sendQ    

#--- Compares user answer with quiz database and returns win/lose conditions based on comparison ------------------------
#----To Use: recieve_answer(user account number, answer)
#----Return: String with win/loss condition message
def recieve_answer(user, answer):
    finString = "EMPTY STRING"
    reset = None
    con = lite.connect('account.db')
    cursor = con.cursor() 
    c = lite.connect('text2learn.db')
    cur = c.cursor()
    cursor.execute("SELECT SubjectID FROM account WHERE UserID=?", (user,))
    sID = ''.join(map(str,cursor.fetchone()))
    cursor.execute("SELECT LevelID FROM account WHERE UserID=?", (user,))
    lID = ''.join(map(str,cursor.fetchone()))
    cursor.execute("SELECT ProblemID FROM account WHERE UserID = ?", (user,))
    pID = int(''.join(map(str,cursor.fetchone())))
    cur.execute("SELECT Answer FROM "+lID+" WHERE Id = ?", (pID,))
    cur.execute("SELECT Answer FROM "+sID+" WHERE Id = ?", (pID,))
    answerDB = ''.join(map(str,cur.fetchone()))
    finString = "Sorry! Your answer of "+answer+" was incorrect. The correct answer was "+answerDB+". Don't give up! Try again soon!"
    lvlString = ""
    if answerDB == answer:
        if sID == 'spanish':
            cursor.execute("SELECT SpanishPoint FROM account WHERE UserID = ?", (user,))
            sPnt = int(''.join(map(str,cursor.fetchone())))
            if sPnt < MAXPOINTS:
			    sPnt = sPnt + 10
            checkPnt = sPnt
            cursor.execute("UPDATE account SET SpanishPoint = ? WHERE UserID = ?", (sPnt,user,))
        if sID == 'math':
            cursor.execute("SELECT MathPoint FROM account WHERE UserID = ?", (user,))
            mPnt = int(''.join(map(str,cursor.fetchone())))
            if mPnt < MAXPOINTS:
			    mPnt = mPnt + 10
            checkPnt = mPnt
            cursor.execute("UPDATE account SET MathPoint = ? WHERE UserID = ?", (mPnt,user,))
        checkPnt = checkPnt/100
        level = str(int(math.floor(checkPnt)))
        finString ="Congratlations! Your answer of "+answer+" was correct! You are at the max level for this subject! You won't be able to earn any more points but keep playing to learn some more!\nSend 'check points' to see how many points you earned!"
        if level<3:
            checkUpdate = sID+level
            level=int(level)
            level=str(level)
            #print checkUpdate
            #print lID
            if lID != checkUpdate:
		        lvlString = "\nAlso, you have earned enough points to level up to Level "+level+" "+sID+"! Congratlations! Keep it up!"
            finString = "Congratulations! Your answer of "+answer+" was correct! You earned 10 more points for the "+sID+" category!"+lvlString+"\nSend 'check points' to see how many points you earned!"
	    
	cursor.execute("UPDATE account SET ProblemID = ? WHERE UserID = ?", (reset,user,))
    cursor.execute("UPDATE account SET SubjectID = ? WHERE UserID = ?", (reset,user,))	
    con.commit()
    con.close() 
    c.commit()
    c.close() 
    return finString
	
#--- Sends users point status ------------------------
#----To Use: check_points(user account number)
#----Return: String containing current user point count for each subject
def check_points(user):
    con = lite.connect('account.db')
    cursor = con.cursor() 
    cursor.execute("SELECT MathPoint FROM account WHERE UserID = ?", (user,))
    mPnt = (''.join(map(str,cursor.fetchone())))
    cursor.execute("SELECT SpanishPoint FROM account WHERE UserID = ?", (user,))
    sPnt = (''.join(map(str,cursor.fetchone())))
    rString = "You have "+mPnt+" Math Points and "+sPnt+" Spanish Points! Keep up the good work!"	
    con.commit()
    con.close()
    return rString
	

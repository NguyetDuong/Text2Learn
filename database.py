#database.py
#Python script used to generate the database of all the quizzes and answers
#------------------------------------------------------------------------------
#Database file name: text2learn.db
#How to run: python database.py input.txt
#What it does: This program reads in an input file that has a subject name
#followed by questions & answers and makes a table that has all 
#questions and their answers
#Read in file format: (refer to input.txt for example)
#
#subjectName
#question
#answer
#question
#answer ...
#
#subjectName
#question
#answer
#question
#answer ...
#
#
#Ordering of table:
# | Subject | Problem ID | Question | Answer |
#------------------------------------------------------------------------------
#CONTRIBUTERS: Sarah Borland, Joyce Scalettar, Hui Shi

import sqlite3 as lite
import sys
from array import array
from sys import argv

#--- ARGUMENTS ----------------------------------------------------------------
script, filename = argv

#--- STRUCT FOR QUIZ OBJECT ---------------------------------------------------
#Has a question array and an answer array
class quiz(object):
    def __init__(self, title):
        self.title = title
    qArray=[None]*101
    aArray=[None]*101
#Initialization of quiz object ------------------------------------------------
quizObject = quiz(["title"])


try:
	#Connect to database file -------------------------------------------------
    con = lite.connect('text2learn.db')
    cur = con.cursor()  
    file = open(filename)
    lineNum = 0
    x = 1
	
	#Go through to add lines to table -----------------------------------------
    while True:
        nextLine = file.readline()
		
		#Break from while when end of txt file is reached ---------------------
        if nextLine=='':
             #print 'END OF FILE'
             break
			 
		#New line means that there will be a next table label and, ------------
		#if there has already been one table's worth of data scanned into 
		#the quiz object, a table will be created 
        if nextLine=='\n':
            #print 'NEW LABEL'
			
            #A table's worth of data has been scanned, make table -------------
            if lineNum>0:
                #print 'PUTTING IN TABLE'
                categories = ''.join(quizObject.title).rstrip('\n')
                QuizArr=[None]*lineNum
                for n in range(0, lineNum):
                    QuizArr[n] =(categories,(n), (quizObject.qArray[n]), (quizObject.aArray[n])) 
                    #print (QuizArr[n])
                #print quizObject.qArray[n]
                #print categories
                #cur.execute('''DROP TABLE IF EXISTS '''+categories)
                cur.execute("DROP TABLE IF EXISTS "+categories)
                #print "making table"
				
				#The table holds the question ID, the question itself, and then the answer
				#in each column. When grabbing data from the database, it should (hopefully!)
				#have it's datatype already set.
                cur.execute("CREATE TABLE "+categories+"(Subject TEXT, Id INT, Name TEXT, Answer TEXT)")  
                cur.executemany("INSERT INTO "+categories+" VALUES(?, ?, ?, ?)", QuizArr)
            #print "finished if statement"
            #cur.execute("SELECT * FROM math")
            #print cur.rowcount
            #print "+++++++++++++++++++++++++++"
            #print cur.fetchone()
            #print "/+++++++++++++++++++++++++"
            #lineNum=0
            #print "finished if statement"
            #cur.execute("SELECT * FROM spanish")
            #print cur.rowcount
            #print "+++++++++++++++++++++++++++"
            #print cur.fetchone()
            #print "/+++++++++++++++++++++++++"
			
			#Read in new table's label and reset table variables --------------
            lineNum=0
            quizName=file.readline()
            quizObject.title = quizName
            #print 'GETTING QUIZ NAME: '+quizObject.title
            #print quizObject.title 
		#Reading in the questions and answers into the quiz object arrays -----
        else:
            #print 'ENTERING ELSE'
            if x==1:
                x = 2
				#Save line from file into question array ----------------------
                quizObject.qArray[lineNum] = nextLine.rstrip('\n')
            else:
                x = 1
				#Save line from file into answer array ------------------------
                quizObject.aArray[lineNum] = nextLine.rstrip('\n')
                lineNum=lineNum+1
    con.commit()

	#testing
    cur.execute("SELECT * FROM math")
    print(cur.fetchall())
    cur.execute("SELECT * FROM spanish")
    print(cur.fetchall())

#Error handling: prints out error location
except lite.Error, e:
    if con:
        con.rollback()
    print "Error %s:" % e.args[0]
    sys.exit(1)

#Closes connection   
finally:
    if con:
        con.close() 
#database.py
#Python script used to generate the database of all the quizzes and answers
#-------------------------------------------------------------------
#Database file name: text2learn.db
# Ordering of table:
# | Id | Question | Answer|
# Current tables:
# math
# spanish
#------------------------------------------
#CONTRIBUTERS: Sarah Borland, Joyce Scalettar, Hui Shi


import sqlite3 as lite
import sys
from array import array
from sys import argv

#arguments 
script, filename = argv


class quiz(object):
    def __init__(self, title):
        self.title = title
    qArray=[None]*101
    aArray=[None]*101
    nArray=[None]*101
    numQuiz=0
  
 
#for now, I have it using preset arrays, my next plan is to have it intake a textfile
#and automatically create these arrays for ease of editing yaaaa <3
#mathArr=[(1,'5+9=?','14' ),
#		    (2, '3*3=?','9'),
#			(3, '8/2=?','4'),
#		  ]
		   
#spanishArr=[(1, 'What is the cat in Spanish?','el gato' ),
#		    (2, 'What is bread in Spanish?','el pan'),
#			(3, 'What is programmer in Spanish?','programador'),
#		    ]


quizObject = quiz(["title"])

try:
    con = lite.connect('text2learn.db')
    cur = con.cursor()  
    file = open(filename)
    lineNum = 0
    x =1
    while True:
        nextLine = file.readline()
        if nextLine=='':
             print 'END OF FILE'
             break
        if nextLine=='\n':
            print 'NEW LABEL'
            if lineNum>0:
                print 'PUTTING IN TABLE'
                QuizArr=[None]*lineNum
                for n in range(0, lineNum):
                    QuizArr[n] =((n), (quizObject.qArray[n]), (quizObject.aArray[n])) 
                    #print (QuizArr[n])
                #print quizObject.qArray[n]
                categories = ''.join(quizObject.title)
                #print categories
                #cur.execute('''DROP TABLE IF EXISTS '''+categories)
                cur.execute("DROP TABLE IF EXISTS "+categories)
                #print "making table" 
                cur.execute("CREATE TABLE "+categories+"(Id INT, Name TEXT, Answer TEXT)")  
                
                #print lineNum                
                #for n in range(0,lineNum):
                 #   cur.execute('''INSERT INTO '''+categories+'''(Id, Question, Answer) VALUES(?, ?, ?)''', (n, quizObject.qArray[n], quizObject.aArray[n],))
                
                cur.executemany("INSERT INTO "+categories+" VALUES(?, ?, ?)", QuizArr)
                
                #cur.execute("INSERT INTO math VALUES (?,?,?)", (QuizArr,))
                


                #print QuizArr
                #stmt = "insert into " + categories + " (Id, Question, Answer) values (?, ?, ?)"   
                #cur.executemany(stmt, QuizArr)
                #print cur.rowcount

            print "finished if statement"
            cur.execute("SELECT * FROM math")
            #print cur.rowcount
            print "+++++++++++++++++++++++++++"
            print cur.fetchone()
            print "/+++++++++++++++++++++++++"
            lineNum=0
            print "finished if statement"
            cur.execute("SELECT * FROM spanish")
            #print cur.rowcount
            print "+++++++++++++++++++++++++++"
            print cur.fetchone()
            print "/+++++++++++++++++++++++++"
            lineNum=0
            #quizObject.numQuiz=quizObject.numQuiz+1
            quizName=file.readline()
           # getattr(quizzes,quizName)
            quizObject.title = quizName
            print 'GETTING QUIZ NAME: '+quizObject.title
            #print quizObject.title 
        else:
           # print 'ENTERING ELSE'
           
            if x==1:
                x = 2
                quizObject.qArray[lineNum] = nextLine.rstrip('\n')
            else:
                x = 1
                quizObject.aArray[lineNum] = nextLine.rstrip('\n')
                lineNum=lineNum+1
            #print x
           # print nextLine

  
#The table holds the question ID, the question itself, and then the answer
#in each column. When grabbing data from the database, it should (hopefully!)
#have it's datatype already set.



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
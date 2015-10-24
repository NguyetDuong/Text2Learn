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
#THINGS TO GET DONE:
#     Import file text into arrays (that goes into database)
#     Implement "difficulty" databases 
#CONTRIBUTERS: Sarah Borland & Joyce Scalettar


import sqlite3 as lite
import sys
from array import array

#for now, I have it using preset arrays, my next plan is to have it intake a textfile
#and automatically create these arrays for ease of editing yaaaa <3
mathArr=[(1,'5+9=?',14 ),
		    (2, '3*3=?',9),
			(3, '8/2=?',4),
		  ]
		   
spanishArr=[(1, 'What is the cat in Spanish?','el gato' ),
		    (2, 'What is bread in Spanish?','el pan'),
			(3, 'What is programmer in Spanish?','programador'),
		    ]
try:
    con = lite.connect('text2learn.db')
    cur = con.cursor()  
	

		   
#The table holds the question ID, the question itself, and then the answer
#in each column. When grabbing data from the database, it should (hopefully!)
#have it's datatype already set.

    cur.executescript("""
        DROP TABLE IF EXISTS math;
		DROP TABLE IF EXISTS spanish;
        CREATE TABLE math(Id INT, Question TEXT, Answer INT);
		CREATE TABLE spanish(Id INT, Question TEXT, Answer TEXT);
        """)
		
    cur.executemany('INSERT INTO math VALUES (?,?,?)', mathArr)
    cur.executemany('INSERT INTO spanish VALUES (?,?,?)', spanishArr)

    con.commit()

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
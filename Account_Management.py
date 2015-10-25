#Account_Management.py

import sqlite3 as lite
import sys
from array import array
from sys import argv

#--- STRUCT FOR PERSON OBJECT ---------------------------------------------------
class person(object):
    def __init__(self, AcNum):
        self.AcNum = AcNum
    self.math = None
    self.spanish = None
    self.CurrProb = None
    self.CurrSubj = None

#--- Connect to database file ---------------------------------------------------
def runCommand(self, sql, params=(), commit=True):
    self.cursor.execut(sql, params)
    if commit:
        self.connector.commit()
cmd = "attach ? as toMerge"
cursor.execut(cmd, ('text2learn.db',))
cmd = "attach ? as toMerge"
cursor.execut(cmd, ('Subscribers.db',))

#con = lite.connect('text2learn.db')

def update_accounts
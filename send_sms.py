## This is written for intitial testing.
## Primary offline, used to send messages to all "subscribers."
## Contributer: Hui Shi Li

from twilio.rest import TwilioRestClient
from wordnik import *
import sqlite3 as lite
import sys
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '2c2aa817225a9b275e2170c366304d437582c298f11a89644'
wclient = swagger.ApiClient(apiKey, apiUrl)

# To find these visit https://www.twilio.com/user/account
ACCOUNT_SID = "null"
AUTH_TOKEN = "null"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

#our phone
base = "+14152149331"
#hash table of the SMS received
msg_received = {}

#to get word of the day
wordsApi = WordsApi.WordsApi(wclient)
wotd = wordsApi.getWordOfTheDay().word

#used to get word of the day definition
wordApi = WordApi.WordApi(wclient)
wotd_defs = wordApi.getDefinitions(wotd)
wotd_def = wotd_defs[0].text

#contacts hash: key:name value:phone_number
#contacts = {}

#used to send SMS
def send_SMS_wotd():
	"""Used to send daily SMS for Word of the Day."""
	con = lite.connect('subscribers.db')
	con.text_factory = str
	cur = con.cursor()
	cur.execute("SELECT * FROM Subscribers")
	rows = cur.fetchall()

	for row in rows:
	#for person in contacts:
		message = client.messages.create(
	    	body= "Guess the word of the day! Definition: " + wotd_def ,  # Message body, if any
	    	to= str(row[0]),#contacts[person],
			from_=base,
		)
	con.close()

def get_wotd():
	"""Returns the word of the day."""
	return wotd

#add received SMS to hash - msg_received
def get_SMS():
	"""Add received SMS to hash -- msg_received."""
	for msg in client.messages.list():
		#check for incoming sms and add to hash

		#delete prev SMS from same sender	
		if(msg.from_ != base):
			#check if sender had sent SMS previously
			if msg.from_ in msg_received.keys():
				#if so delete the prev SMS
				curr_sid = msg.sid
				delete_rSMS(curr_sid)		
			else :
				#otherwise store in hash
				msg_received[msg.from_] = msg.body		
			
def delete_rSMS(dsid):
	"""Used to delete received SMS == delete previous SMS from same senders."""
	client.messages.delete(dsid)
	

def delete_sSMS():
	"""Used to delete sent SMS. WILL DELETE ALL SMS WE'VE SENT.
	   To delete a specific SMS, replace msg.sid with 
	   the sid of the sms you want to delete."""
	for msg in client.messages.list():
		temp = str(msg.from_)
		if(temp == base):
			client.messages.delete(msg.sid)

#print received SMS
def print_rSMS():
	"""Print received SMS."""
	#key = phone #, val = body of msg
	for k in msg_received.keys():
		print "From: " + k + " Body: " + msg_received[k]

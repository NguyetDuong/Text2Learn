from twilio.rest import TwilioRestClient
from wordnik import *
import sqlite3 as lite
import sys
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '2c2aa817225a9b275e2170c366304d437582c298f11a89644'
wclient = swagger.ApiClient(apiKey, apiUrl)


##################################
# con = lite.connect('text2learn.db')

# with con:
# 	curr = con.cursor()
# 	cur.execute("SELECT * FROM spanish")

# 	rows = cur.fetchall()

# 	for row in rows:
# 		print row


#if needed to convert phone # to e164
#def convert_to_e164(raw_phone):
#    if not raw_phone:
#        return

#    if raw_phone[0] == '+':
        # Phone number may already be in E.164 format.
#        parse_type = None
#    else:
        # If no country code information present, assume it's a US number
#        parse_type = "US"

#    phone_representation = phonenumbers.parse(raw_phone, parse_type)
#    return phonenumbers.format_number(phone_representation,
#        phonenumbers.PhoneNumberFormat.E164)

# To find these visit https://www.twilio.com/user/account
ACCOUNT_SID = "ACa136b47b25a3e1297d2cdbe8a65dd8ca"
AUTH_TOKEN = "be72154f7e25bb7c4fc7421e2cbef3f6"
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

#contacts hash
#'mimi' : "+14153749191"
contacts = {'gavin' : '+16507769918',
 'joyce' : "+15306018016", 'brian' : '+14158718763' }


#used to send SMS
def send_SMS_wotd():
	"""Used to send SMS."""
	#con = lite.connect('subscribers.db')
	#con.text_factory = str
	#cur = con.cursor()
	#cur.execute("SELECT * FROM Subscribers")
	#rows = cur.fetchall()

	#for row in rows:
	for person in contacts:
		message = client.messages.create(
	    	body= "Guess the word of the day! Definition: " + wotd_def ,  # Message body, if any
	    	to= contacts[person],#str(row[0])
			from_=base,
		)

#add received SMS to hash - msg_received
def get_SMS():
	"""Add received SMS to hash -- msg_received."""
	for msg in client.messages.list():
		#check for incoming sms and add to hash
		######USED FOR TESTING##########
		# print "\nMSID: " + msg.sid
		# print "body: " + msg.body
		# print "from: " + msg.from_
		################################

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
	print "\n"
	for k in msg_received.keys():
		print "From: " + k + " Body: " + msg_received[k]
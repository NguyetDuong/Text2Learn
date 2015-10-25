from twilio.rest import TwilioRestClient
from wordnik import *
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '2c2aa817225a9b275e2170c366304d437582c298f11a89644'
wclient = swagger.ApiClient(apiKey, apiUrl)

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

# our phone
#base = "+16507298318"
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
contacts = {  'mimi' : "+14153749191", 'david' : "+15106913320", 'gavin' : '+16507769918'}

#'mimi' : "+14153749191", 'sarah': "+18316005752",
 #'joyce' : "+15306018016", 


#used to send SMS
def send_SMS_wotd():	
	for person in contacts:
		message = client.messages.create(
	    	body = "Guess the word of the day! Definition: " + wotd_def ,  # Message body, if any
	    	to = contacts[person],
			from_ = "+14152149331",
		)



#add received SMS to hash - msg_received
def get_SMS():
	for msg in client.messages.list():
		
		#check for incoming sms and add to hash
		######USED FOR TESTING##########
		print "\nMSID: " + msg.sid
		print "body: " + msg.body
		print "from: " + msg.from_
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
			
#use to delete received SMS == del prev SMS from same sender
def delete_rSMS(dsid):
	client.messages.delete(dsid)
	

#use to delete sent SMS
#WARNING: WILL DELETE ALL SMS WE'VE SENT
#to delete a specific sms, replace msg.sid with sid of the sms you want to delete
def delete_sSMS():
	for msg in client.messages.list():
		temp = str(msg.from_)
		if(temp == base):
			client.messages.delete(msg.sid)

#print received SMS
def print_rSMS():
	#key = phone #, val = body of msg
	print "\n"
	for k in msg_received.keys():
		print "From: " + k + " Body: " + msg_received[k]



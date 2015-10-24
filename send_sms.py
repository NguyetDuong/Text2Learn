from twilio.rest import TwilioRestClient

def convert_to_e164(raw_phone):
    if not raw_phone:
        return

    if raw_phone[0] == '+':
        # Phone number may already be in E.164 format.
        parse_type = None
    else:
        # If no country code information present, assume it's a US number
        parse_type = "US"

    phone_representation = phonenumbers.parse(raw_phone, parse_type)
    return phonenumbers.format_number(phone_representation,
        phonenumbers.PhoneNumberFormat.E164)

# To find these visit https://www.twilio.com/user/account
ACCOUNT_SID = "ACc98c7be798532eb3bf9a428f5c152f64"
AUTH_TOKEN = "f177b7ab10a41be5f6fa9c82d5696f62"


client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

#message = client.messages.create(
#    body="Hello Nguyet, we got twilio!",  # Message body, if any
#    to="+14155741183",
#    from_="+16507298318",
#)

#our phone
base = "+16507298318"
#hash table of the messages sent to us
msg_received = {}

#base = "+16507298318"
def getIncSMS():
	for msg in client.messages.list():
		#convert e164 to to str
		temp = str(msg.from_)
		#check for inc sms
		if(temp != base):
			print "Body: "+ msg.body
			print "Sid: " + msg.from_
			#store in hash
			msg_received[msg.from_] = msg.body


def printRSMS():
	#key = phone #, val = body of msg
	for k in msg_received.keys():
		print "Msg from: " + k + " Body: " + msg_received[k]

getIncSMS()
printRSMS()
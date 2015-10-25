from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
from send_sms import send_SMS_wotd
import twilio.twiml
import sqlite3 as lite
import sys

 
app = Flask(__name__)

name = "Text2Learn"
subscribeMessage = "make it easier"
errorMessage = "To subscribe, please reply with MAKE IT EASIER"

ACCOUNT_SID = "ACa136b47b25a3e1297d2cdbe8a65dd8ca"
AUTH_TOKEN = "be72154f7e25bb7c4fc7421e2cbef3f6"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


def parseSubscription(inp):
	"""Takes in a String, and will parse it to see if it contains the phrase
	   to subscribe to our Text2Learn."""

	l = inp.lower()
	l = l.rstrip()
	l = l.lstrip()
	
	b = (l == subscribeMessage)
	return b

# App is being run at this point, all variables & methods 
# not related to app should be above

@app.route("/", methods=['GET', 'POST'])
def start():
	"""Break statements -- decide where things should go."""
	body_message = request.values.get('Body', None)
	person_number = request.values.get('From', None)
	pnumber = request.values.get('From',None)

	con = lite.connect('subscribers.db')
	con.text_factory = str
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM Subscribers")
		rows = cur.fetchall()

		for row in rows:
			if str(row[0] == person_number):
				#print(str(row[0]))
				cur.exectue("DELETE FROM Subscribers WHERE subscriber = (?)", person_number)
				#con.close()
				#return help(person_number)
		

		for row in rows: 
			print str(row[0])
	# return subscribe(body_message, person_number)

@app.route("/help", methods=['GET', 'POST'])
def help(person_number):
	"""Tells the user what to type for which subject to learn."""

	print("went into /help")
	automatic_help_reply = "To learn math, type LEARN MATH. To learn Spanish, type LEARN SPANISH."

	message = client.messages.create(
			body= automatic_help_reply,
			to= person_number,
			from_= "+14152149331",
	)

@app.route("/subscribe", methods=['GET', 'POST'])
def subscribe(body_message, person_number):
	"""Notifies if a person has subscribed or what they should type in order to subscribe."""

	automatic_subscription = "You are now subscribed to " + name + ". To learn the key functions, text HELP back."

	if parseSubscription(body_message):
		resp = twilio.twiml.Response()
		resp.message(automatic_subscription)
		con = lite.connect('subscribers.db')
		con.text_factory = str
		cur = con.cursor()
		print("person_number is:  " + person_number)
		#cur.exectue("DELETE FROM Subscribers WHERE subscriber = (?)", person_number)
		cur.execute("INSERT INTO Subscribers VALUES (?);", (person_number,))
		#cur.execute("SELECT * FROM Subscribers")
		con.commit()
		con.close()
	else:
		resp = twilio.twiml.Response()
		resp.message(errorMessage)
	return str(resp)


send_SMS_wotd() # begins with sending the wotd to everyone



if __name__ == "__main__":
    app.run(debug=False)
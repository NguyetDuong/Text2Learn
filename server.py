from flask import Flask, request, redirect
from send_sms import send_SMS_wotd
import twilio.twiml
import sqlite3 as lite
import sys

 
app = Flask(__name__)

name = "Text2Learn"
subscribeMessage = "make it easier"
errorMessage = "To subscribe, please reply with MAKE IT EASIER"

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

	

	return subscribe(body_message, person_number)


@app.route("/subscribe", methods=['GET', 'POST'])
def subscribe(body_message, person_number):
	"""Reads the incoming messages to see who is subscribing."""

	automatic_subscription = "You are now subscribed to " + name + ". To learn the key functions, text HELP back."

	if parseSubscription(body_message):
		resp = twilio.twiml.Response()
		resp.message(automatic_subscription)
		con = lite.connect('subscribers.db')
		cur = con.cursor()
		cur.execute("INSERT INTO Subscribers VALUES (?);", (person_number,))
		cur.execute("SELECT * FROM Subscribers")
		con.commit()
		con.close()
	else:
		resp = twilio.twiml.Response()
		resp.message(errorMessage)
	return str(resp)


send_SMS_wotd() # begins with sending the wotd to everyone



if __name__ == "__main__":
    app.run(debug=False)
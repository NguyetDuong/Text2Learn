from flask import Flask, request, redirect
import twilio.twiml
import sqlite3 as lite
import sys

app = Flask(__name__)
name = "Text2Learn"
subscribeMessage = "make it easier"
errorMessage = "To subscribe, please reply with MAKE IT EASIER"
subscribers = []

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
def subscribe():
	"""Reads the incoming messages to see who is subscribing."""

	automatic_subscription = "You are now subscribed to " + name + ". To learn the key functions, text HELP back."
	body_message = request.values.get('Body', None)
	person_number = request.values.get('From', None)
	if parseSubscription(body_message):
		resp = twilio.twiml.Response()
		con = lite.connect('subscribers.db')
    	cur = con.cursor()
    	cur.execute("DROP TABLE IF EXISTS Subscribers")
    	cur.execute("CREATE TABLE Subscribers(PhoneNumber TEXT")
    	cur.execute("INSERT INTO Subscribers VALUES(?)", person_number)	
    	con.close()
		resp.message(automatic_subscription)
		subscribers.append(person_number)
	else:
		resp = twilio.twiml.Response()
		resp.message(errorMessage)
	

	return str(resp)




 
if __name__ == "__main__":
    app.run(debug=True)
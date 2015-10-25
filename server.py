## This is the main file. It receives the messages, comprehends them, and direct them appropriately
## Contributers: Nguyet Duong, Hui Shi Li

from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
from send_sms import send_SMS_wotd
from word_parsing import tokenize_string, user_input_analysis
from Account_Management import *
import twilio.twiml
import sqlite3 as lite
import sys
 
app = Flask(__name__)

name = "Text2Learn"
subscribeMessage = "subscribe"
errorMessage = "To subscribe, please reply with SUBSCRIBE"

ACCOUNT_SID = "ACa136b47b25a3e1297d2cdbe8a65dd8ca"
AUTH_TOKEN = "be72154f7e25bb7c4fc7421e2cbef3f6"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
acc = "+14152149331"


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
	tokens = tokenize_string(body_message)
	translation = user_input_analysis(tokens)



	"""This is to check for duplication of subscribers, and remove them.
	   It also checks if the person messaging is a new or a returning subscriber."""
	#### BEGIN ####
	con = lite.connect('subscribers.db')
	con.text_factory = str
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM Subscribers")
		rows = cur.fetchall()
		#print cur.description
		print("got into the search")

		for row in rows:
			print("we are comparing: ")
			print("p#: " + person_number)
			print("row data: " +str(row[0]))
			print("--------------")
			if str(row[0]) == person_number:
				#print(str(row[0]))
				#cur.execute("DELETE FROM Subscribers WHERE subscriber = (?)", person_number)
				con.close()
				print("we are checking for txt back")
				"""This is the beginning of redirecting the messages in order for the
	   			user to achieve the correct message."""
	   			if translation == "help":
	   				return help(person_number)
	   			elif translation == "learn spanish":
	   				return spanish(person_number)
	   			elif translation == "learn math":
	   				return math(person_number)
	   			elif translation == "guess":
	   				return answer(person_number, tokens)
	   			elif translation == "points":
	   				return points(person_number)
	   			else:
	   				return invalid(person_number)
	print("where")
	con.close()
	print("done yet?")
	return subscribe(body_message, person_number)

	#### END ####
	

@app.route("/help", methods=['GET', 'POST'])
def help(person_number):
	"""Tells the user what to type for which subject to learn."""

	print("went into /help")
	automatic_help_reply = "Currently we have two different courses: math and Spanish. To learn Spanish, please reply with: LEARN SPANISH." \
	" To learn math, please reply with: LEARN MATH. If you wish to know how many points you have, reply with CHECK POINTS." \
	"To find out more about us and our product, please visit http://goo.gl/Mrp3QK." \
	"\n\nWhenever answering questions, make sure to begin your reply with ANSWER, then just your answer."

	message = client.messages.create(
			body= automatic_help_reply,
			to= person_number,
			from_= acc,
	)

@app.route("/invalid", methods=['GET', 'POST'])
def invalid(person_number):
	print("went into /invalid")
	reply = "It seems like you have given an invalid input. Please reply with: HELPME (one word) for valid inputs."
	message = client.messages.create(
			body = reply,
			to = person_number,
			from_ = acc,
		)

@app.route("/spanish", methods=['GET', 'POST'])
def spanish(person_number):
	print("went into /spanish")
	question = send_problem(person_number, "learn spanish")
	reply = str(question[0]) + "\nRemember to begin your answer with ANSWER."

	message = client.messages.create(
			body = reply,
			to = person_number,
			from_ = acc,
		)

@app.route("/math", methods=['GET', 'POST'])
def math(person_number):
	print("went into /math")
	question = send_problem(person_number, "learn math")
	reply = str(question[0]) + "\nRemember to begin your answer with ANSWER"

	message = client.messages.create(
			body = reply,
			to = person_number,
			from_ = acc,
		)

@app.route("/answer", methods=['GET', 'POST'])
def answer(person_number, guess):
	print("went into /answer")
	print("user answer: " + guess[1])
	response = recieve_answer(person_number, guess[1])
	print(response)
	reply = str(response)

	message = client.messages.create(
			body = reply,
			to = person_number,
			from_ = acc,
		)

@app.route("/points", methods=['GET', 'POST'])
def points(person_number):
	print("went into /points")
	response = check_points(person_number)
	reply = str(response)

	message = client.messages.create(
			body = reply,
			to = person_number,
			from_ = acc,
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
		#cur.execute("CREATE TABLE Subscribers(subscriber TEXT)")
		#cur.exectue("DELETE FROM Subscribers WHERE subscriber = (?)", person_number)
		print("added subscriber")
		cur.execute("INSERT INTO Subscribers VALUES (?);", (person_number,))
		#cur.execute("SELECT * FROM Subscribers")
		con.commit()
		con.close()

		"""Creating a user in the database. Changes made bellow here."""
		init_subscribe(person_number)
	else:
		resp = twilio.twiml.Response()
		resp.message(errorMessage)
	return str(resp)

send_SMS_wotd() # begins with sending the wotd to everyone

if __name__ == "__main__":
    app.run(debug=False)
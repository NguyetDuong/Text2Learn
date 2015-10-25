## This file is for helpers methods in server.py
## Contributers: Nguyet Duong

def tokenize_string(s):
	"""Given a string, it will return an array of Strings.
	   Each index value is a word in the sentence, in order."""
	words = []
	s = s.lstrip()
	s = s.rstrip()
	s = s.lower()
	wd = ""

	for l in s:
		if l == ' ':
			words.append(wd)
			wd = ""
		else:
			wd += l
	words.append(wd)
	return words

def user_input_analysis(arr):
	"""Analyzes the user's input message, and decifer what they want to do.
	   Meaning figuring out which method to direct them to."""
	# print(arr)
	if arr[0] == "helpme":
		return "help"
	elif arr[0] == "answer":
		return "guess"
	elif arr[0] == "learn":
		if len(arr) == 1:
			return "help"
		elif arr[1] == "math":
			return "learn math"
		elif arr[1] == "spanish":
			return "learn spanish"
		elif len(arr) > 1:
			return "help"
	elif arr[0] == "check":
		if len(arr) == 1:
			return "help"
		elif arr[1] == "points":
			return "points"
	else:
		return "input"


def parseSubscription(inp):
	"""Takes in a String, and will parse it to see if it contains the phrase
	   to subscribe to our Text2Learn."""

	l = inp.lower()
	l = l.rstrip()
	l = l.lstrip()
	
	b = (l == subscribeMessage)
	return b

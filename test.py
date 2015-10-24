## THIS A TEST CLASS TO SEE HOW TWILIO WORKS
## Author: Nguyet Duong

from twilio.rest import TwilioRestClient
 
# Your Account Sid and Auth Token from twilio.com/user/account
# This is Nguyet's personal ID's
account_sid = "ACa136b47b25a3e1297d2cdbe8a65dd8ca"
auth_token  = "be72154f7e25bb7c4fc7421e2cbef3f6"
client = TwilioRestClient(account_sid, auth_token)

# Test send message to Rosalba
message = client.messages.create(body="Sup Rosalba, you wanna learn 2 code??",
    to="+14156120624",    # Replace with your phone number
    from_="+14152149331") # Replace with your Twilio number
print message.sid
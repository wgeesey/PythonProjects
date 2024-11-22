### SMS using Twilio API
### https://ntfy.sh/ is another useful tool for sms
## Programmable SMS

from twilio.rest import Client

account_sid = 'Account sid'
auth_token = '[Auth Token]'
client = Client(account_sid, auth_token)

message = client.message.create(
								from_='your number',
								to='destination number'
								)

print(message.sid)
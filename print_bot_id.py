import os
from slackclient import SlackClient

BOT_NAME= 'servitor'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


if __name__ == "__main__":
	api_call = slack_client.api_call("users.list")
	if api_call.get('ok'):
		# retrieve all usres so we can find our bot
		users = api_call.get('members')
		for user in users:
			if 'name' in user and user.get('name') == BOT_NAME:
				print("Die Bot ID für '" + user['name'] + "' ist " + user.get('id'))

#			else:
#				print("Dieser User ist nicht der  Bot mit Name " + BOT_NAME + " :/")

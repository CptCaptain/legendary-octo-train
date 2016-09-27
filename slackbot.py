import os
import time
import requests
#import json
#import pprint
#import kwargs
#import urllib.request
from slackclient import SlackClient

# Slackbot ID aus der Umgebungsvariable auslesen
BOT_ID=os.environ.get("BOT_ID")

#constants
AT_BOT="<@" + BOT_ID +">"
EXAMPLE_COMMAND = "tu"
PRIME = "prim"
WETTER = "a"
#instanziiere Slack und Twilio (was auch immer das sein mag)
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


#Funktionen zum parsen von Slack output und den handle commands und so
def handle_command(command, channel):
	"""
		Empfängt Befehle für den Bot und ermittelt, ob sie valide sind, den rest kannst du dir wahrscheinlich denken
	"""
	response="Wat meinste? Nimm den  *" + EXAMPLE_COMMAND + "* Befehl, du Spasti"
	if command.startswith(EXAMPLE_COMMAND):
		response="Alles klar, da fehlt aber noch ein bissl code, meinste nicht auch?"
		slack_client.api_call("chat.postMessage", channel=channel,
				text=response, as_user=True)
	if command.startswith(PRIME):
		i=1
		while i<50:
			#
			slack_client.api_call("chat.postMessage", channel=channel, text=i, as_user=True)
			i=i+2
	if command.startswith(WETTER):
		#Wetterversuch, mal schauen was drauss wirt
		openweather_api='442c26ca8ed7eec9212e6beb25720d27'
		#weather = requests.get('http://api.openweathermap.org/data/2.5/forecast/city?q=wiesbaden,de&APPID=' + openweather_api)
		weather = requests.get('http://api.openweathermap.org/data/2.5/forecast/city?q=wiesbaden,de&APPID=442c26ca8ed7eec9212e6beb25720d27')
		wjdata = weather.json()
		i=wjdata['list']
		#Location=wjdata['message']
		#Temp=wjdata['temp_max']
		#Pressure=wjdata['pressure']
		#Wind=wjdata['wind']
		#i=('In ' + Location + ' hat es ' + Temp + 'Grad, bei ' + Pressure + ' bar und ' + Wind)
		slack_client.api_call("chat.postMessage", channel=channel, text=i, as_user=True)


def parse_slack_output(slack_rtm_output):
	"""
		Die Slack Real Time Messaging API ist ein wahrer Feuerwehrschlauch der Ereignisse, diese Parsing Funktion  antwortet nur, wenn die Nachricht an den BOT gewandt ist, in Abhängigkeit von seiner ID
	"""
	output_list=slack_rtm_output
	if output_list and len(output_list) >0:
		for output in output_list:
			if output and 'text' in output and AT_BOT in output['text']:
				#gibt den text nach dem @ aus, ohne leerzeichen
				return output['text'].split(AT_BOT)[1].strip().lower(), output ['channel']
	return None, None



if __name__=="__main__":
	READ_WEBSOCKET_DELAY=0.1 #1 Sekunde delay
	if slack_client.rtm_connect():
		print("SlackBot verbunden und am RENNEN!")
		while True:
			command, channel = parse_slack_output(slack_client.rtm_read())
			if command and channel:
				handle_command(command, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Verbindung fehlgeschlage, da stimmt am end was mit dem TOKEN oder der ID nicht :(")



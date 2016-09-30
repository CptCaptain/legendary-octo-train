import os
import time
import requests
import json
import urllib.request
from slackclient import SlackClient


#Lookup für Bot ID und so

BOT_NAME= 'servitor'

SLACK_BOT_TOKEN = 'xoxb-84060539537-XXXXXXXXXXXXXXXXXXXXXXXXXXX'


#instanziiere Slack
slack_client = SlackClient(SLACK_BOT_TOKEN)

if __name__ == "__main__":
        api_call = slack_client.api_call("users.list")
        if api_call.get('ok'):
                # retrieve all users so we can find our bot
                users = api_call.get('members')
                for user in users:
                        if 'name' in user and user.get('name') == BOT_NAME:
                                BOT_ID=user.get('id')
                                print("Die Bot ID für '" + user['name'] + "' ist " + user.get('id'))

#constants
AT_BOT="<@" + BOT_ID +">"
EXAMPLE_COMMAND = "tu"
PRIME = "prim"
WETTER = "wetter"
CLOCK = "uhr"
CITY = "Wiesbaden"
client = SlackClient(SLACK_BOT_TOKEN)
#Funktionen zum parsen von Slack output und den handle commands und so
def handle_command(command, channel):
	"""
		Empfängt Befehle für den Bot und ermittelt, ob sie valide sind, den rest kannst du dir wahrscheinlich denken
	"""
	response="Wat meinste? Nimm den  *" + EXAMPLE_COMMAND + "* Befehl, du Spasti"
#	if client.rtm_connect():
#		last_read = client.rtm_read()
#		if last_read:
#			try:
#				parsed = last_read
#				if parsed and 'berlin' in parsed:
#					CITY="Berlin"
#				print(parsed)
#			except:
#				pass
	if command.startswith(EXAMPLE_COMMAND):
		response="Alles klar, da fehlt aber noch ein bissl code, meinste nicht auch?"
		slack_client.api_call("chat.postMessage", channel=channel,
				text=response, as_user=True)
	if command.startswith(PRIME):
		i=1
		while i<50:
			slack_client.api_call("chat.postMessage", channel=channel, text=i, as_user=True)
			i=i+2
	if WETTER in command:
		#Wetterversuch, mal schauen was drauss wirt
		openweather_api='442c26ca8ed7eec9212e6beb25720d27'
		print(command)
		split=command.split()
		for x in split:
			CITY=x
			if CITY=='wetter':
				print('wetter, aber das bleibt unter uns ;)')
			else:
				print(CITY)
				line=urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast/city?q=' + CITY +',de&APPID=442c26ca8ed7eec9212e6beb25720d27').read()
				jdata=json.loads(line.decode('utf-8'))
				if 'error' in jdata:
					print('FEHLER! FEHLER! FEHLER!')
				else:
					#hier werden die einzelnen dinge die einen interessieren aus dem
					#riesigen json extrahiert, und im anschluss dargestellt.
					Main_Weather=jdata["list"][0]["weather"]
					Weather=Main_Weather[0]["description"]
					Wind=jdata["list"][0]["wind"]
					Speed=Wind["speed"]
					Angle=Wind["deg"]
					Main_Temp=jdata["list"][0]["main"]
					Temp=Main_Temp["temp"]
					Temp_C=int(Temp)-275.13
					Pressure=jdata["list"][0]["clouds"]
					i=('In ' + str.capitalize(CITY)+ ', there\'s ' + str(Weather) + ' at ' + str(Temp) + 'K (' + str(Temp_C) + '°C) with a windspeed of ' + str(Speed) + 'km/h coming from ' + str(Angle) + '°N.')
					print('Wetter')
				slack_client.api_call("chat.postMessage", channel=channel, text=i, as_user=True)
	if CLOCK in command:
		i=time.strftime("It's %A, the %d of %B %Y, %H:%M:%S ", time.localtime())
		slack_client.api_call("chat.postMessage", channel=channel, text=i, as_user=True)
		print('Uhrzeit')
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
		print("Verbindung fehlgeschlagen, da stimmt am end was mit dem TOKEN oder der ID nicht :(")



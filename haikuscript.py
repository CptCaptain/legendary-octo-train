#requires: apiclient, --upgrade google-api-python-client, oauth2client

import praw
import httplib2
import os
import sys
import datetime

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

#Youtube OAuth
CLIENT_SECRETS_FILE = "client_secret_***.apps.googleusercontent.com.json"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_READ_WRITE_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

month = datetime.datetime.now()

# This code creates a new, public playlist in the authorized user's channel.
playlists_insert_response = youtube.playlists().insert(
  part="snippet,status",
  body=dict(
    snippet=dict(
      title="YouTube Haikus " + month.strftime("%B"),
      description="Automated Youtube haikus, only reddits 150 best of the month! created with the YouTube API v3"
    ),
    status=dict(
      privacyStatus="public"
    )
  )
).execute()
print ("New playlist id: %s" + playlists_insert_response["id"])

#This should add a Video to the playlist
def add_video_to_playlist(youtube,videoID,playlistID):
      add_video_request=youtube.playlistItems().insert(
      part="snippet",
      body={
            'snippet': {
              'playlistId': playlist_ID, 
              'resourceId': {
                      'kind': 'youtube#video',
                  'videoId': videoID
                }
            #'position': 0
            }
    }
).execute()


#Grab the top 150 youtubehaikus of the month's urls 
r=praw.Reddit(user_agent='python:YouTube_Haiku:v0.1 (by /u/***)')
submissions = r.get_subreddit('youtubehaiku').get_top_from_month(limit=150)
for item in submissions:
    pre_url = item.url
    #print('preurl'+pre_url)
    if '&feature=' in pre_url:
        urlo = pre_url.split('&feature=youtu.be')
        #print('urlo'+str(urlo))
        url=urlo[0]
    else:
        url=pre_url
    #print('url'+str(url))
    if url.startswith('https://youtu.be'):
        split = url.split('.be/')
        if '?t=' in url:
            split = split[1].split('?t=')
            #print('split'+str(split))
            video_ID=split[0]
        else:
            #print('split'+str(split))
            video_ID=split[1]
    else:
       # print(str(item) + str(item.url))
        split = url.split('?v=')
        try:
            video_ID = split[1]
        except:
            print('I couldn\'t handle the url! :(')
            pass
    playlist_ID = playlists_insert_response["id"].strip('%')
    try:
        add_video_to_playlist(youtube, video_ID, playlist_ID)
        print('Video \"' + str(item) + '\" erfolgreich hinzugefuegt')
    except:
        print('Video ID nicht gefunden!')
        pass

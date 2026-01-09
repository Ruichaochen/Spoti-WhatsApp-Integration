#import urllib.parse
import base64
import requests
#import subprocess
import os
import time
import threading
import traceback
#from requests_oauthlib import OAuth2Session

# Constants for the spotify API
CLIENT_ID = ""
CLIENT_SECRET = ""
REFRESH_TOKEN = ""
redirect_uri = ""
token_url = "https://accounts.spotify.com/api/token"
authorization_base_url = 'https://accounts.spotify.com/authorize'
scope = ["user-read-playback-state", "user-modify-playback-state"]

try:
    open("config.json","r")
    configpresent = True
except Exception as Error:
    configpresent = False

if configpresent:
    f = open("config.json","r")
    for i in f.read().splitlines():
        exec(i) # Again, I would not use exec today, when safe alternatives exist.
else:
    print("Please correctly set up your configuration.")

##spotify = OAuth2Session(CLIENT_ID, scope=scope, redirect_uri=redirect_uri)
##authorization_url, state = spotify.authorization_url(authorization_base_url)
##print("Go auth at:", authorization_url)
##redirect_response = input("response:")
##from requests.auth import HTTPBasicAuth
##auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
##
##token = spotify.fetch_token(token_url,auth=auth,authorization_response=redirect_response)
##print(token)
##try:
##    a = requests.get("https://api.spotify.com/v1/me/player/currently-playing",headers={"Authorization" : "Bearer " + token["access_token"]})
##    print(a.json())
##except:
##    print("Not listening to a song")

def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except Exception:
            traceback.print_exc()
        next_time += (time.time() - next_time) // delay * delay + delay

def refresh():
        refresh_params = {
            'grant_type': 'refresh_token',
            'refresh_token': REFRESH_TOKEN,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        refreshed = requests.post(token_url, data = refresh_params)
        global token
        token = refreshed.json()["access_token"]
refresh()
threading.Thread(target=lambda: every(3000, refresh)).start()

def getsong():
        try:
            song = requests.get("https://api.spotify.com/v1/me/player/currently-playing",headers={"Authorization" : "Bearer " + token})
            song = song.json()
            artists = ""
            for i in song["item"]["artists"]:
              artists = artists + i["name"] + ", "
            #print(song["item"]["album"]["images"][0]["url"])
            seconds, milliseconds = divmod(song["progress_ms"], 1000)
            minutes, seconds = divmod(seconds, 60)
            if len(str(seconds)) == 1:
                    seconds = "0" + str(seconds)
            songseconds, songmilliseconds = divmod(song["item"]["duration_ms"], 1000)
            songminutes, songseconds = divmod(songseconds, 60)
            if len(str(songseconds)) == 1:
                    songseconds = "0" + str(songseconds)
            return (song["item"]["name"],"by", artists[:-2], "" + str(minutes) + ":" + str(seconds) + "/"+ str(songminutes)+":"+str(songseconds))
        except ValueError as error:
            return None
        except Exception as error:
          print(error)

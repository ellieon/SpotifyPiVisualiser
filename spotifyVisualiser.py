import spotipy
import spotipy.util as util
import json
import time
import sys

def current_song(spotify, print_name=False):
    currentTrack = spotify.currently_playing()
    if print_name:
        print(currentTrack['item']['name'])
    return currentTrack['item']['id']
    
REQUIRED_PERMISSION_SCOPE = 'user-read-playback-state user-modify-playback-state'
username = sys.argv[1]

token = util.prompt_for_user_token(username, REQUIRED_PERMISSION_SCOPE)

spotify = spotipy.Spotify(auth=token)
currentTrack = current_song(spotify, True)
startTrack = currentTrack
analysis = spotify.audio_analysis(currentTrack)

while currentTrack == startTrack:
    print(spotify.currently_playing()['progress_ms'])
    time.sleep
    currentTrack = current_song(spotify)




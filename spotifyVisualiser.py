import spotipy
import spotipy.util as util
import json
import time
import sys
from songState import SongState

REQUIRED_PERMISSION_SCOPE = 'user-read-playback-state user-modify-playback-state'
def getToken():
    username = sys.argv[1]
    token = util.prompt_for_user_token(username, REQUIRED_PERMISSION_SCOPE)
    return token
    
if __name__ == "__main__":
    songState = SongState(getToken())
    songState.run()
import spotipy.util as util
import sys
from songAnalyser import SongAnalyser

REQUIRED_PERMISSION_SCOPE = 'user-read-playback-state user-modify-playback-state'

def getToken():
    username = sys.argv[1]
    token: str = util.prompt_for_user_token(username, REQUIRED_PERMISSION_SCOPE)
    return token
    
if __name__ == "__main__":
    songState = SongAnalyser(getToken(), False)
    songState.run()
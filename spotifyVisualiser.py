import spotipy.util as util
import sys
from songAnalyser import SongAnalyser
import cv2 as cv
import numpy as np

REQUIRED_PERMISSION_SCOPE = 'user-read-playback-state user-modify-playback-state'
WINDOW_NAME = 'Beat Visualiser'
COLOUR_MAX = 255
img = np.zeros((50,50,3), np.uint8)
currentColour = 0

def getToken():
    username = sys.argv[1]
    token: str = util.prompt_for_user_token(username, REQUIRED_PERMISSION_SCOPE)
    return token

def onEvent(state, type):
    if type == 'beats':
        global currentColour

        pitches = songState.currentSignatures['segments']['pitches']

        r = int(COLOUR_MAX * np.mean(pitches[0:3]))
        g = int(COLOUR_MAX * np.mean(pitches[4:7]))
        b = int(COLOUR_MAX * np.mean(pitches[8:11]))

        currentColour = r << 16 | g << 8 | b
        
def onDraw():
    if cv.getWindowProperty(WINDOW_NAME, cv.WND_PROP_VISIBLE) == 1:
        if songState.currentSignatures['beats'] == None:
            return
        
        global img
    
        segmentProgress = songState.songProgress / 1000 - songState.currentSignatures['segments']['start']
        segmentEnd = songState.nextSignatures['segments']['start'] - songState.currentSignatures['segments']['start']

        decay = 1 - (segmentProgress / segmentEnd)

        r = ((currentColour & 0xFF0000) >> 16) * decay
        g = ((currentColour & 0x00FF00) >> 8) * decay
        b = (currentColour & 0x0000FF) * decay

        img[:,0:50] = (b,g,r)     

        cv.imshow(WINDOW_NAME, img)
        cv.waitKey(1)
    else:
        songState.stop()

if __name__ == "__main__":
    cv.namedWindow(WINDOW_NAME, cv.WINDOW_NORMAL)
    songState = SongAnalyser(getToken(), False)
    songState.onSignatureEvent(onEvent)
    songState.onDraw = onDraw
    songState.run()

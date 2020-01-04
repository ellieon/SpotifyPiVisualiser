import spotipy.util as util
import sys
from songAnalyser import SongAnalyser
import cv2 as cv
import numpy as np

REQUIRED_PERMISSION_SCOPE = 'user-read-playback-state user-modify-playback-state'
COLOUR_MAX = 255
img = np.zeros((50,50,3), np.uint8)
currentColour = 0
targetColour = 0

def getToken():
    username = sys.argv[1]
    token: str = util.prompt_for_user_token(username, REQUIRED_PERMISSION_SCOPE)
    return token

def onEvent(state, type):
    if type == 'beats':
        global currentColour
        global targetColour

        pitches = songState.currentSignatures['segments']['pitches']

        r = int(COLOUR_MAX * np.mean(pitches[0:3]))
        g = int(COLOUR_MAX * np.mean(pitches[4:7]))
        b = int(COLOUR_MAX * np.mean(pitches[8:11]))


        currentColour = r << 16 | g << 8 | b

    return
        
def onDraw():
    if songState.currentSignatures['beats'] == None:
        return
    segmentProgress = songState.songProgress / 1000 - songState.currentSignatures['beats']['start']
    segmentEnd = songState.nextSignatures['beats']['start'] - songState.currentSignatures['beats']['start']

    percent = 1 - (segmentProgress / segmentEnd)
    global currentColour


    r = ((currentColour & 0xFF0000) >> 16) * percent
    g = ((currentColour & 0x00FF00) >> 8) * percent
    b = (currentColour & 0x0000FF) * percent

    print(r)
    print(g)
    print(b)

    print('=========')


    img[:,0:50] = (b,g,r)     

    cv.imshow('Beat Visualiser', img)
    cv.waitKey(1)

if __name__ == "__main__":
    songState = SongAnalyser(getToken(), False)
    songState.onSignatureEvent(onEvent)
    songState.onDraw = onDraw
    songState.run()

import spotipy
import time
import json
import cv2 as cv
import numpy as np
class SongAnalyser:
    MS_PER_SECOND = 1000
    DEFAULT_TICKS_PER_SECOND = 60
    SIGNATURE_TYPES = {'bars', 'beats', 'tatums', 'sections', 'segments'}
    

    
    def __init__(self, token: str, debug: bool = False):
        """
        Constructs a new SongAnalyser
    
        Parameters
        -----------
        token: `str`
            Authentication token for a valid Spotify user
        debug: `bool`, optional
            Whether debug messages should be printed (default is false)
        """
        self.spotify = spotipy.Spotify(auth=token)
        self.analysis = None
        self.ticksPerSecond = self.DEFAULT_TICKS_PER_SECOND
        self.debug = debug
        self.analysedSong = None
        self.currentSystemTime = time.time()
        self.isPlaying = False
        self.ticksSinceLastUpdate = 0
        self.currentBeat = None

    
    def run(self):
        """Starts this Song Analyser, creating a loop to keep track of current song position"""
        self.analyseSong()
        while True:
            self.mainLoop()
            
    def mainLoop(self):
        if self.isPlaying:
            self.updateTime()
            self.updateSongState()
            time.sleep(1 / self.ticksPerSecond)
        #Currently this will update every 60 ticks, not strictly every second if there is any sort of delay between ticks.
        if(self.ticksSinceLastUpdate % (self.ticksPerSecond * 4) == 0):
            self.analyseSong()
        self.ticksSinceLastUpdate+=1
        img = np.zeros((512,512,3), np.uint8)
        cv.rectangle(img, (0,0), (100,100), (255,255,255))
        cv.imshow('', img)

    def updateTime(self):
        """Determines the current position in the currently playing song by taking the delta since the last recorded system time vs now"""
        delta = time.time() - self.currentSystemTime
        self.currentSystemTime += delta
        self.songProgress += int(delta * self.MS_PER_SECOND)
        if self.debug:
            print(self.songProgress)
            
    def updateSongState(self):
        #Todo, binary search the array damnit
        songTimeSeconds = self.songProgress / 1000
        for type in self.SIGNATURE_TYPES:
            signatures = self.analysis[type]
            signature = 0
            while signature < len(signatures):
                signatureNow = signatures[signature]
                signatureNext = signatures[signature + 1]
                if((signatureNow['start'] < songTimeSeconds) & (songTimeSeconds < signatureNext['start'])) :
                    if not self.currentBeat or self.currentBeat['start'] != signatureNow['start']:
                        self.currentBeat = signatureNow
                        self.onSegmentChange(type, signatureNow)
                    break
                signature+=1


    def analyseSong(self):
        """
        Checks the current song ID vs the Spotify Connect reported current song ID.\n
        If a change has occured, grab the song analysis data for the song.\n
        Updates the song progress timer to the currently reported Spotify Connect time\n
        
        TODO: This really needs to be done on it's own thread as the REST calls to the Spotify Web API can introduce delay we really don't want
        """
        #This needs to be done on a thread at a regular interval
        currentTrack = self.spotify.currently_playing()
        if currentTrack:
            currentId = currentTrack['item']['id']
            preCallTime = time.time()
            currentlyplaying = self.spotify.currently_playing()
            self.songProgress = currentlyplaying['progress_ms'] - 1000
            self.isPlaying = currentlyplaying['is_playing'] 
            if currentId != self.analysedSong:
                if self.debug:
                    print(currentTrack['item']['name'])
                    print('Analysing')
                self.analysedSong = currentId
                self.analysis = self.spotify.audio_analysis(self.analysedSong)
            
            
    def onSegmentChange(self, segmentType: str, segment):
        if segmentType == 'beats':
            print(segmentType)
            print(segment['confidence'])
        
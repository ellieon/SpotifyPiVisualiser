import spotipy
import time
import json
import threading

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
        self.currentSignatures = {}
        self.nextSignatures = {}
        self.songProgress = 0
        self.onEvent = None
        self.onDraw = None
        self.resetTime = False
        self.t1 = threading.Thread(target=self.analyseSongLoop)
        self.exit = False

        for type in self.SIGNATURE_TYPES:
            self.currentSignatures[type] = None
            self.nextSignatures[type] = None

    def onSignatureEvent(self, event):
        self.onEvent = event

    def onDraw(self, onDraw):
        self.onDraw = onDraw

    def run(self):
        """Starts this Song Analyser, creating a loop to keep track of current song position"""
        self.t1.start()
        while not self.exit:
            self.mainLoop()
            
    def mainLoop(self):
        if self.isPlaying:
            self.updateTime()
            self.updateSongState()
            self.onDraw()
            time.sleep(1 / self.ticksPerSecond)
        #Currently this will update every 60 ticks, not strictly every second if there is any sort of delay between ticks.
        self.ticksSinceLastUpdate+=1
        

    def updateTime(self):
        """Determines the current position in the currently playing song by taking the delta since the last recorded system time vs now"""
        if self.resetTime:
                self.spotify.seek_track(0)
                self.currentSystemTime = time.time()
                self.songProgress = 0
                self.resetTime = False
        else:
            delta = time.time() - self.currentSystemTime
            self.currentSystemTime += delta
            self.songProgress += delta * self.MS_PER_SECOND
        if self.debug:
            print(self.songProgress)
            
    def updateSongState(self):
        #Todo, binary search the array damnit
        songTimeSeconds = self.songProgress / 1000
        if self.analysis == None:
            return
        for type in self.SIGNATURE_TYPES:
            signatures = self.analysis[type]
            signature = 0
            while signature < len(signatures):
                signatureNow = signatures[signature]
                if signature == len(signatures) - 1:
                    signatureNext = signatures[signature]
                else:
                    signatureNext = signatures[signature + 1] 
                if((signatureNow['start'] < songTimeSeconds) & (songTimeSeconds < signatureNext['start'])) :
                    if self.currentSignatures[type] == None or (self.currentSignatures[type]['start'] != signatureNow ['start']):
                        self.currentSignatures[type] = signatureNow
                        self.nextSignatures[type] = signatureNext
                        self.onSegmentChange(type, signatureNow)
                    break
                signature+=1


    def analyseSongLoop(self):
        """
        Checks the current song ID vs the Spotify Connect reported current song ID.\n
        If a change has occured, grab the song analysis data for the song.\n
        Updates the song progress timer to the currently reported Spotify Connect time\n
        """
        while not self.exit:
            currentTrack = self.spotify.currently_playing()
            if currentTrack:
                currentId = currentTrack['item']['id']
                preCallTime = time.time()
                currentlyplaying = self.spotify.currently_playing()
                self.isPlaying = currentlyplaying['is_playing'] 

                if currentId != self.analysedSong:
                    if self.debug:
                        print(currentTrack['item']['name'])
                        print('Analysing')
                    self.analysedSong = currentId
                    self.resetTime = True
                    self.analysis = self.spotify.audio_analysis(self.analysedSong)

            time.sleep(.1)
                
    def onSegmentChange(self, segmentType: str, segment):
        self.onEvent(self, segmentType)

    def stop(self):
        self.exit = True
        
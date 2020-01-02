import spotipy
import time
    
class SongState:
    MS_PER_SECOND = 1000
    DEFAULT_TICKS_PER_SECOND = 60
    
    def __init__(self, token, debug = False):
        self.spotify = spotipy.Spotify(auth=token)
        self.currentSongTime = None
        self.analysis = None
        self.ticksPerSecond = self.DEFAULT_TICKS_PER_SECOND
        self.debug = debug
        self.analysedSong = None
        self.currentSystemTime = time.time()

    def run(self):
        self.analyseSong()
        currentTrack = self.analysedSong
        i = 0
        while True:
            self.updateTime()
            time.sleep(1 / self.ticksPerSecond)
            i+=1
            if(i % self.ticksPerSecond == 0):
                self.analyseSong()

    def updateTime(self):
        delta = time.time() - self.currentSystemTime
        self.currentSystemTime += delta
        self.songProgress += int(delta * self.MS_PER_SECOND)
        if self.debug:
            print(self.songProgress)
            
    #This needs to be done on a thread at a regular interval
    def analyseSong(self):
        currentTrack = self.spotify.currently_playing()
        currentId = currentTrack['item']['id']
        if self.debug:
            print(currentTrack['item']['name'])
        if currentId != self.analysedSong:
            if self.debug:
                print('Analysing')
            self.analysedSong = currentId
            self.analysis = self.spotify.audio_analysis(self.analysedSong)
        self.songProgress = self.spotify.currently_playing()['progress_ms']
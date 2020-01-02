import spotipy
import time
    
class SongAnalyser:
    MS_PER_SECOND = 1000
    DEFAULT_TICKS_PER_SECOND = 60
    
    def __init__(self, token: str, debug: bool = False):
        """
        Constructs a new SongAnalyser
    
        Parameters
        -----------
        token: `str`
            The token object from spotipy.util.prompt_for_user_token()
        debug: `bool`, optional
            Whether debug messages should be printed (default is false)
        """
        self.spotify = spotipy.Spotify(auth=token)
        self.currentSongTime = None
        self.analysis = None
        self.ticksPerSecond = self.DEFAULT_TICKS_PER_SECOND
        self.debug = debug
        self.analysedSong = None
        self.currentSystemTime = time.time()

    
    def run(self):
        """Starts this Song Analyser, creating a loop to keep track of current song position"""
        self.analyseSong()
        currentTrack = self.analysedSong
        ticksSinceLastUpdate = 0
        while True:
            self.updateTime()
            time.sleep(1 / self.ticksPerSecond)
            ticksSinceLastUpdate+=1
            #Currently this will update every 60 ticks, not strictly every second if there is any sort of delay between ticks.
            if(ticksSinceLastUpdate % self.ticksPerSecond == 0):
                self.analyseSong()

    def updateTime(self):
        """Determines the current position in the currently playing song by taking the delta since the last recorded system time vs now"""
        delta = time.time() - self.currentSystemTime
        self.currentSystemTime += delta
        self.songProgress += int(delta * self.MS_PER_SECOND)
        if self.debug:
            print(self.songProgress)
            

    def analyseSong(self):
        """
        Checks the current song ID vs the Spotify Connect reported current song ID.\n
        If a change has occured, grab the song analysis data for the song.\n
        Updates the song progress timer to the currently reported Spotify Connect time\n
        
        TODO: This really needs to be done on it's own thread as the REST calls to the Spotify Web API can introduce delay we really don't want
        """
        #This needs to be done on a thread at a regular interval
        currentTrack = self.spotify.currently_playing()
        currentId = currentTrack['item']['id']
        if currentId != self.analysedSong:
            if self.debug:
                print(currentTrack['item']['name'])
                print('Analysing')
            self.analysedSong = currentId
            self.analysis = self.spotify.audio_analysis(self.analysedSong)
        self.songProgress = self.spotify.currently_playing()['progress_ms']
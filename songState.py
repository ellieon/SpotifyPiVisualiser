import spotipy
import time
    
class SongState:
    MS_PER_SECOND = 1000
    
    def __init__(self, token):
        self.spotify = spotipy.Spotify(auth=token)
        self.currentSongTime = None
        self.currentProcessorTime = None
        self.ticksPerSecond = 60
            
    def current_song(self, print_name=False):
        currentTrack = self.spotify.currently_playing()
        if print_name:
            print(currentTrack['item']['name'])
        return currentTrack['item']['id']

    def run(self):
        currentTrack = self.current_song(True)
        startTrack = currentTrack
        analysis = self.spotify.audio_analysis(currentTrack)
        
        self.songProgress = self.spotify.currently_playing()['progress_ms']
        self.currentSystemTime = time.time()
        
        while currentTrack == startTrack:
            delta = time.time() - self.currentSystemTime
            self.currentSystemTime += delta
            self.songProgress += int(delta * self.MS_PER_SECOND)

            print(self.songProgress)
            time.sleep(1 / self.ticksPerSecond)


            
        
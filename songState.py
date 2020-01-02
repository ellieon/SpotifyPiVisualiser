import spotipy
import time


class SongState:
    
    def __init__(self, token):
        self.spotify = spotipy.Spotify(auth=token)
            
    def current_song(self, print_name=False):
        currentTrack = self.spotify.currently_playing()
        if print_name:
            print(currentTrack['item']['name'])
        return currentTrack['item']['id']

    def run(self):
        currentTrack = self.current_song(True)
        startTrack = currentTrack
        analysis = self.spotify.audio_analysis(currentTrack)

        while currentTrack == startTrack:
            print(self.spotify.currently_playing()['progress_ms'])
            currentTrack = self.current_song()  
            time.sleep(1)
        
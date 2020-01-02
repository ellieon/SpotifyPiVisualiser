LED Visualiser for RaspberryPi to take users currently playing Spotify song and calculate an output RGB ready to send over GPIO
---
#Usage 
The following environment variables must be defined for this application to run (The client ID and Secret must be obtained by creating a new app in the Spotify Developer area)
```
export SPOTIPY_CLIENT_ID='<client_id>'
export SPOTIPY_CLIENT_SECRET='<client_secret>'
export SPOTIPY_REDIRECT_URI='<redirect_url>'
```

After setting these up just run the following command
`python3 spotifyVisualiser.py <username>`
Where <username> is the Spotify username you wish to log in with.
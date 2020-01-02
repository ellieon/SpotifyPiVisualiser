Spotify Visualiser
---
# Description
Visualiser application that grabs information from a given user's currently playing Spotify song and generate visualisation data in realtime for it.

# Dependencies
Spotify Visualiser is written for Python3 using the spotipy library (https://github.com/plamere/spotipy), the current version of spotipy on pip is not up to date with the latest version, so run the following to grab the library direct from source:

`pip3 install git+https://github.com/plamere/spotipy.git --upgrade`

# Usage 
The following environment variables must be defined for this application to run (The client ID and Secret must be obtained by creating a new app in the Spotify Developer area), redirect URL can be anything:

```
export SPOTIPY_CLIENT_ID='<client_id>'
export SPOTIPY_CLIENT_SECRET='<client_secret>'
export SPOTIPY_REDIRECT_URI='<redirect_url>'
```

After setting these up just run the following command:

`python3 spotifyVisualiser.py <username>`

Where <username> is the Spotify username you wish to log in with.
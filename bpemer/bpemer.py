import os
from yaml_settings import YAMLSettings
from colorama import init, Fore, Back, Style

class SimpleLine(object):
    def __init__(self, text, color=Fore.WHITE, background=Back.BLACK):
        print
        print(background + color + ' ' + text + ' ' + Style.RESET_ALL)
        print

import spotipy
import spotipy.util as util

class AccessSettings(YAMLSettings):
    YAML = os.path.join(
        os.path.expanduser('~'),
        '.bpemer.yml'
    )

    def __init__(self):
        SimpleLine('Accessing yaml settings', Fore.BLACK, Back.GREEN)
        self.load(self.YAML)
        require = {
            'echonet': {
                'api_key': 'API Key',
                'consumer_key': 'Consumer Key',
                'shared_secret': 'Shared Secret',
            },
            'spotify': {
                'client_id': 'Client ID',
                'client_secret': 'Client Secret',
                'redirect_uri': 'Redirect URI',
                'username': 'Spotify Username'
            }
        }
 
        for k in require.keys():
            if not k in self.data.keys():
                self.data[k] = {}
            for j in require[k].keys():
                if not j in self.data[k].keys():
                    self.data[k][j] =  raw_input(
                        Fore.GREEN + 
                        "Please enter your %s %s: " % (
                            k,
                            require[k][j]
                        ) + 
                        Style.RESET_ALL
                    )

        if not 'token' in self.data['spotify'].keys():
            token = util.prompt_for_user_token(
                self.data['spotify']['username'],
                client_id=self.data['spotify']['client_id'],
                client_secret=self.data['spotify']['client_secret'],
                redirect_uri=self.data['spotify']['redirect_uri'],
                scope='playlist-read-private'
            )
            self.data['spotify']['token'] = '%s' % token
        self.save()

settings = AccessSettings()
sp = spotipy.Spotify(auth=settings.data['spotify']['token'])

class Playlists:
    @classmethod
    def iterate_tracks(cls, tracks):
        ts = []
        for track in tracks:
            t = {
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name']
            }
            ts.append(t)
        return t

    def __init__(self, username):
        playlists = sp.user_playlists(username)
        self.data = []
        for playlist in playlists['items']:
            p = {
                'id': playlist['id'],
                'name': playlist['name'],
                'total_tracks': playlist['tracks']['total'],
            }
            results = sp.user_playlist(
                username,
                playlist['id'],
                fields="tracks,next"
            )
            
            tracks = results['tracks']
            p['tracks'] = []
            p['tracks'].append(Playlists.iterate_tracks(tracks))
            while tracks['next']:
                tracks = sp.next(tracks)
                p['tracks'].append(Playlists.iterate_tracks(tracks))
            self.data.append(p)

playlists = Playlists(settings.data['spotify']['username'])
print playlists.data
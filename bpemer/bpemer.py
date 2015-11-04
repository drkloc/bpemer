from colorama import Fore, Back, Style
from tabulate import tabulate
from utils import SimpleLine

from access import AccessSettings
settings = AccessSettings()

import spotipy
sp = spotipy.Spotify(auth=settings.data['spotify']['token'])

class Playlists:
    def __init__(self, username):
        playlists = sp.user_playlists(username)
        playlists = playlists['items']
        self.data = []
        i = 1
        for playlist in playlists:
            p = {
                'i': '%s)' % i,
                'name': playlist['name'],
                'id': playlist['id'],
                'owner': '%s' % playlist['owner']['id']
            }
            i += 1
            self.data.append(p)

    def tabulate(self):
        h = self.data[0].keys()
        o = [[t[k] for k in t.keys()] for t in self.data]
        print tabulate(o, headers=h)
        print

    def buildTracks(self, i):
        p = self.data[i]
        t = Tracks(
            p['name'],
            p['owner'],
            p['id']
        )
        return t

class Tracks:
    @classmethod
    def iterate_tracks(cls, tracks):
        ts = []
        for track in tracks:
            track = track['track']
            t = {
                'uri': track['uri'],
                'artist': track['artists'][0]['name'],
                'name': track['name'],
            }
            ts.append(t)
        return ts

    def __init__(self, name, owner, id):
        self.name = name
        self.owner = owner
        self.id = id
        results = sp.user_playlist(self.owner, self.id, fields="tracks,next")
        tracks = results['tracks']
        self.tracks = Tracks.iterate_tracks(tracks['items'])
        while tracks['next']:
            tracks = sp.next(tracks)
            self.tracks = self.tracks + Tracks.iterate_tracks(tracks['items'])

    def tabulate(self):
        SimpleLine(self.name, Fore.BLACK, Back.GREEN)
        h = self.tracks[0].keys()
        o = [[t[k] for k in t.keys()] for t in self.tracks]
        print tabulate(o, headers=h)
        print

playlists = Playlists(settings.data['spotify']['username'])
playlists.tabulate()
i = raw_input(Fore.GREEN + 'Choose playlist to analize: ' + Style.RESET_ALL)
i = int(i) - 1
tracks = playlists.buildTracks(i)
tracks.tabulate()

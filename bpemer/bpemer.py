from colorama import Fore, Back, Style
from tabulate import tabulate
from utils import SimpleLine
import pyen

from access import AccessSettings
settings = AccessSettings()

import spotipy
sp = spotipy.Spotify(auth=settings.data['spotify']['token'])
en = pyen.Pyen(settings.data['echonet']['api_key'])

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
                'meta': {},
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
        for i in range(len(self.tracks)):
            track = self.tracks[i].copy()
            tid = track['uri']
            try:
                response = en.get(
                    'song/profile', 
                    track_id = tid,
                    bucket= ['audio_summary', 'song_hotttnesss', 'artist_hotttnesss']
                )
                if response['status']['code'] == 0:
                    song = response['songs'][0]
                    for k in song['audio_summary'].keys():
                        if k in ['tempo']:
                          self.tracks[i]['meta'][k] = song['audio_summary'][k]  
            except:
                pass
            

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

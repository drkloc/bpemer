import os
from yaml_settings import YAMLSettings
from utils import SimpleLine
from colorama import Fore, Back, Style
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
        token = util.prompt_for_user_token(
            self.data['spotify']['username'],
            client_id=self.data['spotify']['client_id'],
            client_secret=self.data['spotify']['client_secret'],
            redirect_uri=self.data['spotify']['redirect_uri'],
            scope='playlist-read-private'
        )
        self.data['spotify']['token'] = '%s' % token
        self.save()

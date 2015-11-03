import yaml

try:
    from collections import UserDict
except ImportError:
    # Python 2..
    from UserDict import UserDict

__all__ = ['YAMLSettings']

class YAMLSettings(UserDict):
    def load(self, filename=None):
        if filename or not getattr(self, 'filename', None):
            self.filename = filename

        if not self.filename:
            raise ValueError('`filename` must be set.')

        try:
            f = open(self.filename, 'r')
            data = yaml.load(f)
        except IOError:
            data = {}

        if data is None:
            data = {}

        if not isinstance(data, dict):
            raise TypeError(
                'Data was replace with non dict type, got: {}'.format(
                    type(data)))
        self.data = data

    def save(self, filename=None, sort_keys=False):
        if filename or not getattr(self, 'filename', None):
            self.filename = filename

        if not self.filename:
            raise ValueError('`filename` must be set.')

        with open(self.filename, 'w') as f:
            yaml.dump(self.data, f, indent=4)

    @classmethod
    def from_file(cls, filename):
        settings = cls()
        settings.load(filename)
        return settings

    def set(self, option, value):
        self.data[option] = value

    def setsave(self, option, value, filename=None):
        self.set(option, value)
        self.save(filename=filename)

# Package: kuwtg.config
import configparser
import os.path


class Configuration(object):

    DEFAULT_CONFIG_FILE = "~/.config/kuwtg/kuwtg.conf"

    def __init__(self):
        config_parser = configparser.ConfigParser()
        config_file = os.path.expanduser(self.DEFAULT_CONFIG_FILE)
        if not os.path.exists(config_file):
            self._initialize_config(config_file)
        config_parser.read(config_file)
        self._access_token = config_parser.get('tokens', 'access-token')

    def _initialize_config(self, config_file):
        config_dir = os.path.dirname(config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        config_parser = configparser.ConfigParser()
        config_parser['tokens'] = {'access-token': '<your-access-token-here>'}
        with open(config_file, 'w') as config:
            config_parser.write(config)

    @property
    def access_token(self):
        return self._access_token

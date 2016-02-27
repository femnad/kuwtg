import configparser
import os.path


class Configuration(object):

    DEFAULT_CONFIG_FILE = "~/.config/kuwtg/kuwtg.conf"
    DEFAULT_LOG_FILE = "~/.local/share/kuwtg/logs/kuwtg.log"

    DEFAULTS = {
        'tokens':
        {'access-token': '<your-access-token-here>'},
        'application':
        {'log-file': os.path.expanduser(DEFAULT_LOG_FILE)}
    }

    def __init__(self):
        config_parser = configparser.ConfigParser()
        config_file = os.path.expanduser(self.DEFAULT_CONFIG_FILE)
        if not os.path.exists(config_file):
            self._initialize_config(config_file)
        config_parser.read(config_file)
        self._access_token = config_parser.get('tokens', 'access-token')
        self._log_file = config_parser.get('application', 'log-file')

    def _initialize_config(self, config_file):
        config_dir = os.path.dirname(config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        config_parser = configparser.ConfigParser()
        for section, section_items in self.DEFAULTS.items():
            config_parser[section] = section_items
        with open(config_file, 'w') as config:
            config_parser.write(config)

    @property
    def access_token(self):
        return self._access_token

    @property
    def log_file(self):
        return self._log_file

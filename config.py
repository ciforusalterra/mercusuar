import os
from configparser import ConfigParser

config = ConfigParser()

config.read(os.getenv('CONFIG', 'etc/config.ini'))

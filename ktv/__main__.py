import os
import sys
import argparse

from six.moves import configparser

__all__ = []
NAME = 'k'

def load_config():
    config = configparser.ConfigParser()
    
    HOME = os.path.expanduser('~')
    XDG_CONFIG_HOME = os.getenv('XDG_CONFIG_HOME', os.path.join(HOME, '.config'))
    config_paths = [
        os.path.join(XDG_CONFIG_HOME, NAME, NAME + '.cfg'),
        os.path.join(HOME, '.'+NAME)
    ]

    for config_path in config_paths:
        if os.path.exists(config_path):
            config.read(config_path)
            break

    defaults = {}
    if config.has_section(NAME):
        defaults = dict(config.items(NAME))

    return defaults

def command_line():
    
    parser = argparse.ArgumentParser(
            prog=NAME, description='',
            formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-u', dest='_id', help='user id')
    parser.add_argument('-p', dest='pw', help='user password')
    #parser.add_argument('--auto', action='auto_login', help='login automatically')

    args = parser.parse_args()

    return args

def main():
    
    args = command_line()
    local_config = load_config()

    for key, val in local_config.items():
        if getattr(args, key, None) is None:
            setattr(args, key, val)

    print dir(args)
    
    try:


main()

import configparser
import os


def get_firebase_config(config, **kwargs):
    return {
        "apiKey": kwargs['apiKey'] if 'apiKey' in kwargs else config.get("firebase", "apiKey"),
        "email": kwargs['email'] if 'email' in kwargs else config.get("firebase", "email"),
        "password": kwargs['password'] if 'password' in kwargs else config.get("firebase", "password"),
        "refreshUrl": config.get("firebase", "refreshUrl", fallback="https://securetoken.googleapis.com/v1/token?key="),
        "signInWithEmailAndPasswordUrl": config.get("firebase", "signInWithEmailAndPasswordUrl",
                                                    fallback="https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key="),
        "ttl": config.getint("firebase", "ttl", fallback=3300)
    }


def marlin_config(config):
    return {
        "apiUrl": config.get('marlin', "apiUrl", fallback="grpc-api.tern.ai"),
        "ttl": config.getint('marlin', "ttl", fallback=120)
    }


class ConfigProcessor:
    CONFIG_FILE = '~/.marlin/config'

    def __init__(self, **kwargs):
        config = configparser.ConfigParser()
        config_file = kwargs.get('config_file', ConfigProcessor.CONFIG_FILE)
        config.read(os.path.expanduser(config_file))

        self.marlin_config = marlin_config(config)
        self.firebase_config = get_firebase_config(config, **kwargs)

from marlin.batch_store.pandas.pandas_fs_batch_store import PandasS3BatchStore
from marlin.config.config_processor import ConfigProcessor
from marlin.exploration_client import ExplorationClient
from marlin.marlin_batch_client import ServingBatchClient, TransformBatchClient
from marlin.metadata_store.marlin_metadata_store import MarlinMetadataStore
from marlin.marlin_service_pb2 import ServingConsumer
from getpass import getpass
import json
import requests

METADATA_STORE = None


def login():
    email = input("Username (Email): ")
    password = getpass("password: ")
    apiKey = getpass("apiKey: ")
    config = ConfigProcessor(email=email, password=password, apiKey=apiKey)
    data = json.dumps({'email': config.firebase_config['email'], 'password': config.firebase_config['password'],
                       'returnSecureToken': True})
    url = f"{config.firebase_config['signInWithEmailAndPasswordUrl']}{config.firebase_config['apiKey']}"
    try:
        api_request(url, data)
        _setup_metadata_store(config)
    except requests.HTTPError as e:
        raise requests.HTTPError(e.response.json(), e)


def api_request(url, data):
    headers = {'content-type': 'application/json; charset=UTF-8'}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()


def transform_client(namespace, name, version, entities):
    return TransformBatchClient(namespace, name, version, entities, PandasS3BatchStore(_metadata_store()))


def batch_scoring_client(namespace, name, version):
    return serving_client(namespace, name, version, ServingConsumer.SCORING)


def batch_training_client(namespace, name, version):
    return serving_client(namespace, name, version, ServingConsumer.TRAINING)


def serving_client(namespace, name, version, serving_consumer):
    store = _metadata_store()
    return ServingBatchClient(namespace, name, version, PandasS3BatchStore(store), store, serving_consumer)


def exploration_client():
    store = _metadata_store()
    return ExplorationClient(store, PandasS3BatchStore(store))


def _metadata_store():
    if METADATA_STORE is None:
        _setup_metadata_store_from_file_conf()

    return METADATA_STORE


def _setup_metadata_store_from_file_conf():
    config = ConfigProcessor()
    _setup_metadata_store(config)


def _setup_metadata_store(config):
    global METADATA_STORE
    METADATA_STORE = MarlinMetadataStore(config.marlin_config['apiUrl'], config.marlin_config['ttl'],
                                         config.firebase_config)

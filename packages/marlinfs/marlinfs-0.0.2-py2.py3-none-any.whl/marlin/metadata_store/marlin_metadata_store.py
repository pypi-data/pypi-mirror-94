from marlin.marlin_service_pb2 import TransformDefinition, TransformInputDefinition, TransformKey
from marlin.marlin_service_pb2 import ServingDefinition
from marlin.utils import dict_set_helper
from marlin.marlin_service_pb2_grpc import MarlinServiceStub
import grpc
import time
from functools import lru_cache, wraps
from datetime import datetime, timedelta
import collections
import requests
import json


def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


def get_client_wrapper(grpc_ttl, firebase_config):
    firebase = FirebaseAuthMetadataPlugin(firebase_config)

    @timed_lru_cache(seconds=grpc_ttl)
    def get_client(api_url):
        credential = grpc.composite_channel_credentials(grpc.ssl_channel_credentials(),
                                                        grpc.metadata_call_credentials(firebase))
        return MarlinServiceStub(grpc.secure_channel(api_url, credential))

    return get_client


class MarlinMetadataStore:
    def __init__(self, api_url, grpc_ttl, firebase_config):
        self.location_and_fs_options = None

        client_wrapper = get_client_wrapper(grpc_ttl, firebase_config)
        self.marlin_api_client = lambda: client_wrapper(api_url)

    def get_location_and_read_fs_options(self, namespace, transform_name, transform_version):
        request = MarlinMetadataStore.get_transform_key(namespace, transform_name, transform_version)
        return MarlinMetadataStore.parse_permission_response(self.marlin_api_client().DatasetReadPermission(request))

    def get_location_and_write_fs_options(self, namespace, transform_name, transform_version):
        request = MarlinMetadataStore.get_transform_key(namespace, transform_name, transform_version)
        return MarlinMetadataStore.parse_permission_response(self.marlin_api_client().DatasetWritePermission(request))

    def serving_definition_registration(self,
                                        namespace,
                                        name,
                                        version,
                                        serving_consumer,
                                        job_type,
                                        inputs,
                                        code):
        definition = MarlinMetadataStore.serving_definition_payload(namespace, name, version, serving_consumer,
                                                                    job_type, inputs, code)
        return definition, self.marlin_api_client().ServingRegistration(definition)

    def transform_definition_registration(self,
                                          namespace,
                                          name,
                                          version,
                                          features,
                                          entities,
                                          output_stores,
                                          input_readers,
                                          job_type,
                                          code):
        definition = MarlinMetadataStore.transform_definition_payload(namespace, name, version, code, job_type,
                                                                      features, entities, output_stores, input_readers)
        return self.marlin_api_client().TransformRegistration(definition)

    @lru_cache(maxsize=1024)
    def get_features(self, namespace, transform_name, transform_version):
        metadata = self.get_transform_metadata(namespace, transform_name, transform_version)
        return list(metadata.transform_definition.output_definition.features.keys())

    @lru_cache(maxsize=1024)
    def get_entities(self, namespace, transform_name, transform_version):
        metadata = self.get_transform_metadata(namespace, transform_name, transform_version)
        return list(metadata.transform_definition.output_definition.entities.keys())

    @lru_cache(maxsize=1024)
    def get_transform_metadata(self, namespace, transform_name, transform_version):
        return self.marlin_api_client().TransformMetadataRequest(
            MarlinMetadataStore.get_transform_key(namespace, transform_name, transform_version))

    @classmethod
    def serving_definition_payload(cls,
                                   namespace,
                                   name,
                                   version,
                                   serving_consumer,
                                   job_type,
                                   inputs,
                                   code):
        serving_definition = ServingDefinition()
        serving_definition.serving_key.namespace = namespace
        serving_definition.serving_key.name = name
        serving_definition.serving_key.version = version
        serving_definition.serving_consumer = serving_consumer
        serving_definition.serving_type = job_type
        serving_definition.serving_inputs.extend(MarlinMetadataStore.input_reader_to_input_definition(inputs))
        serving_definition.code = code
        return serving_definition

    @classmethod
    def parse_permission_response(cls, permission_response):
        storage_options = {'key': permission_response.permission['accessKeyId'],
                           'secret': permission_response.permission['secretAccessKey'],
                           'token': permission_response.permission['sessionToken']}

        return permission_response.permission['transformLocation'], storage_options

    @classmethod
    def get_transform_key(cls, namespace, transform_name, transform_version):
        transform_key = TransformKey()
        transform_key.namespace = namespace
        transform_key.transform_name = transform_name
        transform_key.version = transform_version
        return transform_key

    @classmethod
    def transform_definition_payload(cls,
                                     namespace,
                                     name,
                                     version,
                                     code,
                                     job_type,
                                     features,
                                     entities,
                                     output_stores,
                                     input_readers):
        transform_definition = TransformDefinition()
        transform_definition.transform_key.namespace = namespace
        transform_definition.transform_key.transform_name = name
        transform_definition.transform_key.version = version

        transform_definition.code = code
        transform_definition.job_type = job_type

        transform_definition.output_definition.stores.extend(output_stores)
        dict_set_helper(entities, transform_definition.output_definition.entities)
        dict_set_helper(features, transform_definition.output_definition.features)

        transform_definition.input_definitions.extend(
            MarlinMetadataStore.input_reader_to_input_definition(input_readers))

        return transform_definition

    @classmethod
    def input_reader_to_input_definition(cls, input_readers):
        feature_dict = collections.defaultdict(set)

        for reader in input_readers:
            feature_dict[(reader.namespace, reader.name, reader.version)].update(reader.features)

        input_def = []
        for (key, features) in feature_dict.items():
            transform_input_definition = TransformInputDefinition()
            transform_input_definition.transform_key.namespace = key[0]
            transform_input_definition.transform_key.transform_name = key[1]
            transform_input_definition.transform_key.version = key[2]
            transform_input_definition.features.extend(features)
            input_def.append(transform_input_definition)
        return input_def


class FirebaseAuthMetadataPlugin(grpc.AuthMetadataPlugin):
    def __init__(self, firebase_config):
        self.refresh_url = f"{firebase_config['refreshUrl']}{firebase_config['apiKey']}"
        self.sign_in_with_email_and_password_url = \
            f"{firebase_config['signInWithEmailAndPasswordUrl']}{firebase_config['apiKey']}"
        self.user = self.sign_in_with_email_and_password(firebase_config['email'], firebase_config['password'],
                                                         self.sign_in_with_email_and_password_url)
        self.firebase_ttl = firebase_config['ttl']
        self.expiry = FirebaseAuthMetadataPlugin.get_expiry(self.user.expires_in, self.firebase_ttl)

    def __call__(self, context, callback):
        callback(self.get_token(), None)

    def get_token(self):
        if FirebaseAuthMetadataPlugin.should_refresh(self.expiry):
            self.user = self.refresh(self.user.refresh_token)
            self.expiry = FirebaseAuthMetadataPlugin.get_expiry(self.user.expires_in, self.firebase_ttl)
        return (("authorization", "Bearer {}".format(self.user.id_token)),)

    def refresh(self, refresh_token):
        data = json.dumps({'grantType': 'refresh_token', 'refreshToken': refresh_token})
        response = FirebaseAuthMetadataPlugin.api_request(self.refresh_url, data)
        return FirebaseUser(response['user_id'], response['id_token'], response['refresh_token'],
                            response['expires_in'])

    @classmethod
    def sign_in_with_email_and_password(cls, email, password, url):
        data = json.dumps({'email': email, 'password': password, 'returnSecureToken': True})
        response = FirebaseAuthMetadataPlugin.api_request(url, data)
        return FirebaseUser(response['localId'], response['idToken'], response['refreshToken'], response['expiresIn'])

    @classmethod
    def api_request(cls, url, data):
        headers = {'content-type': 'application/json; charset=UTF-8'}
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_expiry(cls, expiry, ttl):
        return time.time() + expiry - ttl

    @classmethod
    def should_refresh(cls, expiry):
        return time.time() >= expiry


class FirebaseUser:
    def __init__(self, user_id, id_token, refresh_token, expires_in):
        self.user_id = user_id
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = float(expires_in)

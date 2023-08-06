import abc
from marlin.marlin_service_pb2 import TransformOutputStores, TransformJobType
from datetime import datetime


class BatchStore(abc.ABC):
    def __init__(self, metadata_store):
        self.metadata_store = metadata_store

    @abc.abstractmethod
    def batch_transform_reader(self, namespace, name, version, features):
        pass

    @abc.abstractmethod
    def batch_transform_writer(self, namespace, name, version, code, entities, input_definition):
        pass


class TransformBatchReader(abc.ABC):
    def __init__(self, namespace, name, version, features, metadata_store):
        self.namespace = namespace
        self.name = name
        self.version = version
        self.features = features
        self.entities = metadata_store.get_entities(namespace, name, version)
        self.metadata_store = metadata_store

    @abc.abstractmethod
    def read_by_ingestion_date(self, start_date, end_date, date_format='%Y-%m-%d-%H'):
        pass

    @abc.abstractmethod
    def read_by_event_date(self, start_date, end_date, date_format='%Y-%m-%d-%H'):
        pass

    @abc.abstractmethod
    def read_by_ingestion_ts(self, start_ingestion_time, end_ingestion_time):
        pass

    @abc.abstractmethod
    def read_by_event_ts(self, start_event_time, end_event_time):
        pass

    @abc.abstractmethod
    def point_in_time_join_by_date(self, entity_df, date_format='%Y-%m-%d-%H'):
        pass

    @abc.abstractmethod
    def point_in_time_join_by_ts(self, entity_df):
        pass

    @abc.abstractmethod
    def point_in_time_join_across_inputs_by_date(self, entity_df, input_list, date_format='%Y-%m-%d-%H'):
        pass

    @abc.abstractmethod
    def point_in_time_join_across_inputs_by_ts(self, entity_df, input_list):
        pass


class TransformBatchWriter(abc.ABC):
    def __init__(self,
                 metadata_store,
                 namespace,
                 name,
                 version,
                 code,
                 entities,
                 input_definition):
        self.namespace = namespace
        self.name = name
        self.version = version
        self.metadata_store = metadata_store
        self.input_definition = input_definition
        self.code = code
        self.entities = entities

    def register(self, entities, features):
        self.metadata_store.transform_definition_registration(self.namespace, self.name, self.version, features,
                                                              entities, [TransformOutputStores.BATCH_STORE],
                                                              self.input_definition, TransformJobType.BATCH_JOB,
                                                              self.code)

    @abc.abstractmethod
    def determine_features_and_entities(self, df):
        pass

    @abc.abstractmethod
    def write_df(self, df, ingest_timestamp, ingest_datetime, storage_options=None):
        pass

    def write(self, df, storage_options=None):
        (entities, features) = self.determine_features_and_entities(df)
        self.register(entities, features)
        ingest_datetime = datetime.utcnow()
        return self.write_df(df, round(ingest_datetime.timestamp() * 1000), ingest_datetime, storage_options)

import inspect
import abc
from functools import wraps
from marlin.marlin_service_pb2 import ServingType


class MarlinBaseClient(abc.ABC):
    def __init__(self, namespace, name, version, batch_store):
        self.namespace = namespace
        self.name = name
        self.version = version
        self.dependency = []
        self.batch_store = batch_store
        self.code = ''
        self.commit_flag = False

    def commit(self):
        self.commit_flag = True

    def process_function(self, function):
        self.code = inspect.getsource(function)

        @wraps(function)
        def decorator(*args, **kwargs):
            return self._process_function_handler(function(*args, **kwargs))

        return decorator

    @abc.abstractmethod
    def _process_function_handler(self, ret_val):
        pass

    def add_dependency(self, namespace, name, version, features):
        if self.commit_flag:
            raise Exception("Cannot add dependency after calling commit!")
        reader = self.batch_store.batch_transform_reader(namespace=namespace, name=name, version=version,
                                                         features=features)
        self.dependency.append(reader)
        return reader


class TransformBatchClient(MarlinBaseClient):
    def __init__(self, namespace, name, version, entities, batch_store):
        super().__init__(namespace, name, version, batch_store)
        self.entities = entities

    def _process_function_handler(self, df):
        return self.save(df)

    def save(self, df):
        if self.commit_flag:
            dataframe = df
            storage_options = None
            if (isinstance(df, tuple)):
                dataframe = df[0]
                storage_options = df[1]
            return self.batch_store.batch_transform_writer(self.namespace, self.name, self.version, self.code,
                                                           self.entities, self.dependency).write(dataframe,
                                                                                                 storage_options)
        return df


class ServingBatchClient(MarlinBaseClient):
    def _process_function_handler(self, ret_val):
        return ret_val

    def __init__(self, namespace, name, version, batch_store, metadata_store, serving_consumer):
        super().__init__(namespace, name, version, batch_store)
        self.metadata_store = metadata_store
        self.serving_consumer = serving_consumer

    def commit(self):
        super(ServingBatchClient, self).commit()
        self.metadata_store.serving_definition_registration(self.namespace, self.name, self.version,
                                                            self.serving_consumer, ServingType.BATCH_SERVING,
                                                            self.dependency, self.code)

class ExplorationClient:
    def __init__(self, metadata_store, batch_store):
        self.metadata_store = metadata_store
        self.batch_store = batch_store

    def get_transform(self, namespace, name, version):
        return self.batch_store.batch_transform_reader(namespace=namespace, name=name, version=version,
                                                features=self.metadata_store.get_features(namespace, name, version))

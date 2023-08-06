from dippy.labels.datastore import Datastore


class UnsupportedObjectType(Exception):
    ...


class Labeler:
    datastore: Datastore

    def get_labels(self, **match) -> :
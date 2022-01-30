from bug_killer_app.datastore.project_table.project_item import ProjectItem


class DummyTransactWrite:
    """ Unit tests can't use a connection for transact write. Instead, we batch write items """

    def __init__(self, *args, **kwargs):
        self._items = []

    def __enter__(self):
        self._items = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with ProjectItem.batch_write() as batch:
            [batch.save(item) for item in self._items]

        return self

    def save(self, item):
        self._items.append(item)

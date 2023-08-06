import django
import django.db

from .Database import DatabaseStatus


class Waiter:
    def __init__(self, executor=None):
        self._executor = executor

    def run_query(self, query, database):
        pass


class WaitWaiter(Waiter):
    def __init__(self, executor=None):
        super(WaitWaiter, self).__init__(executor)

    def run_query(self, query, database):
        while database.status.get() == DatabaseStatus.RUNNING.value:
            try:
                self._executor.run_query(query, database)
                break
            except django.db.utils.OperationalError:
                database.status.put(DatabaseStatus.DOWN.value)
                self.wait_for_connection(query, database)

    def wait_for_connection(self, query, database):
        while database.status.get() == DatabaseStatus.DOWN.value:
            pass


class DontWaitWaiter(Waiter):
    def run_query(self, query, database):
        if database.status.get() == DatabaseStatus.RUNNING.value:
            try:
                self._executor.run_query(query, database)
            except django.db.utils.OperationalError:
                database.status.put(DatabaseStatus.DOWN.value)
                raise django.db.utils.OperationalError

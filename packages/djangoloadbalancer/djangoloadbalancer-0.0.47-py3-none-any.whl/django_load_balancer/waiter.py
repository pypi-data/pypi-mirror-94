import django
import django.db.utils

from .database import DatabaseStatus


class Waiter:
    def __init__(self, executor=None):
        self.executor = executor

    def run_query(self, query, database):
        pass


class WaitWaiter(Waiter):
    def __init__(self, executor=None):
        super(WaitWaiter, self).__init__(executor)

    def run_query(self, query, database):
        if database.check_status() == DatabaseStatus.RUNNING.value:
            try:
                self.executor.run_query(query, database)
                database.query_ended.set()
            except django.db.utils.OperationalError:
                database.change_status(DatabaseStatus.DOWN.value)
                self.wait_for_connection(query, database)
        else:
            self.wait_for_connection(query, database)

    def wait_for_connection(self, query, database):
        database.is_up.wait()
        database.is_up.clear()
        self.run_query(query, database)


class DontWaitWaiter(Waiter):
    def run_query(self, query, database):
        try:
            self.executor.run_query(query, database)
            database.query_ended.set()
        except django.db.utils.OperationalError:
            database.change_status(DatabaseStatus.DOWN.value)
            database.query_ended.set()
            raise django.db.utils.OperationalError

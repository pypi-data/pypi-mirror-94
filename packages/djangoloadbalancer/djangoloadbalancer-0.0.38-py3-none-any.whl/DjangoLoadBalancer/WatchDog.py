from time import sleep

from django.db import connections, OperationalError

from .Database import DatabaseStatus


class WatchDog():
    def __init__(self, databases,wait_time):
        self._databases=databases
        self._wait_time=wait_time

    def check_databases_statuses(self):
        while True:
            sleep(self._wait_time)
            for database in self._databases:
                if database.check_status()==DatabaseStatus.RUNNING.value:
                    try:
                        cursor= connections[database.name].cursor()
                        cursor.execute("select count(*) from pg_stat_activity where pid <> pg_backend_pid() and usename = current_user;")
                        cursor.close()
                    except (database.operational_error,OperationalError) as e:
                        database.change_status(DatabaseStatus.DOWN.value)
                        database.is_up.clear()
                else:
                    try:
                        connections[database.name].close()
                        connections[database.name].connect()
                        database.change_status(DatabaseStatus.RUNNING.value)
                        database.is_up.set()
                    except (database.operational_error):
                        pass


from datetime import datetime
from time import sleep

import django.db
import django.db.utils

from .database import DatabaseStatus


class WatchDog():
    def __init__(self, databases, wait_time):
        self._databases = databases
        self._wait_time = wait_time

    def check_databases_statuses(self):
        while True:
            sleep(self._wait_time)
            for database in self._databases:
                if database.check_status() == DatabaseStatus.RUNNING.value:
                    try:
                        cursor = django.db.connections[database.name].cursor()
                        cursor.execute(
                            "select count(*) from pg_stat_activity where pid <> pg_backend_pid() and usename = current_user;")
                        cursor.close()
                    except (database.operational_error, django.db.utils.OperationalError):
                        database.change_status(DatabaseStatus.DOWN.value)
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print(f"{current_time}   {database.name} went down")
                else:
                    try:
                        django.db.connections[database.name].close()
                        django.db.connections[database.name].connect()
                        database.change_status(DatabaseStatus.RUNNING.value)
                        database.is_up.set()
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print(f"{current_time}   {database.name} went up")
                    except (database.operational_error):
                        pass

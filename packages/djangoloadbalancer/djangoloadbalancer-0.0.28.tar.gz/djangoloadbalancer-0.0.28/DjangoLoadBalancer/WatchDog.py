from time import sleep

from django.db import connections

from DjangoLoadBalancer.DjangoLoadBalancer.Database import DatabaseStatus


class WatchDog():
    def __init__(self, databases,wait_time):
        self._databases=databases
        self._wait_time=wait_time

    def check_databases_statuses(self):
        while True:
            sleep(self._wait_time)
            for database in self._databases:
                try:
                    connections[database.name].connect()
                except database.operational_error:
                    database.status.put(DatabaseStatus.DOWN.value)
                else:
                    database.status.put(DatabaseStatus.RUNNING.value)

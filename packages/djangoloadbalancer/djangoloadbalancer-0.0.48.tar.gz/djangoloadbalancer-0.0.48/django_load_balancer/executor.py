import inspect
from datetime import datetime

import django.db
import django.db.models


class Executor():
    def __init__(self, result=None):
        self._result = result

    def run_query(self, query, database):
        pass


class NoQuerySetExecutor(Executor):
    def run_query(self, query, database):
        if query.method == 'get_queryset':
            instance = query.model.loadbalancer_base_manager
            result = instance.__getattribute__(query.method)(*query.args, **query.kwargs).using(database.name)
        else:
            instance = query.model
            result = dict(inspect.getmembers(django.db.models.Model))[query.method](instance, using=database.name)
        self._result.put({query.query_id: result})
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"{current_time}   {database.name}   {query.model}   {query.method}")


class QuerySetExecutor(Executor):
    def run_query(self, query, database):
        instance = query.model.models_manager.using(database.name)
        result = instance.__getattribute__(query.method)(*query.args, **query.kwargs)
        self._result.put({query.query_id: result})
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"{current_time}   {database.name}   {query.model}   {query.method}")


class InfoQueryExecutor(Executor):
    def run_query(self, query, database):
        with django.db.connections[database.name].cursor() as cursor:
            new_info = self.get_statistic(query, cursor, database)
            database.info.put(new_info)

    def get_statistic(self, query, cursor, database):
        pass

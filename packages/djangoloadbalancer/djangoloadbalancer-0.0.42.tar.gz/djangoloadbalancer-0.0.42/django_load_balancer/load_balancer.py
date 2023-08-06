import sys

import django.db.utils

from .query import Wait


class LoadBalancer():
    def __init__(self, result, databases, cud_algorithm, r_algorithm):
        self._current_query_id = 0
        self._result = result
        self._databases = databases
        self._cud_algorithm = cud_algorithm
        self._r_algorithm = r_algorithm

    def run_query(self, query):
        self.generate_query_id()
        query.query_id = self._current_query_id
        if query.wait == Wait.DONT_WAIT.value:
            self.execute_r(query)
        else:
            self.execute_cud(query)
        res = self._result.get()
        while list(res.keys())[0] != self._current_query_id:
            res = self._result.get()
        return list(res.values())[0]

    def execute_cud(self, query):
        self._cud_algorithm.execute_cud(query)

    def execute_r(self, query):
        while True:
            try:
                self._r_algorithm.execute_r(query)
            except django.db.utils.OperationalError:
                pass
            else:
                break

    def generate_query_id(self):
        if self._current_query_id == sys.maxsize:
            self._current_query_id = 0
        else:
            self._current_query_id += 1

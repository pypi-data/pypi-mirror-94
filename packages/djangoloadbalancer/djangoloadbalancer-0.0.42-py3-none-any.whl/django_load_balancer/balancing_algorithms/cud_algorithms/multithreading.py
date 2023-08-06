from ...balancing_algorithms.cud_algorithm import CUDAlgorithm


class MultithreadingAlgorithm(CUDAlgorithm):
    def __init__(self, databases):
        self._databases = databases

    def execute_cud(self, query):
        for db in self._databases:
            db.queries.put(query)
            db.has_queries.release()

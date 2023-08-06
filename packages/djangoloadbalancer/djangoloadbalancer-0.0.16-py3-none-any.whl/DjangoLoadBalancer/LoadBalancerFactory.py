import sqlite3
import threading
from queue import Queue

import psycopg2

from .BalancingAlgorithms.CUDAlgorithms.MultithreadingAlgorithm import \
    MultithreadingAlgorithm
from .BalancingAlgorithms.RAlgorithms.Interval import Interval
from .BalancingAlgorithms.RAlgorithms.RoundRobin import RoundRobin
from .Database import Database, DatabaseEngine
from .Executors import QuerySetExecutor, NoQuerySetExecutor
from .InfoQueryExecutors import ResponseTimeExecutor, NumberOfConnectionsExecutor
from .LoadBalancer import LoadBalancer
from .Query import QueryType, Wait
from .Waiters import WaitWaiter, DontWaitWaiter
from .local_settings import LOAD_BALANCER,DATABASES


class LoadBalancerFactory:
    @classmethod
    def create_load_balancer(cls):
        result = Queue()
        threads, databases = cls._create_databases(result)
        cud_algorithm = cls._create_cud_algorithm(databases, threads)
        r_algorithm = cls._create_r_algorithm(databases)
        return LoadBalancer(result, databases, cud_algorithm, r_algorithm)

    @classmethod
    def _create_databases(cls, result):
        if LOAD_BALANCER['CUD_ALGORITHM'] == "MULTITHREADING":
            threads = []
            databases = []
            for i, name in enumerate(LOAD_BALANCER['DATABASES']):
                database = Database(name, {Wait.WAIT: WaitWaiter(LOAD_BALANCER['WAIT_TIME']),
                                           Wait.DONT_WAIT: DontWaitWaiter()},
                                    {QueryType.QUERYSET: QuerySetExecutor(result),
                                     QueryType.NO_QUERYSET: NoQuerySetExecutor(result)}, DATABASES[name]['ENGINE'],
                                    cls.OperationalErrorGenerator.generate_operational_error(DATABASES[name]['ENGINE']))
                databases.append(database)
                threads.append(threading.Thread(target=database.run_queries, args=(), daemon=True))
                threads[i].start()
            return threads, databases

    @staticmethod
    def _create_cud_algorithm(databases, threads=None):
        if LOAD_BALANCER['CUD_ALGORITHM'] == "MULTITHREADING":
            return MultithreadingAlgorithm(threads, databases)

    @staticmethod
    def _create_r_algorithm(databases):
        if LOAD_BALANCER['R_ALGORITHM']['NAME'] == "ROUND_ROBIN":
            return RoundRobin(databases)
        elif LOAD_BALANCER['R_ALGORITHM']['NAME'] == "INTERVAL_TIME":
            algorithm = Interval(databases)
            for database in databases:
                database.executors[QueryType.INFO_RESPONSE_TIME] = ResponseTimeExecutor()
            threading.Thread(target=algorithm.update_info,
                             args=(LOAD_BALANCER['R_ALGORITHM']['INTERVAL'], QueryType.INFO_RESPONSE_TIME),
                             daemon=True).start()
            return algorithm
        elif LOAD_BALANCER['R_ALGORITHM']['NAME'] == "INTERVAL_NUMBER_OF_CONNECTIONS":
            algorithm = Interval(databases)
            for database in databases:
                database.executors[QueryType.INFO_NUMBER_OF_CONNECTIONS] = NumberOfConnectionsExecutor()
            threading.Thread(target=algorithm.update_info,
                             args=(LOAD_BALANCER['R_ALGORITHM']['INTERVAL'], QueryType.INFO_NUMBER_OF_CONNECTIONS),
                             daemon=True).start()
            return algorithm

    class OperationalErrorGenerator:
        @staticmethod
        def generate_operational_error(engine):
            if engine == DatabaseEngine.POSTGRESQL.value:
                return psycopg2.OperationalError
            elif engine == DatabaseEngine.SQLITE.value:
                return sqlite3.OperationalError

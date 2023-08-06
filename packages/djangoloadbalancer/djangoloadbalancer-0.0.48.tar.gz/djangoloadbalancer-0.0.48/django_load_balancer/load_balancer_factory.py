import queue
import sqlite3
import threading

import MySQLdb
import psycopg2

from .balancing_algorithms.cud_algorithms.multithreading import \
    MultithreadingAlgorithm
from .balancing_algorithms.r_algorithms.interval import Interval
from .balancing_algorithms.r_algorithms.round_robin import RoundRobin
from .database import Database, DatabaseEngine
from .executor import QuerySetExecutor, NoQuerySetExecutor
from .info_query_executor import ResponseTimeExecutor, NumberOfConnectionsExecutor
from .load_balancer import LoadBalancer
from .local_settings import LOAD_BALANCER, DATABASES
from .query import QueryType, Wait
from .waiter import WaitWaiter, DontWaitWaiter
from .watch_dog import WatchDog


class LoadBalancerFactory:
    @classmethod
    def create_load_balancer(cls):
        result = queue.Queue()
        databases = cls._create_databases(result)
        watch_dog = WatchDog(databases, LOAD_BALANCER['WAIT_TIME'])
        watch_dog_thread = threading.Thread(target=watch_dog.check_databases_statuses, args=(), daemon=True)
        watch_dog_thread.start()
        cud_algorithm = cls._create_cud_algorithm(databases)
        r_algorithm = cls._create_r_algorithm(databases)
        return LoadBalancer(result, databases, cud_algorithm, r_algorithm)

    @classmethod
    def _create_databases(cls, result):
        if LOAD_BALANCER['CUD_ALGORITHM'] == "MULTITHREADING":
            databases = []
            for i, name in enumerate(LOAD_BALANCER['DATABASES']):
                database = Database(name, {Wait.WAIT.value: WaitWaiter(),
                                           Wait.DONT_WAIT.value: DontWaitWaiter()},
                                    {QueryType.QUERYSET.value: QuerySetExecutor(result),
                                     QueryType.NO_QUERYSET.value: NoQuerySetExecutor(result)},
                                    DATABASES[name]['ENGINE'],
                                    cls.OperationalErrorGenerator.generate_operational_error(DATABASES[name]['ENGINE']))
                databases.append(database)
                database.query_ended.set()
                thread = threading.Thread(target=database.run_queries, args=(), daemon=True)
                thread.start()
            return databases

    @staticmethod
    def _create_cud_algorithm(databases):
        if LOAD_BALANCER['CUD_ALGORITHM'] == "MULTITHREADING":
            return MultithreadingAlgorithm(databases)

    @staticmethod
    def _create_r_algorithm(databases):
        if LOAD_BALANCER['R_ALGORITHM']['NAME'] == "ROUND_ROBIN":
            return RoundRobin(databases)
        elif LOAD_BALANCER['R_ALGORITHM']['NAME'] == "INTERVAL_TIME":
            algorithm = Interval(databases)
            for database in databases:
                database.executors[QueryType.INFO_RESPONSE_TIME] = ResponseTimeExecutor()
            threading.Thread(target=algorithm.update_info,
                             args=(LOAD_BALANCER['R_ALGORITHM']['INTERVAL'], QueryType.INFO_RESPONSE_TIME.value),
                             daemon=True).start()
            return algorithm
        elif LOAD_BALANCER['R_ALGORITHM']['NAME'] == "INTERVAL_NUMBER_OF_CONNECTIONS":
            algorithm = Interval(databases)
            for database in databases:
                database.executors[QueryType.INFO_NUMBER_OF_CONNECTIONS] = NumberOfConnectionsExecutor()
            threading.Thread(target=algorithm.update_info,
                             args=(
                             LOAD_BALANCER['R_ALGORITHM']['INTERVAL'], QueryType.INFO_NUMBER_OF_CONNECTIONS.value),
                             daemon=True).start()
            return algorithm

    class OperationalErrorGenerator:
        @staticmethod
        def generate_operational_error(engine):
            if engine == DatabaseEngine.POSTGRESQL.value:
                return psycopg2.OperationalError
            elif engine == DatabaseEngine.MYSQL.value:
                return MySQLdb.OperationalError
            elif engine == DatabaseEngine.SQLITE.value:
                return sqlite3.OperationalError

from neo4j import GraphDatabase
from py2neo import Graph
import time


def neo4j_driver_1():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"), encrypted=False)
    session = driver.session()
    cypher = 'match (n:newNode)-[r]-(k:newNode) return n,r,k'
    se = session.run(cypher)
    # print(type(se))


def neo4j_driver_2():
    graph = Graph()
    data = graph.run('match (n:newNode)-[r]-(k:newNode) return n,r,k').data()
    # print(type(data))


if __name__ == '__main__':
    start = time.perf_counter()
    neo4j_driver_1()
    mid = time.perf_counter()
    print(str(mid - start) + " s")
    neo4j_driver_2()
    print(str(time.perf_counter() - mid) + " s")

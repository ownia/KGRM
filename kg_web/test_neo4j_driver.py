from neo4j import GraphDatabase, Transaction
from py2neo import Graph
import pandas as pd
import json
import time
from py2neo import Graph


def old():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"), encrypted=False)
    session = driver.session()
    data = session.run("MATCH (m)-[r]->(n) RETURN m.title, r.relation, n.title LIMIT 200")
    print(data)


def eva_index_cypher_test():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"), encrypted=False)
    session = driver.session()
    nlist = ['奥维云网', 'AVC', '海尔', 'GJds', '奥克斯', '格力', '美的']
    for i in nlist:
        cypher = 'MATCH(n) WHERE n.title =~\'.*' + str(i) + '.*\' RETURN n.title LIMIT 1'
        # se = graph.run(cypher).data()
        se = session.run(cypher)
        print(type(se))
        for d in se:
            bs = str(d[0])
            print(str(bs))


def new_test():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"), encrypted=False)
    session = driver.session()
    cypher = 'MATCH (p1:product {title: "' \
             + '海尔BCD-458WDVMU1' + '"})-[]-(cuisine1) ' \
                                   'WITH p1, collect(id(cuisine1)) AS p1Cuisine ' \
                                   'MATCH (p2:product {title: "' \
             + "海尔XPB30-0623S" + '"})-[]-(cuisine2) ' \
                                 'WITH p1, p1Cuisine, p2, collect(id(cuisine2)) AS p2Cuisine ' \
                                 'RETURN p1.title AS from, p2.title AS to, ' \
                                 'gds.alpha.similarity.jaccard(p1Cuisine, p2Cuisine) AS similarity'
    se = session.run(cypher)
    print(se)
    for d in se:
        print(d[0])
        print(d[1])
        print(d[2])


def gds_test():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"), encrypted=False)
    session = driver.session()
    cypher = 'MATCH (p1 {title: "' \
             + '海尔BCD-458WDVMU1' + '"})-[]-() ' \
                                   'MATCH (p2 {title: "' \
             + "格力(GREE)" + '"})-[]-() ' \
                            'RETURN gds.alpha.linkprediction.commonNeighbors(p1, p2) LIMIT 1'
    se = session.run(cypher)
    for i in se:
        print(i[0])


def gds_test_2():
    graph = Graph()
    cypher = 'MATCH (p1 {title: "' \
             + '海尔BCD-458WDVMU1' + '"})-[]-() ' \
                                   'MATCH (p2 {title: "' \
             + "格力(GREE)" + '"})-[]-() ' \
                            'RETURN gds.alpha.linkprediction.commonNeighbors(p1, p2) LIMIT 1'
    se = graph.run(cypher).data()
    print(se)


def gds_test_3():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"), encrypted=False)
    session = driver.session()
    similarity_value = []
    cypher_euclidean = 'MATCH (p1:product {title: "' \
                       + '海尔BCD-458WDVMU1' + '"})-[]-() ' \
                                             'MATCH (p2:product {title: "' \
                       + "格力(GREE)" + '"})-[]-() ' \
                                      'RETURN p1.title AS from, p2.title AS to, ' \
                                      'gds.alpha.similarity.euclideanDistance(collect(coalesce(toFloat(' \
                                      'p1.price), gds.util.NaN())), collect(coalesce(toFloat(p2.price), ' \
                                      'gds.util.NaN()))) AS similarity '
    se = session.run(cypher_euclidean)
    if Transaction.success:
        print("1")
    else:
        print("2")


if __name__ == '__main__':
    # eva_index_cypher_test()
    # new_test()

    """
    start = time.perf_counter()
    gds_test()
    end = time.perf_counter()
    print(end - start)
    start = time.perf_counter()
    gds_test_2()
    end = time.perf_counter()
    print(end - start)
    """

    gds_test_3()

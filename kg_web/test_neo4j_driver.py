from neo4j import GraphDatabase
from py2neo import Graph
import pandas as pd
import json


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


if __name__ == '__main__':
    # eva_index_cypher_test()
    new_test()

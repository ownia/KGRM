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


if __name__ == '__main__':
    eva_index_cypher_test()

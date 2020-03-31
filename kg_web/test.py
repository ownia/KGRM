from py2neo import Graph, Node, Relationship

if __name__ == '__main__':
    graph = Graph()
    # tx = graph.begin()
    print(len(graph.nodes))
    data = graph.run(
        'MATCH (:class{title:"快递物流品牌"})-[r:RELATION {type :"包括"  }]->(n) RETURN n.title, n.registered ORDER BY '
        'n.registered').to_table()
    print(repr(data))

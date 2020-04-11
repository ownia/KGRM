from py2neo import Graph, Node, Relationship
from flask import jsonify
import json
import re
import chardet
from demjson import decode


def build_nodes(node_record):
    data = {'id': str(node_record['id(n)'])}
    return {'data': data}


def build_edges(relation_record):
    data = {'source': str(relation_record['id(k)']),
            'target': str(relation_record['id(n)']),
            'relationship': "生产"}
    return {'data': data}


def old():
    nodes = list(map(build_nodes, graph.run('MATCH (n:product) WHERE n.title=~".*索尼.*" RETURN id(n) LIMIT 50').data()))
    nodes.append({'data': {'id': '14'}})
    edges = list(map(build_edges, graph.run(
        'MATCH (n:product) WHERE n.title=~".*索尼.*" MATCH (k)-[r]-(n) RETURN id(n),id(k) LIMIT 50').data()))
    elements = {'nodes': nodes, 'edges': edges}
    js = json.dumps(elements)
    print(js)


if __name__ == '__main__':
    graph = Graph()
    data = graph.run('match (n:newNode)-[r]-(k:newNode) return n,r,k limit 3').data()
    # print(type(data))
    # print(data)
    # for i in data:r'^("[^"]+")([^"]+)("[^"]+")'
    #     for e in i:
    #         if 'title' in e:
    #             print(i)
    nodes = []
    edges = []
    # print(data)
    for i in data:
        for e in i:
            if 'title' in i[e]:
                id_pattern = re.compile(r'_(\d+):')
                id = id_pattern.findall(str(i[e]))
                label_pattern = re.compile(r':(\w+)')
                label = label_pattern.findall(str(i[e]))
                title_pattern = re.compile(r'\'(\S+)\'')
                title = title_pattern.findall(str(i[e]))
                t = eval(repr(title).replace('\\\\', '\\'))
                s = str(t).replace("['", "").replace("']", "")
                data = {'id': str(id).replace("['", "").replace("']", ""),
                        'label': str(label).replace("['", "").replace("']", ""),
                        'title': s}
                nodes.append({'data': data})
            else:
                target_pattern = re.compile(r'_(\d+)\)-')
                target = target_pattern.findall(str(i[e]))
                source_pattern = re.compile(r'->\(_(\d+)')
                source = source_pattern.findall(str(i[e]))
                rela_pattern = re.compile(r'\'(.+)\'')
                rela = rela_pattern.findall(str(i[e]))
                r = eval(repr(rela).replace('\\\\', '\\'))
                s = str(r).replace("['", "").replace("']", "")
                data = {'source': str(source).replace("['", "").replace("']", ""),
                        'target': str(target).replace("['", "").replace("']", ""),
                        'relationship': s}
                edges.append({'data': data})
    elements = {'nodes': nodes, 'edges': edges}
    js = json.dumps(elements, ensure_ascii=False)
    print(js)

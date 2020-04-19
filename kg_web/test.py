from py2neo import Graph, Node, Relationship
from flask import jsonify
import json
import re
import chardet
from demjson import decode
import numpy as np
from neo4j import GraphDatabase, basic_auth, kerberos_auth, custom_auth, TRUST_ALL_CERTIFICATES


def build_nodes(node_record):
    data = {'id': str(node_record['id(n)'])}
    return {'data': data}


def build_edges(relation_record):
    data = {'source': str(relation_record['id(k)']),
            'target': str(relation_record['id(n)']),
            'relationship': "生产"}
    return {'data': data}


def old():
    graph = Graph()
    nodes = list(map(build_nodes, graph.run('MATCH (n:product) WHERE n.title=~".*索尼.*" RETURN id(n) LIMIT 50').data()))
    nodes.append({'data': {'id': '14'}})
    edges = list(map(build_edges, graph.run(
        'MATCH (n:product) WHERE n.title=~".*索尼.*" MATCH (k)-[r]-(n) RETURN id(n),id(k) LIMIT 50').data()))
    elements = {'nodes': nodes, 'edges': edges}
    js = json.dumps(elements)
    print(js)


def re_data():
    graph = Graph()
    data = graph.run('match (n:newNode)-[r]-(k:newNode) return n,r,k').data()
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
                title_pattern = re.compile(r'title: \'(\S+)\'')
                title = title_pattern.findall(str(i[e]))
                t_title = eval(repr(title).replace('\\\\', '\\'))
                s_title = str(t_title).replace("['", "").replace("']", "")

                info_pattern = re.compile(r'\"(.+)\"')
                info = info_pattern.findall(str(i[e]))
                t_info = eval(repr(info).replace('\\\\', '\\'))
                s_info = str(t_info).replace("['", "").replace("']", "")

                data = {'id': str(id).replace("['", "").replace("']", ""),
                        'label': str(label).replace("['", "").replace("']", ""),
                        'title': s_title, 'info': s_info}
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


class Solution:
    def entityParser(self, text: str) -> str:
        data = text.replace("&quot;", "\"").replace("&apos;", "\'").replace("&amp;", "&").replace("&gt;", ">").replace(
            "&lt;", "<").replace("&frasl;", "/")
        return data


def Jaccard(terms_model, reference):
    grams_reference = set(reference)
    grams_model = set(terms_model)
    temp = 0
    for i in grams_reference:
        if i in grams_model:
            temp = temp + 1
    dis = len(grams_model) + len(grams_reference) - temp
    jaccard_coefficient = float(temp / dis)
    return jaccard_coefficient


def dice_coefficient(a, b):
    """dice coefficient 2nt/na + nb."""
    a_bigrams = set(a)
    b_bigrams = set(b)
    overlap = len(a_bigrams & b_bigrams)
    return overlap * 2.0 / (len(a_bigrams) + len(b_bigrams))


def edit_distance(word1, word2):
    len1 = len(word1)
    len2 = len(word2)
    dp = np.zeros((len1 + 1, len2 + 1))
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            delta = 0 if word1[i - 1] == word2[j - 1] else 1
    dp[i][j] = min(dp[i - 1][j - 1] + delta, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
    return dp[len1][len2]


def print_title_of(tx, name):
    for record in tx.run("MATCH (a:class)-[]->(f) "
                         "WHERE a.name = {name} "
                         "RETURN f.name", name=name):
        print(record["f.name"])


if __name__ == '__main__':
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    session = driver.session()
    data = session.run("MATCH (m)-[r]->(n) RETURN m.title, r.relation, n.title LIMIT 100")
    # print(data)
    blists = []
    for d in data:
        bs = str(d[0])
        blists.append(bs)
    for i in range(len(blists)):
        for j in range(0, i):
            a = blists[i]
            b = blists[j]
            td = Jaccard(a, b)
            std = edit_distance(a, b) / max(len(a), len(b))
            fy = 1 - std
            avg = (td + fy) / 2
            if avg < 1:
                print(blists[i], blists[j])
                print('avg_sim: ', avg)

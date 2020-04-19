from flask import Flask, render_template, request, redirect, abort, jsonify, g
from py2neo import Graph
from collections import OrderedDict
import pandas as pd
import json
import hanlp
import re
import numpy as np
from neo4j import GraphDatabase, basic_auth, kerberos_auth, custom_auth, TRUST_ALL_CERTIFICATES

app = Flask(__name__)
graph = Graph()
ctx = app.app_context()
ctx.text = 'match (n:newNode)-[r]-(k:newNode) return n,r,k'


def build_nodes(node_record):
    data = {'id': str(node_record['id(n)'])}
    return {'data': data}


def build_edges(relation_record):
    data = {'source': str(relation_record['id(k)']),
            'target': str(relation_record['id(n)']),
            'relationship': "生产"}
    return {'data': data}


@app.route('/', methods=("GET", "POST"))
def index():
    data = count()
    return render_template('index.html', data=data)


@app.route('/graph')
def get_graph():
    # nodes = list(map(build_nodes, graph.run('MATCH (n:product) WHERE n.title=~".*索尼.*" RETURN id(n) LIMIT 50').data()))
    # nodes.append({'data': {'id': '14'}})
    # edges = list(map(build_edges, graph.run(
    #     'MATCH (n:product) WHERE n.title=~".*索尼.*" MATCH (k)-[r]-(n) RETURN id(n),id(k) LIMIT 50').data()))
    # elements = {'nodes': nodes, 'edges': edges}
    data1 = graph.run(ctx.text).data()
    nodes = []
    edges = []
    for i in data1:
        for e in i:
            if 'title' in i[e]:
                id_pattern = re.compile(r'_(\d+):')
                id = id_pattern.findall(str(i[e]))
                label_pattern = re.compile(r':(\w+) {')
                label = label_pattern.findall(str(i[e]))
                title_pattern = re.compile(r'title: \'(\S+)\'')
                title = title_pattern.findall(str(i[e]))
                t_title = eval(repr(title).replace('\\\\', '\\'))
                s_title = str(t_title).replace("['", "").replace("']", "")

                info_pattern = re.compile(r'info: \'(.+),')
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
    return jsonify(elements)


@app.route('/cypher', methods=("GET", "POST"))
def get_cypher():
    pd.set_option('display.float_format', lambda x: '%.4f' % x)
    df = pd.DataFrame(graph.run(
        'MATCH (:class{title:"快递物流品牌"})-[r:RELATION {type :"包括"  }]->(n) RETURN n.title, n.registered ORDER BY '
        'n.registered').to_table())
    if request.method == "POST":
        cypher = request.form['cypher']
        print(cypher)
        try:
            df = pd.DataFrame(graph.run(cypher).to_table())
            print(df)
        except:
            print('error')
    data = count()
    return render_template('cypher.html', data=data,
                           tables=[df.to_html(classes='table table-dark table-striped')],
                           titles=df.columns.values)


@app.route('/graph_visualization', methods=("GET", "POST"))
def graph_visualization():
    data = count()
    if request.method == "POST":
        cypher = request.form['graph-cypher']
        try:
            ctx.text = cypher
            print('success')
        except:
            print('error')
    return render_template('graph_visualization.html', data=data)


def count() -> str:
    node = len(graph.nodes)
    edge = len(graph)
    data = "共有" + str(node) + "个节点，" + str(edge) + "个关系"
    return str(data)


@app.route('/about')
def about():
    data = count()
    return render_template('about.html', data=data)


@app.route('/ner_data')
def get_ner(list_ner):
    elements = {'word': list_ner}
    return jsonify(elements)


@app.route('/ner', methods=("GET", "POST"))
def ner():
    data = count()
    ner_output = ""
    data2 = []
    text = ""
    page = ""
    if request.method == "POST":
        ner_post = request.form['ner_post']
        text = ner_post
        # print(ner_post)
        try:
            # tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')
            # ner_output = tokenizer(ner_post)
            recognizer = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
            list_data = re.split(r'[，。；\s]\s*', ner_post)
            data1 = []
            for li in list_data:
                data1.append(list(li))
            ner_output = recognizer(data1)
            for n in ner_output:
                for i in n:
                    if len(i[0]) > 1:
                        data2.append(i[0])
            ner_output = data2
            src = str(ner_post)
            for i in data2:
                temp = src.replace(str(i), str("<mark>" + i + "</mark>"))
                src = temp
            page = "<p>" + src + "</p>"
            # print(page)
        except:
            print('post error.')
    return render_template('ner.html', data=data, text=text, ner_output=ner_output, page=page)


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


def take_third(elem):
    return elem[2]


@app.route('/similarity_coefficient')
def sim_coe():
    data = count()
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    session = driver.session()
    data = session.run("MATCH (m)-[r]->(n) RETURN m.title, r.relation, n.title LIMIT 100")
    # print(data)
    blists = []
    out_j = []
    out_d = []
    for d in data:
        bs = str(d[0])
        blists.append(bs)
    for i in range(len(blists)):
        for j in range(0, i):
            a = blists[i]
            b = blists[j]
            td_j = Jaccard(a, b)
            td_d = dice_coefficient(a, b)
            std = edit_distance(a, b) / max(len(a), len(b))
            fy = 1 - std
            avg_j = (td_j + fy) / 2
            avg_d = (td_d + fy) / 2
            if avg_j < 1:
                # print(blists[i], blists[j])
                # print('avg_sim: ', avg_j)
                out_j.append(blists[i] + " " + blists[j] + " " + str(avg_j))
            if avg_d < 1:
                out_d.append(blists[i] + " " + blists[j] + " " + str(avg_d))
    list_j = list(set(out_j))
    list_d = list(set(out_d))
    list_j.sort(key=take_third)
    list_d.sort(key=take_third)
    return render_template('similarity_coefficient.html', data=data, text_j=list_j, text_d=list_d)


@app.errorhandler(404)
def handle_404_error(err_msg):
    data = count()
    return render_template('404.html', error=err_msg, data=data)


@app.errorhandler(500)
def handle_500_error(err_msg):
    data = count()
    return render_template('500.html', error=err_msg, data=data)


if __name__ == '__main__':
    app.run(debug=True)

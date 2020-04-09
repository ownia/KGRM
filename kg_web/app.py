from flask import Flask, render_template, request, redirect, abort, jsonify
from py2neo import Graph
from collections import OrderedDict
import pandas as pd
import json
import hanlp
import re

app = Flask(__name__)
graph = Graph()


def buildNodes(nodeRecord):
    data = {'id': str(nodeRecord['id(n)'])}
    return {'data': data}


def buildEdges(relationRecord):
    data = {'source': str(relationRecord['id(k)']),
            'target': str(relationRecord['id(n)']),
            'relationship': "生产"}
    return {'data': data}


@app.route('/', methods=("GET", "POST"))
def index():
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
    node = len(graph.nodes)
    edge = len(graph)
    data = "共有" + str(node) + "个节点，" + str(edge) + "个关系"
    return render_template('index.html', data=data,
                           tables=[df.to_html(classes='table table-dark table-striped')],
                           titles=df.columns.values)


@app.route('/graph')
def get_graph():
    nodes = list(map(buildNodes, graph.run('MATCH (n:product) WHERE n.title=~".*索尼.*" RETURN id(n) LIMIT 50').data()))
    nodes.append({'data': {'id': '14'}})
    edges = list(map(buildEdges, graph.run(
        'MATCH (n:product) WHERE n.title=~".*索尼.*" MATCH (k)-[r]-(n) RETURN id(n),id(k) LIMIT 50').data()))
    elements = {'nodes': nodes, 'edges': edges}
    return jsonify(elements)


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
    ner_output = "null."
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

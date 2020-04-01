from flask import Flask, render_template, request, redirect, abort, jsonify
from py2neo import Graph
from collections import OrderedDict
import pandas as pd

app = Flask(__name__)
graph = Graph()


def buildNodes(nodeRecord):
    data = {"id": str(nodeRecord.n._id), "label": next(iter(nodeRecord.n.labels))}
    data.update(nodeRecord.n.properties)
    return {"data": data}


def buildEdges(relationRecord):
    data = {"source": str(relationRecord.r.start_node._id),
            "target": str(relationRecord.r.end_node._id),
            "relationship": relationRecord.r.rel.type}
    return {"data": data}


@app.route('/', methods=("GET", "POST"))
def index():
    pd.set_option('display.float_format', lambda x: '%.4f' % x)
    df = pd.DataFrame(graph.run(
        'MATCH (:class{title:"快递物流品牌"})-[r:RELATION {type :"包括"  }]->(n) RETURN n.title, n.registered ORDER BY '
        'n.registered').to_table())
    df.drop(0, axis=0, inplace=True)
    return render_template('index.html',
                           tables=[df.to_html(classes='table table-dark table-striped')],
                           titles=df.columns.values)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/graph')
def get_graph():
    nodes = map(buildNodes, graph.run('MATCH (:class{title:"快递物流品牌"})-[r:RELATION {type :"包括"  }]->(n) RETURN n'))
    edges = map(buildEdges, graph.run('MATCH (:class{title:"快递物流品牌"})-[r:RELATION {type :"包括"  }]->(n) RETURN r'))
    data = list({"nodes": nodes, "edges": edges})
    return jsonify(elements=data)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, abort, jsonify, g
from py2neo import Graph
from collections import OrderedDict
import pandas as pd
import json
import hanlp
import re
import numpy as np
from neo4j import GraphDatabase, Transaction, basic_auth, kerberos_auth, custom_auth, TRUST_ALL_CERTIFICATES
import synonyms
import heapq
from typing import List
import time

# import jieba

# import warnings
# warnings.filterwarnings("ignore")

app = Flask(__name__)
graph = Graph()
ctx = app.app_context()


# ctx.text = 'match (n:newNode)-[r]-(k:newNode) return n,r,k'


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
    text = ""
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
            text = cypher
        except BaseException as e:
            print('error: ' + str(e))
    data = count()
    return render_template('cypher.html', data=data,
                           tables=[df.to_html(classes='table table-dark table-striped')],
                           titles=df.columns.values, text=text)


@app.route('/graph_visualization', methods=("GET", "POST"))
def graph_visualization():
    data = count()
    text = ""
    if request.method == "POST":
        cypher = request.form['graph-cypher']
        try:
            ctx.text = cypher
            text = cypher
            print('success')
        except BaseException as e:
            print('error: ' + str(e))
    return render_template('graph_visualization.html', data=data, text=text)


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
        except BaseException as e:
            print('error: ' + str(e))
    return render_template('ner.html', data=data, text=text, ner_output=ner_output, page=page)


def jaccard_coefficient(terms_model, reference):
    grams_reference = set(reference)
    grams_model = set(terms_model)
    temp = 0
    for i in grams_reference:
        if i in grams_model:
            temp = temp + 1
    dis = len(grams_model) + len(grams_reference) - temp
    jaccard_res = float(temp / dis)
    return jaccard_res


def dice_coefficient(a, b):
    a_bigrams = set(a)
    b_bigrams = set(b)
    overlap = len(a_bigrams & b_bigrams)
    return overlap * 2.0 / (len(a_bigrams) + len(b_bigrams))


def ochiai_coefficient(a, b):
    a_bigrams = set(a)
    b_bigrams = set(b)
    len_a = len(a_bigrams)
    len_b = len(b_bigrams)
    temp = 0
    for i in b_bigrams:
        if i in a_bigrams:
            temp = temp + 1
    overlap = temp
    # union = pow(pow(len_a, 1 / len_a) * pow(len_b, 1 / len_b), 1 / 2)
    union = pow(len_a * len_b, 1 / 2)
    return float(overlap / union)


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
    data_count = count()
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"), encrypted=False)
    session = driver.session()
    data = session.run("MATCH (m)-[r]->(n) RETURN m.title, r.relation, n.title LIMIT 200")
    # print(data)
    blists = []
    out_j = []
    out_d = []
    out_o = []
    for d in data:
        bs = str(d[0])
        blists.append(bs)
    for i in range(len(blists)):
        for j in range(0, i):
            a = blists[i]
            b = blists[j]
            td_j = jaccard_coefficient(a, b)
            td_d = dice_coefficient(a, b)
            td_o = ochiai_coefficient(a, b)
            std = edit_distance(a, b) / max(len(a), len(b))
            fy = 1 - std
            avg_j = (td_j + fy) / 2
            avg_d = (td_d + fy) / 2
            avg_o = (td_o + fy) / 2
            if avg_j < 1:
                # print(blists[i], blists[j])
                # print('avg_sim: ', avg_j)
                # out_j.append(blists[i] + " " + blists[j] + " " + str(avg_j))
                out_j.append((blists[i], blists[j], str(avg_j)))
            if avg_d < 1:
                # out_d.append(blists[i] + " " + blists[j] + " " + str(avg_d))
                out_d.append((blists[i], blists[j], str(avg_d)))
            if avg_o < 1:
                # out_o.append(blists[i] + " " + blists[j] + " " + str(avg_o))
                out_o.append((blists[i], blists[j], str(avg_o)))
    list_j = list(set(out_j))
    list_d = list(set(out_d))
    list_o = list(set(out_o))
    list_j.sort()
    list_d.sort()
    list_o.sort()

    df = pd.DataFrame(columns=('Entity1', 'Entity2', 'Jaccard', 'Dice', 'Ochiai'))
    for i in range(len(list_j)):
        # print(list_d[i][2])
        # df.append([{'entity1': list_j[i][0], 'entity2': list_j[i][1], 'jaccard': list_j[i][2], 'dice': list_d[i][2],
        #             'ochiai': list_o[i][2]}], ignore_index=True)
        df.loc[i] = [list_j[i][0], list_j[i][1], format(float(list_j[i][2]), '.8f'), format(float(list_d[i][2]), '.8f'),
                     format(float(list_o[i][2]), '.8f')]

    # list_sum = {'jaccard': list_j, 'dice': list_d, 'ochiai': list_o}
    # df = pd.DataFrame(list_sum)
    # html_text = df.to_html()

    jaccard = []
    dice = []
    ochiai = []
    for i in range(len(list_j)):
        jaccard.append(float(list_j[i][2]))
    for i in range(len(list_d)):
        dice.append(float(list_d[i][2]))
    for i in range(len(list_o)):
        ochiai.append(float(list_o[i][2]))
    jaccard_mean = np.mean(jaccard)
    jaccard_var = np.var(jaccard)
    jaccard_std = np.std(jaccard, ddof=1)
    dice_mean = np.mean(dice)
    dice_var = np.var(dice)
    dice_std = np.std(dice, ddof=1)
    ochiai_mean = np.mean(ochiai)
    ochiai_var = np.var(ochiai)
    ochiai_std = np.std(ochiai, ddof=1)
    df2 = pd.DataFrame(columns=('Name', 'Mean', 'Variance', 'Standard Deviation'))
    df2.loc[0] = ['Jaccard', format(float(jaccard_mean), '.8f'), format(float(jaccard_var), '.8f'),
                  format(float(jaccard_std), '.8f')]
    df2.loc[1] = ['Dice', format(float(dice_mean), '.8f'), format(float(dice_var), '.8f'),
                  format(float(dice_std), '.8f')]
    df2.loc[2] = ['Ochiai', format(float(ochiai_mean), '.8f'), format(float(ochiai_var), '.8f'),
                  format(float(ochiai_std), '.8f')]

    return render_template('similarity_coefficient.html', data=data_count,
                           html_text=df.to_html(classes='sim-coe-list') + "<br>",
                           sim_list=df2.to_html(classes='sim-coe-list') + "<br>")


def combination(node: List[str]):
    result = []
    for i in range(len(node)):
        temp = i + 1
        for j in range(len(node) - i - 1):
            # print(node[i] + ", " + node[temp])
            result.append([node[i], node[temp]])
            temp += 1
    return result


def model(j, e, c, o, aa, cn, pa, ra, tn, total, weight1, weight2, weight3):
    # print(total)
    edge = len(graph)
    node = len(graph.nodes)
    # c_new = abs(c)
    c_new = (c + 1) / 2
    zo_value = (float(j / total) + float(c_new / total) + float(o / total)) / 3
    e_new = float((e / total) / node)
    if e_new >= 1.0:
        e_new = 1.0
    tn_new = float((tn / total) / node)
    if tn_new >= 1.0:
        tn_new = 1.0
    cn_new = float((cn / total) / node)
    if cn_new >= 1.0:
        cn_new = 1.0
    pa_mean = float(pa / total)
    pa_new = float(pa_mean / edge)
    if pa_mean >= 2 * edge:
        pa_new = 1.0
    else:
        if pa_new >= 1.0:
            pa_new = 1.0

    lp_value = (float(aa / total) + float(ra / total)) / 2

    result = weight1 * zo_value + (1 - weight1) * (weight2 * lp_value + (1 - weight2) * (
            (weight3 * (e_new + cn_new + tn_new) / 3) + (1 - weight3) * pa_new))
    return result


@app.route('/evaluation_index', methods=("GET", "POST"))
def eva_index():
    data = count()
    text = ""
    max_n_total = []  # synonyms值集合
    similarity_value = []
    link_prediction_value = []

    entity_list_text = ""
    node_list_text = ""
    similarity_value_text = ""
    link_prediction_value_text = ""
    timeline = ""
    result = ""
    formula_combination = ""
    formula_function = ""
    output_1 = ""
    output_2 = ""
    output_3 = ""
    output_4 = ""

    if request.method == "POST":
        try:
            """
            step1: 
                获取eva_post数据
                使用正则表达式切割数据
                使用MSRA_NER_BERT_BASE_ZH模型进行命名实体识别
                将m个实体存储在eva_list2列表中
            """
            eva_text = request.form['eva_post']
            text = eva_text
            start = time.perf_counter()
            # print(eva_text)
            eva_recognizer = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
            list_data = re.split(r'[，。；,\s]\s*', eva_text)
            eva_list1 = []
            eva_list2 = []
            for li in list_data:
                eva_list1.append(list(li))
            eva_output = eva_recognizer(eva_list1)
            for n in eva_output:
                for i in n:
                    if len(i[0]) > 1:
                        eva_list2.append(i[0])
            # print(eva_list2)
            step1_time = time.perf_counter()

            """
            step2:
                针对可能存在的节点label类型为product的实体进行正则表达式匹配
                读取本地node数据文件
                对n个节点数据进行近义词匹配获得5n个数据
                对m个数据进行neo4j模糊查询获得k个数据
                获得5n+k个匹配数据
            """
            entity_list = []
            for i in eva_list2:
                eva_pattern = re.compile(str(i) + r'[a-zA-Z0-9-_]+')
                eva_target = eva_pattern.findall(eva_text)
                # print(eva_target)
                if len(eva_target) > 0:
                    for j in eva_target:
                        entity_list.append(j)
            eva_input = []
            # test = []
            uri = "bolt://localhost:7687"
            driver = GraphDatabase.driver(uri, auth=("neo4j", "password"), encrypted=False)
            session = driver.session()
            for i in eva_list2:
                cypher = 'MATCH(n) WHERE n.title =~\'.*' + str(i) + '.*\' RETURN n.title LIMIT 1'
                se = session.run(cypher)
                for d in se:
                    # test.append(str(d[0]))
                    eva_input.append(str(d[0]))
            # print(entity_list)
            data_list = []
            with open("node_min.txt", "r", encoding="utf-8") as f:
                for line in f:
                    data_list.append(line.strip("\n"))
            # ieba.load_userdict("node.txt")
            for sen1 in entity_list:
                # print(sen1)
                data_dict = {}
                for sen2 in data_list:
                    r = synonyms.compare(sen1, sen2, seg=True)
                    data_dict[str(sen2)] = r
                if len(entity_list) <= 1:
                    max_n = heapq.nlargest(5, data_dict.items(), key=lambda x: x[1])
                    max_n_total.append(max_n)
                    for i in range(len(max_n)):
                        eva_input.append(max_n[i][0])
                else:
                    max_n = heapq.nlargest(2, data_dict.items(), key=lambda x: x[1])
                    max_n_total.append(max_n)
                    for i in range(len(max_n)):
                        eva_input.append(max_n[i][0])
            del data_list[:]
            step2_time = time.perf_counter()

            """
            step3:
                对5n+k个匹配数据构建combination关系
                执行相似度算法和链接预测算法
                    相似度算法
                        Jaccard, Euclidean, Cosine, Overlap
                    链接预测算法
                        Adamic Adar, Common Neighbors, Preferential Attachment,
                        Resource Allocation, Total Neighbors
            """
            # print(eva_input)
            e_index = combination(eva_input)
            jaccard_value = 0
            euclidean_value = 0
            cosine_value = 0
            overlap_value = 0
            adamicadar_value = 0
            commonneighbors_value = 0
            preferentialattachment_value = 0
            resourceallocation_value = 0
            totalneighbors_value = 0

            # Jaccard
            """
            for i in e_index:
                cypher = 'MATCH (p1 {title: "' \
                         + str(i[0]) + '"})-[]-(cuisine1) ' \
                                       'WITH p1, collect(id(cuisine1)) AS p1Cuisine ' \
                                       'MATCH (p2 {title: "' \
                         + str(i[1]) + '"})-[]-(cuisine2) ' \
                                       'WITH p1, p1Cuisine, p2, collect(id(cuisine2)) AS p2Cuisine ' \
                                       'RETURN p1.title AS from, p2.title AS to, ' \
                                       'gds.alpha.similarity.jaccard(p1Cuisine, p2Cuisine) AS similarity'
                se = session.run(cypher)
                for d in se:
                    similarity_value.append("Jaccard " + str(d[2]))            
            """
            # Pearson
            """
            for i in e_index:
                cypher = 'MATCH (p1:product {title: "' \
                         + str(i[0]) + '"})-[]-(cuisine1) ' \
                                       'WITH p1, gds.alpha.similarity.asVector(cuisine1,p1.registered) AS p1Vector ' \
                                       'MATCH (p2:product {title: "' \
                         + str(i[1]) + '"})-[]-(cuisine2) ' \
                                       'WITH p1, p2, p1Vector, gds.alpha.similarity.asVector(cuisine2,p2.registered) ' \
                                       'AS p2Vector ' \
                                       'RETURN p1.title AS from, p2.title AS to, ' \
                                       'gds.alpha.similarity.pearson(p1Vector, p2Vector, {vectorType: "maps"}) AS ' \
                                       'similarity '
                se = session.run(cypher)
                for d in se:
                    similarity_value.append("Pearson" + str(d[2]) + "<br>")
            """
            for i in e_index:
                # Jaccard
                cypher_jaccard = 'MATCH (p1 {title: "' \
                                 + str(i[0]) + '"})-[]-(cuisine1) ' \
                                               'WITH p1, collect(id(cuisine1)) AS p1Cuisine ' \
                                               'MATCH (p2 {title: "' \
                                 + str(i[1]) + '"})-[]-(cuisine2) ' \
                                               'WITH p1, p1Cuisine, p2, collect(id(cuisine2)) AS p2Cuisine ' \
                                               'RETURN p1.title AS from, p2.title AS to, ' \
                                               'gds.alpha.similarity.jaccard(p1Cuisine, p2Cuisine) AS similarity'
                se = session.run(cypher_jaccard)
                value = se.single().value('similarity')
                jaccard_value += value
                similarity_value.append("Jaccard " + str(value))

                # Euclidean
                cypher_euclidean = 'MATCH (p1:product {title: "' \
                                   + str(i[0]) + '"})-[]-() ' \
                                                 'MATCH (p2:product {title: "' \
                                   + str(i[1]) + '"})-[]-() ' \
                                                 'RETURN p1.title AS from, p2.title AS to, ' \
                                                 'gds.alpha.similarity.euclideanDistance(collect(coalesce(toFloat(' \
                                                 'p1.price), gds.util.NaN())), collect(coalesce(toFloat(p2.price), ' \
                                                 'gds.util.NaN()))) AS similarity '
                se = session.run(cypher_euclidean)
                """
                if Transaction.success:
                    for d in se:
                        similarity_value.append("Euclidean " + str(d[2]))
                else:
                    similarity_value.append("Euclidean 0.0")
                """
                for d in se:
                    euclidean_value += d[2]
                    similarity_value.append("Euclidean " + str(d[2]))
                # similarity_value.append("Euclidean " + str(se.single().value('similarity')))

                # Cosine
                cypher_cosine = 'MATCH (p1:product {title: "' \
                                + str(i[0]) + '"})-[]-() ' \
                                              'MATCH (p2:product {title: "' \
                                + str(i[1]) + '"})-[]-() ' \
                                              'RETURN p1.title AS from, p2.title AS to, ' \
                                              'gds.alpha.similarity.cosine(collect(coalesce(toFloat(p1.price), ' \
                                              'gds.util.NaN())), collect(coalesce(toFloat(p2.price), gds.util.NaN(' \
                                              ')))) AS similarity '
                se = session.run(cypher_cosine)
                """
                if Transaction.success:
                    for d in se:
                        similarity_value.append("Cosine " + str(d[2]))
                else:
                    similarity_value.append("Cosine 0.0")                
                """
                for d in se:
                    cosine_value += d[2]
                    similarity_value.append("Cosine " + str(d[2]))
                # similarity_value.append("Cosine " + str(se.single().value('similarity')))

                # Overlap
                cypher_overlap = 'MATCH (p1 {title: "' \
                                 + str(i[0]) + '"})-[]-(cuisine1) ' \
                                               'WITH p1, collect(id(cuisine1)) AS p1Cuisine ' \
                                               'MATCH (p2 {title: "' \
                                 + str(i[1]) + '"})-[]-(cuisine2) ' \
                                               'WITH p1, p1Cuisine, p2, collect(id(cuisine2)) AS p2Cuisine ' \
                                               'RETURN p1.title AS from, p2.title AS to, ' \
                                               'gds.alpha.similarity.overlap(p1Cuisine, p2Cuisine) AS similarity'
                se = session.run(cypher_overlap)
                value = se.single().value('similarity')
                overlap_value += value
                similarity_value.append("Overlap " + str(value))

                # Adamic Adar
                cypher_adamicadar = 'MATCH (p1 {title: "' \
                                    + str(i[0]) + '"})-[]-() ' \
                                                  'MATCH (p2 {title: "' \
                                    + str(i[1]) + '"})-[]-() ' \
                                                  'RETURN gds.alpha.linkprediction.adamicAdar(p1, p2) LIMIT 1'
                se = session.run(cypher_adamicadar)
                value = se.single().value()
                adamicadar_value += value
                link_prediction_value.append("Adamic Adar " + str(value))

                # Common Neighbors
                cypher_commonneighbors = 'MATCH (p1 {title: "' \
                                         + str(i[0]) + '"})-[]-() ' \
                                                       'MATCH (p2 {title: "' \
                                         + str(i[1]) + '"})-[]-() ' \
                                                       'RETURN gds.alpha.linkprediction.commonNeighbors(p1, p2) LIMIT 1'
                se = session.run(cypher_commonneighbors)
                value = se.single().value()
                commonneighbors_value += value
                link_prediction_value.append("Common Neighbors " + str(value))

                # Preferential Attachment
                cypher_preferentialattachment = 'MATCH (p1 {title: "' \
                                                + str(i[0]) + '"})-[]-() ' \
                                                              'MATCH (p2 {title: "' \
                                                + str(i[1]) + '"})-[]-() ' \
                                                              'RETURN gds.alpha.linkprediction' \
                                                              '.preferentialAttachment(p1, p2) LIMIT 1'
                se = session.run(cypher_preferentialattachment)
                value = se.single().value()
                preferentialattachment_value += value
                link_prediction_value.append("Preferential Attachment " + str(value))

                # Resource Allocation
                cypher_resourceallocation = 'MATCH (p1 {title: "' \
                                            + str(i[0]) + '"})-[]-() ' \
                                                          'MATCH (p2 {title: "' \
                                            + str(i[1]) + '"})-[]-() ' \
                                                          'RETURN gds.alpha.linkprediction.resourceAllocation(p1, ' \
                                                          'p2) LIMIT 1'
                se = session.run(cypher_resourceallocation)
                value = se.single().value()
                resourceallocation_value += value
                link_prediction_value.append("Resource Allocation " + str(value))

                # Total Neighbors
                cypher_totalneighbors = 'MATCH (p1 {title: "' \
                                        + str(i[0]) + '"})-[]-() ' \
                                                      'MATCH (p2 {title: "' \
                                        + str(i[1]) + '"})-[]-() ' \
                                                      'RETURN gds.alpha.linkprediction.totalNeighbors(p1, p2) LIMIT 1'
                se = session.run(cypher_totalneighbors)
                value = se.single().value()
                totalneighbors_value += value
                link_prediction_value.append("Total Neighbors " + str(value))
            step3_time = time.perf_counter()

            """
            step4:
                将算法结果经过模型进行权重和偏置处理
                将evaluation_index执行归一化处理
                输出数据
            """
            # print(entity_list)
            # print(eva_list2)
            for i in entity_list:
                entity_list_text += i + "<br>"
                temp = text.replace(str(i), str("<mark>" + i + "</mark> "))
                text = temp
            for i in eva_list2:
                entity_list_text += i + "<br>"
                temp = text.replace(str(i), str("<mark>" + i + "</mark> "))
                text = temp

            node_list = set(eva_input)
            for i in node_list:
                node_list_text += i + "<br>"
            for i in similarity_value:
                similarity_value_text += i + "<br>"
            for i in link_prediction_value:
                link_prediction_value_text += i + "<br>"

            total = len(e_index)
            result = "<strong>9</strong>种算法结果均值如下:<br>"
            result += "<strong>Jaccard_mean:</strong> " + str(float(jaccard_value / total)) + "<br>"
            result += "<strong>Euclidean_mean:</strong> " + str(float(euclidean_value / total)) + "<br>"
            result += "<strong>Cosine_mean:</strong> " + str(float(cosine_value / total)) + "<br>"
            result += "<strong>Overlap_mean:</strong> " + str(float(overlap_value / total)) + "<br>"
            result += "<strong>Adamic_Adar_mean:</strong> " + str(float(adamicadar_value / total)) + "<br>"
            result += "<strong>Common_Neighbors_mean:</strong> " + str(float(commonneighbors_value / total)) + "<br>"
            result += "<strong>Preferential_Attachment_mean:</strong> " + str(
                float(preferentialattachment_value / total)) + "<br>"
            result += "<strong>Resource_Allocation_mean:</strong> " + str(
                float(resourceallocation_value / total)) + "<br>"
            result += "<strong>Total_Neighbors_mean:</strong> " + str(float(totalneighbors_value / total)) + "<br>"
            eva_index_result = model(jaccard_value, euclidean_value, cosine_value, overlap_value, adamicadar_value,
                                     commonneighbors_value, preferentialattachment_value, resourceallocation_value,
                                     totalneighbors_value, total, 0.5, 0.5, 0.8)

            output_1 = "共识别实体<strong>" + str(len(entity_list) + len(eva_list2)) + "</strong>个，匹配节点<strong>" + str(
                len(node_list)) + "</strong>个，识别节点通过combination模块、<strong>9</strong>种相似度算法和链接预测算法获得<strong>" + str(
                total * 9) + "</strong>个结果。"
            output_2 = "<br>将<strong>" + str(total * 9) + "</strong>个结果通过上层模型函数:<br>"
            formula_function = "$$ f(n)=(weight1\\times\\frac{j+\\frac{c+1}{2}+o}{3})+(1-weight1)\\times\\{" \
                               "weight2\\times\\frac{aa+ra}{2}+(1-weight2)\\times[weight3\\times\\frac{e+tn+cn}{" \
                               "node\\times3}+(1-weight3)\\times\\frac{pa}{edge}])\\} $$ "
            output_3 = "计算得出该文本的评价指数(evaluation_index)为<strong>" + str(eva_index_result) + "</strong>。<br><br>"
            if eva_index_result > 0.8:
                output_4 = "<strong>该家电文本包含资源关系优秀。</strong>"
            elif 0.25 < eva_index_result <= 0.8:
                output_4 = "<strong>该家电文本包含资源关系还有提升空间。</strong>"
            else:
                output_4 = "<strong>该家电文本包含资源关系较差。</strong>"

            if len(entity_list) <= 1:
                formula_combination = "$$C\\binom{2}{5\\times " + str(len(eva_input)) + "}\\times 9=" + str(
                    total * 9) + "$$"
            else:
                formula_combination = "$$C\\binom{2}{2\\times " + str(len(eva_input)) + "}\\times 9=" + str(
                    total * 9) + "$$"

            step4_time = time.perf_counter()
            timeline = "<strong>Step1:  " + str(step1_time - start) + "s</strong><br>"
            timeline += "获取eva_post数据<br>"
            timeline += "使用正则表达式切割数据<br>"
            timeline += "使用MSRA_NER_BERT_BASE_ZH模型进行命名实体识别<br>"
            timeline += "将m个实体存储在eva_list2列表中<br><br>"
            timeline += "<strong>Step2:  " + str(step2_time - step1_time) + "s</strong><br>"
            timeline += "针对可能存在的节点label类型为product的实体进行正则表达式匹配<br>"
            timeline += "读取本地node数据文件<br>"
            timeline += "对n个节点数据进行近义词匹配获得5n个数据<br>"
            timeline += "对m个数据进行neo4j模糊查询获得k个数据<br>"
            timeline += "获得5n+k个匹配数据<br><br>"
            timeline += "<strong>Step3:  " + str(step3_time - step2_time) + "s</strong><br>"
            timeline += "对5n+k个匹配数据构建combination关系<br>"
            timeline += "执行相似度算法和链接预测算法<br><br>"
            timeline += "<strong>Step4:  " + str(step4_time - step3_time) + "s</strong><br>"
            timeline += "将算法结果经过模型函数进行权重和偏置处理<br>"
            timeline += "将evaluation_index执行归一化处理<br>"
            timeline += "输出数据<br><br>"
            timeline += "<strong>Total time:  " + str(step4_time - start) + "s</strong><br>"

        except BaseException as e:
            print('Error: ' + str(e))
            text = 'Error: ' + str(e)

    return render_template('evaluation_index.html', data=data, text=text, entity_list_text=entity_list_text,
                           node_list_text=node_list_text, similarity_value_text=similarity_value_text,
                           link_prediction_value_text=link_prediction_value_text, timeline=timeline, result=result,
                           formula_combination=formula_combination, formula_function=formula_function,
                           output_1=output_1, output_2=output_2, output_3=output_3, output_4=output_4)


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

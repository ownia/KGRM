import hanlp
import numpy as np
from neo4j import GraphDatabase, basic_auth, kerberos_auth, custom_auth, TRUST_ALL_CERTIFICATES
import pandas as pd
import time


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


def sim_coe():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    session = driver.session()
    data = session.run("MATCH (m)-[r]->(n) RETURN m.title, r.relation, n.title")
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
    # list_j.sort()
    # list_d.sort()
    # list_o.sort()

    # df = pd.DataFrame(columns=('Entity1', 'Entity2', 'Jaccard', 'Dice', 'Ochiai'))
    # for i in range(len(list_j)):
    #     # print(list_d[i][2])
    #     # df.append([{'entity1': list_j[i][0], 'entity2': list_j[i][1], 'jaccard': list_j[i][2], 'dice': list_d[i][2],
    #     #             'ochiai': list_o[i][2]}], ignore_index=True)
    #     df.loc[i] = [list_j[i][0],
    #                  list_j[i][1],
    #                  format(float(list_j[i][2]), '.8f'),
    #                  format(float(list_d[i][2]), '.8f'),
    #                  format(float(list_o[i][2]), '.8f')]

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
    print(df2)


def data_session():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    session = driver.session()
    data = session.run("MATCH (m)-[r]-(n) RETURN m.title, r.relation, n.title")

    file = open("data.txt", "w", encoding="utf-8")
    for d in data:
        bs = str(d[0])
        file.writelines(bs + "\n")
    file.close()


def test():
    data_list = []
    with open("data.txt", "r", encoding="utf-8") as f:
        for line in f:
            data_list.append(line.strip("\n"))
    # out_j = []
    # out_d = []
    out_o = []
    for i in range(len(data_list)):
        for j in range(0, i):
            a = data_list[i]
            b = data_list[j]
            # td_j = jaccard_coefficient(a, b)
            # td_d = dice_coefficient(a, b)
            td_o = ochiai_coefficient(a, b)
            std = edit_distance(a, b) / max(len(a), len(b))
            fy = 1 - std
            # avg_j = (td_j + fy) / 2
            # avg_d = (td_d + fy) / 2
            avg_o = (td_o + fy) / 2
            # if avg_j < 1:
            #     # print(blists[i], blists[j])
            #     # print('avg_sim: ', avg_j)
            #     # out_j.append(blists[i] + " " + blists[j] + " " + str(avg_j))
            #     out_j.append((data_list[i], data_list[j], str(avg_j)))
            # if avg_d < 1:
            #     # out_d.append(blists[i] + " " + blists[j] + " " + str(avg_d))
            #     out_d.append((data_list[i], data_list[j], str(avg_d)))
            if avg_o < 1:
                # out_o.append(blists[i] + " " + blists[j] + " " + str(avg_o))
                out_o.append((data_list[i], data_list[j], str(avg_o)))
    del data_list[:]
    print("data success")
    # list_j = list(set(out_j))
    # list_d = list(set(out_d))
    list_o = list(set(out_o))
    # del out_j[:]
    # del out_d[:]
    del out_o[:]
    jaccard = []
    dice = []
    ochiai = []
    # for i in range(len(list_j)):
    #     jaccard.append(float(list_j[i][2]))
    # for i in range(len(list_d)):
    #     dice.append(float(list_d[i][2]))
    for i in range(len(list_o)):
        ochiai.append(float(list_o[i][2]))
    # del list_j[:]
    # del list_d[:]
    del list_o[:]
    print("append success")
    # jaccard_mean = np.mean(jaccard)
    # jaccard_var = np.var(jaccard)
    # jaccard_std = np.std(jaccard, ddof=1)
    # dice_mean = np.mean(dice)
    # dice_var = np.var(dice)
    # dice_std = np.std(dice, ddof=1)
    ochiai_mean = np.mean(ochiai)
    ochiai_var = np.var(ochiai)
    ochiai_std = np.std(ochiai, ddof=1)
    df2 = pd.DataFrame(columns=('Name', 'Mean', 'Variance', 'Standard Deviation'))
    # df2.loc[0] = ['Jaccard', format(float(jaccard_mean), '.8f'), format(float(jaccard_var), '.8f'),
    #               format(float(jaccard_std), '.8f')]
    # df2.loc[1] = ['Dice', format(float(dice_mean), '.8f'), format(float(dice_var), '.8f'),
    #               format(float(dice_std), '.8f')]
    df2.loc[2] = ['Ochiai', format(float(ochiai_mean), '.8f'), format(float(ochiai_var), '.8f'),
                  format(float(ochiai_std), '.8f')]
    print(df2)


if __name__ == '__main__':
    start = time.perf_counter()
    # sim_coe()
    # data_session()
    test()
    end = time.perf_counter()
    print(end - start)

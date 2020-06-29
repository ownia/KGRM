import synonyms
import heapq
from neo4j import GraphDatabase
import time
from typing import List


def comp():
    sen1 = "海尔CXW-200"
    data_list = []
    with open("data.txt", "r", encoding="utf-8") as f:
        for line in f:
            data_list.append(line.strip("\n"))
    with open("output.txt", "w", encoding="utf-8") as f:
        for sen2 in data_list:
            r = synonyms.compare(sen1, sen2, seg=True)
            f.writelines(sen2 + "," + str(r) + "\n")
    print("success")


def data_session():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
    session = driver.session()
    data = session.run("MATCH (n) RETURN n.title")
    file = open("node.txt", "w", encoding="utf-8")
    for d in data:
        bs = str(d[0])
        file.writelines(bs + "\n")
    file.close()


def test():
    data_dict = {}
    sen1 = "海尔CXW-200"
    data_list = []
    with open("node.txt", "r", encoding="utf-8") as f:
        for line in f:
            data_list.append(line.strip("\n"))
    with open("output.txt", "w", encoding="utf-8") as f:
        for sen2 in data_list:
            r = synonyms.compare(sen1, sen2, seg=True)
            f.writelines(sen2 + "," + str(r) + "\n")
            data_dict[str(sen2)] = r
    del data_list[:]
    max_n = heapq.nlargest(10, data_dict.items(), key=lambda x: x[1])
    file = open("max_n.txt", "w", encoding="utf-8")
    file.writelines(str(max_n))
    file.close()


def combination(node: List[str]):
    result = []
    for i in range(len(node)):
        temp = i + 1
        for j in range(len(node) - i - 1):
            # print(node[i] + ", " + node[temp])
            result.append([node[i], node[temp]])
            temp += 1
    return result


def new_test():
    data_list = []
    data_dict = {}
    with open("node.txt", "r", encoding="utf-8") as f:
        for line in f:
            data_list.append(line.strip("\n"))
    for sen2 in data_list:
        r = synonyms.compare("海尔BCD476FDGJds", sen2, seg=True)
        data_dict[str(sen2)] = r
    max_n = heapq.nlargest(5, data_dict.items(), key=lambda x: x[1])
    print(max_n)
    node_list = []
    for i in range(len(max_n)):
        node_list.append(max_n[i][0])
    print(node_list)
    e_index = combination(node_list)
    print(e_index)


if __name__ == '__main__':
    start = time.perf_counter()
    # test()
    new_test()
    end = time.perf_counter()
    print(end - start)
    # data_session()

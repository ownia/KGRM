import synonyms
import heapq
from neo4j import GraphDatabase
import time


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


if __name__ == '__main__':
    start = time.perf_counter()
    test()
    end = time.perf_counter()
    print(end - start)
    # data_session()

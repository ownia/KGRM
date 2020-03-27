# _*_ coding:utf-8 _*_
import csv
import pandas as pd
import csv


# 筛选公司和注册资本
def csv_clean(csvfile):
    csv_data = csv.reader(open(csvfile, 'r', encoding='utf-8'))
    with open("clean.txt", "w", encoding="utf-8")as f:
        for line in csv_data:
            f.writelines(line[0] + "," + line[2] + "\n")


def delete(file):
    fp = open(file, 'r+', encoding='utf-8')
    data = fp.readlines()
    with open('fo.txt', 'w', encoding='utf-8')as f:
        for line in data:
            line_new = line.replace(',0,,', '')
            f.writelines(line_new)
    fp.close()


def c2n(entityfile):
    # 读取三元组文件
    h_r_t_name = [":START_ID", "role", ":END_ID"]
    h_r_t = pd.read_table(entityfile, decimal="\t", names=h_r_t_name, encoding="utf-8")
    print(h_r_t.info())
    print(h_r_t.head())
    # 去除重复实体
    entity = set()
    entity_h = h_r_t[':START_ID'].tolist()
    entity_t = h_r_t[':END_ID'].tolist()
    for i in entity_h:
        entity.add(i)
    for i in entity_t:
        entity.add(i)
    print(entity)
    # 保存节点文件
    csvf_entity = open("entity.csv", "w", newline='', encoding='utf-8')
    w_entity = csv.writer(csvf_entity)
    # 实体ID，要求唯一，名称，LABEL标签，可自己不同设定对应的标签
    w_entity.writerow(("entity:ID", "name", ":LABEL"))
    entity = list(entity)
    entity_dict = {}
    for i in range(len(entity)):
        w_entity.writerow(("e" + str(i), entity[i], "my_entity"))
        entity_dict[entity[i]] = "e" + str(i)
    csvf_entity.close()
    # 生成关系文件，起始实体ID，终点实体ID，要求与实体文件中ID对应，:TYPE即为关系
    h_r_t[':START_ID'] = h_r_t[':START_ID'].map(entity_dict)
    h_r_t[':END_ID'] = h_r_t[':END_ID'].map(entity_dict)
    h_r_t[":TYPE"] = h_r_t['role']
    h_r_t.pop('role')
    h_r_t.to_csv("roles.csv", index=False)


if __name__ == '__main__':
    node = "node.csv"
    rel = "rel.csv"
    entity = "output.txt"
    # c2n(entity)
    # csv_clean("info.csv")
    delete("clean.txt")

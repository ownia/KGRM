import json
import csv
import codecs
import sys
import os


# 删除冗余数据
def delete_whitespace(jsonName, txtName):
    fp = open(jsonName, encoding='utf-8')
    wf = open(txtName, 'w', encoding='utf-8')
    for each in fp.readlines():
        str = each.replace(" ", "").replace("\\r", "").replace("\\n", "").replace("\\t", "").replace("￥", "")
        wf.write(str)
    fp.close()
    wf.close()


def price_clean(filedir):
    filenames = os.listdir(filedir)
    f = open('result.txt', 'w', encoding='utf-8')
    for filename in filenames:
        filepath = filedir + '/' + filename
        # 遍历单个文件，读取行数
        for line in open(filepath, encoding='utf-8'):
            f.writelines(line)
        f.write('\n')
    f.close()


if __name__ == '__main__':
    name = 'whirlpool'
    jsonName = name + '.json'
    txtName = name + '.txt'
    # delete_whitespace(jsonName, txtName)
    filedir = './data'
    price_clean(filedir)
    print("deleted.")

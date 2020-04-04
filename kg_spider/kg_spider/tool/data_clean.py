import json
import csv
import codecs
import sys


# 删除冗余数据
def delete_whitespace(jsonName, txtName):
    fp = open(jsonName, encoding='utf-8')
    wf = open(txtName, 'w', encoding='utf-8')
    for each in fp.readlines():
        str = each.replace(" ", "").replace("\\r", "").replace("\\n", "").replace("\\t", "").replace("￥", "")
        wf.write(str)
    fp.close()
    wf.close()


if __name__ == '__main__':
    name = 'whirlpool'
    jsonName = name + '.json'
    txtName = name + '.txt'
    delete_whitespace(jsonName, txtName)
    print("deleted.")

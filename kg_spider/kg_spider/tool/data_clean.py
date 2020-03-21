import json
import csv
import codecs
import sys


def delete_whitespace(jsonName, txtName):
    fp = open(jsonName, encoding='utf-8')
    wf = open(txtName, 'w', encoding='utf-8')
    for each in fp.readlines():
        str = each.replace(" ", "").replace("\\r", "").replace("\\n", "").replace("\\t", "")
        wf.write(str)
    fp.close()
    wf.close()


if __name__ == '__main__':
    name = 'tcl'
    jsonName = name + '.json'
    txtName = name + '.txt'
    delete_whitespace(jsonName, txtName)
    print("deleted.")

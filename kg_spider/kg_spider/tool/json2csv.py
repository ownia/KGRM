import json
import csv
import codecs


def json2csv(jsonName, csvName):
    jsonData = codecs.open(jsonName, 'r', 'utf-8')
    csvfile = open(csvName, 'w', newline='')
    writer = csv.writer(csvfile, delimiter='\t')
    flag = True
    for line in jsonData:
        dic = json.loads(line[0:-1], strict=False)
        if flag:
            keys = list(dic.keys())
            print(keys)
            writer.writerow(keys)
            flag = False
        else:
            writer.writerow(list(dic.values()))
    jsonData.close()
    csvfile.close()


if __name__ == '__main__':
    name = 'littleswan'
    jsonName = name + '.json'
    csvName = name + '.csv'
    json2csv(jsonName, csvName)
    print("transformed.")

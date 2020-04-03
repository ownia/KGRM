import json
import csv
import codecs


# json文件转换为csv文件
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


# 剥离出name,content,entirety
def cut_data(jsonName, name):
    with open(jsonName, 'r', encoding='utf-8') as f:
        temp = json.load(f)
        name_file = open(name + '_name.txt', mode='w', encoding='utf-8')
        price_file = open(name + '_price.txt', mode='w', encoding='utf-8')
        content_file = open(name + '_content.txt', mode='w', encoding='utf-8')
        entirety_file = open(name + '_entirety_file.txt', mode='w', encoding='utf-8')
        for t in range(len(temp)):
            str1 = str(temp[t]['name']).replace("['", "").replace("']", "")
            str2 = str(temp[t]['price'][0]).replace("['", "").replace("']", "")
            str3 = str(temp[t]['content']).replace("['", "").replace("']", "")
            str4 = str1 + ',' + str2
            str5 = str1 + ',' + str3
            str6 = str4 + ',' + str3
            name_file.writelines(str1 + '\n')
            price_file.writelines(str4 + '\n')
            content_file.writelines(str5 + '\n')
            entirety_file.writelines(str6 + '\n')
        name_file.close()
        price_file.close()
        content_file.close()
        entirety_file.close()


if __name__ == '__main__':
    name = 'leader'
    jsonName = name + '.json'
    csvName = name + '.csv'
    # json2csv(jsonName, csvName)
    cut_data(jsonName, name)
    print("transformed.")

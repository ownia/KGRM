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


def cut_data(jsonName):
    with open(jsonName, 'r', encoding='utf-8') as f:
        temp = json.load(f)
        name_file = open('name.txt', mode='w', encoding='utf-8')
        content_file = open('content.txt', mode='w', encoding='utf-8')
        entirety_file = open('entirety_file.txt', mode='w', encoding='utf-8')
        for t in range(len(temp)):
            str1 = str(temp[t]['name']).replace("['", "").replace("']", "")
            str2 = str(temp[t]['content']).replace("['", "").replace("']", "")
            str3 = str1 + ',' + str2
            name_file.writelines(str1 + '\n')
            content_file.writelines(str2 + '\n')
            entirety_file.writelines(str3 + '\n')
        name_file.close()
        content_file.close()
        entirety_file.close()


if __name__ == '__main__':
    name = 'haier2'
    jsonName = name + '.json'
    csvName = name + '.csv'
    # json2csv(jsonName, csvName)
    cut_data(jsonName)
    print("transformed.")

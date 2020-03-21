import json


def delete_whitespace(jsonName, txtName):
    fp = open(jsonName, encoding='utf-8')
    wf = open(txtName, 'w', encoding='utf-8')
    for each in fp.readlines():
        str = each.replace(" ", "")
        wf.write(str)
    fp.close()
    wf.close()


if __name__ == '__main__':
    name = 'haier'
    jsonName = name + '.json'
    txtName = name + '.txt'
    delete_whitespace(jsonName, txtName)
    print("deleted.")

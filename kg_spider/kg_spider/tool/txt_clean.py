# 添加前置实体和关系
def addentity(inputfile):
    fp = open(inputfile, "r", encoding="utf-8")
    lines = fp.readlines()
    str = "小天鹅(LittleSwan),生产,"
    with open("relation.csv", "w", encoding="utf-8")as f:
        f.write('newNode,relation,product\n')
        for line in lines:
            line_new = line.replace('（', '(').replace('）', ')')
            f.write(str + line_new)
    fp.close()


# 添加后置实体
def append(inputfile):
    fp = open(inputfile, encoding="utf-8")
    lines = fp.readlines()
    with open("node.csv", "w", encoding="utf-8")as f:
        f.write('title,label\n')
        for line_list in lines:
            line_new = line_list.replace('\n', '').replace('（', '(').replace('）', ')')
            line_new = line_new + r',product' + '\n'
            f.write(line_new)
    fp.close()


# 快递物流绑定函数
def kdbind(inputfile):
    fp = open(inputfile, encoding="utf-8")
    lines = fp.readlines()
    with open("output.txt", "a+", encoding="utf-8")as f:
        for line in lines:
            line_new = line.replace('{"name": "', '').replace('"},', '')
            f.write(line_new)


if __name__ == '__main__':
    data = "littleswan"
    inputfile = data + "_name.txt"
    addentity(inputfile)
    append(inputfile)

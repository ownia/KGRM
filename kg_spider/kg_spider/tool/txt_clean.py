def addentity(inputfile):
    fp = open(inputfile, "r", encoding="utf-8")
    lines = fp.readlines()
    str = "家电品牌,包括,"
    with open("output.txt", "a+", encoding="utf-8")as f:
        for line in lines:
            line_new = line.replace('（', '(').replace('）', ')')
            f.write(str + line_new)
    fp.close()


def append(inputfile):
    fp = open(inputfile, encoding="utf-8")
    lines = fp.readlines()
    with open("output.txt", "a+", encoding="utf-8")as f:
        for line_list in lines:
            line_new = line_list.replace('\n', '').replace('（', '(').replace('）', ')')
            line_new = line_new + r',newNode' + '\n'
            f.write(line_new)
    fp.close()


if __name__ == '__main__':
    inputfile = "1.txt"
    addentity(inputfile)

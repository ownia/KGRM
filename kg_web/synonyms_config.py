import synonyms

sen1 = "海尔CXW-200"
data_list = []
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        data_list.append(line.strip("\n"))
with open("output.txt", "w", encoding="utf-8") as f:
    for sen2 in data_list:
        r = synonyms.compare(sen1, sen2, seg=True)
        f.writelines(sen2 + "," + str(r) + "\n")
print("success")

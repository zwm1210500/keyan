import jieba

f = open("./1.csv", "r", encoding = "gbk")
str = f.read()
f.close()

mlist = str.split('\n')
mlist.remove(mlist[-1])
str = ''
for i in range(0, len(mlist)):
    mlist[i] = mlist[i].strip().split('|')
    str += mlist[i][4] + '\n'

# print(str)


jieba.load_userdict("userdict.txt")

#jieba.add_word("分词法")
#jieba.add_word("不喜欢")
seg_list = jieba.cut(str)
result = " ".join(seg_list)

f = open("./1_1.txt", "w", encoding = "gbk")
f.write(result)
f.close()

import os
import sys
import codecs
# import jieba


pos_num = 0
unlabel_num = 0
test_num = 0



def loadDocs(filePath, encoding='utf-8'):
    f = codecs.open(filePath, 'r', encoding=encoding)
    content = f.read()
    f.close()
    text_list = str(content).split('\n')
    text_list.remove( text_list[-1] )
    for i in range(0, len(text_list)):
        text_list[i] = text_list[i].strip()
    return text_list


'''
# io 预备
# 读取 pos
f1 = codecs.open("./结巴分词/yuliao_pos.csv", 'r', encoding="utf-8")
content = f1.read()
f1.close()
text_list = content.split('\n')

text_list.remove(text_list[-1])
for i in range(0, len(text_list)):
    text_list[i] = str(text_list[i]).strip()

pos_num = len(text_list)
# 读取 pos

# 读取 unlabel
f2 = open("./结巴分词/yuliao_unlabel.csv", 'r', encoding="utf-8")
content = f2.read()
f2.close()
temp = content.split('\n')

temp.remove(temp[-1])
for i in range(0, len(temp)):
    temp[i] = str(temp[i]).strip()

unlabel_num = len(temp)
# 读取 unlabel

# 总文档中加入 unlabel
text_list.extend(temp)
# 总文档中加入 unlabel

# 读取 test
f3 = open("./结巴分词/yuliao_test.csv", 'r', encoding="utf-8")
content = f3.read()
f3.close()
temp = content.split('\n')

temp.remove(temp[-1])
for i in range(0, len(temp)):
    temp[i] = str(temp[i]).strip()

test_num = len(temp)
# 读取 test

# 总文档中加入 test
text_list.extend(temp)
print('pos: ' + str(pos_num) + ', unlabel: ' + str(unlabel_num) + ', test: ' + str(test_num))
# 总文档中加入 test
# io 预备


# 分词
pynlpir.open()

for i in range(0, len(text_list)):
    text_list[i] = text_list[i].split('|')
    text_list[i] = pynlpir.segment(text_list[i][-1], pos_tagging=False)
    # print(text_list[i])
# 分词


# 去停用词
# 读取停用词
f = open('./结巴分词/stop_word_UTF_8.txt', 'r', encoding='utf-8')
content = f.read()
f.close()
stop_word_list = content.split('\n')
stop_word_list.remove( stop_word_list[-1] )
# 读取停用词

for i in range(0, len(text_list)):
    mlist = []
    for a in text_list[i]:
        if a in stop_word_list:
            continue
        else:
            mlist.append(a)
    text_list[i] = mlist
# 去停用词
'''

word_set = set()

text_list = loadDocs('./Lpu_Input/yuliao_pos.nlpresult')
i = 0
for doc in text_list:
    parts = doc.split('|')
    words = parts[-1].split(' ')
    for word in words:
        word_set.add(word)
    print('process pos', i)
    i += 1

text_list = loadDocs('./Lpu_Input/yuliao_unlabel.nlpresult')
i = 0
for doc in text_list:
    parts = doc.split('|')
    words = parts[-1].split(' ')
    for word in words:
        word_set.add(word)
    print('process unlabel', i)
    i += 1

text_list = loadDocs('./Lpu_Input/yuliao_test.nlpresult')
i = 0
for doc in text_list:
    parts = doc.split('|')
    words = parts[-1].split(' ')
    for word in words:
        word_set.add(word)
    print('process test', i)
    i += 1


# 写入临时词库文件
f = codecs.open('./data/Word_Library.wordlib', 'w', encoding='utf-8')

word_lib = list(word_set)
word_lib.sort()

for i in range(0, len(word_lib)):
    f.write( word_lib[i] + ' ' + str(i + 1) + '\n')
    print('writing word', i)

f.close()
# 写入临时词库文件


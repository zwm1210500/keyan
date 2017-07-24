import os
import sys
import codecs
import jieba


pos_num = 0
unlabel_num = 0
test_num = 0
stop_word_list = []
my_feature_set = []


# 分词
def mySegment(text_list):
    for i in range(0, len(text_list)):
        parts = text_list[i].split('|')
        text_list[i] = parts
        text_list[i].remove( text_list[i][-1] )
        text_list[i].append( jieba.lcut(parts[-1], cut_all=False) )
    return text_list
# 分词


# 读取停用词
def loadTYC():
    f = codecs.open('./结巴分词/stop_word_UTF_8.txt', 'r', encoding='utf-8')
    content = f.read()
    f.close()
    stop_word_list = content.split('\r\n')
    stop_word_list.remove( stop_word_list[-1] )
    return stop_word_list
# 读取停用词
# 去停用词
def quTYC(text_list, stop_word_list):
    for i in range(0, len(text_list)):
        j = 0
        while j < len(text_list[i][-1]):
            word = text_list[i][-1][j]
            if word in stop_word_list:
                text_list[i][-1].remove( word )
            else:
                j += 1
    return text_list
# 去停用词


# 匹配 特征集
def loadFeature():
    f = codecs.open('./test/feature_set.txt', 'r', encoding='utf-8')
    content = f.read()
    f.close()
    my_feature_set = content.split('\n')
    my_feature_set.remove( my_feature_set[-1] )
    return my_feature_set
def feature_process(text_list, my_feature_set):
    for i in range(0, len(text_list)):
        for word in text_list[i][-1]:
            if word in my_feature_set:
                continue
            else:
                text_list[i][-1].remove(word)
    return text_list

# 匹配 特征集


if __name__ == '__main__':
    stop_word_list = loadTYC() # 读取停用词集
    my_feature_set = loadFeature() # 读取特征集


    # io 预备
    # 处理 pos
    f1 = codecs.open("./temp/yuliao_pos.csv", 'r', encoding="utf-8")
    content = f1.read()
    f1.close()
    text_list = content.split('\n')

    text_list.remove(text_list[-1])
    for i in range(0, len(text_list)):
        text_list[i] = str(text_list[i]).strip()

    pos_num = len(text_list)

    text_list = mySegment(text_list) # 分词
    text_list = quTYC(text_list, stop_word_list) # 去停用词
    text_list = feature_process(text_list, my_feature_set) # 有关特征词处理

    f = open('./test/yuliao_pos.nlpresult', 'w', encoding='utf-8')
    for doc in text_list:
        if doc[-1] != []:
            for i in range(0, len(doc) - 1):
                f.write(doc[i] + '|')
            f.write( ' '.join(doc[-1]) + '\n' )
    f.close()

    print('pos Done')
    # 处理 pos


    # 处理 unlabel
    f2 = open("./结巴分词/yuliao_unlabel.csv", 'r', encoding="utf-8")
    content = f2.read()
    f2.close()
    temp = content.split('\n')

    temp.remove(temp[-1])
    for i in range(0, len(temp)):
        temp[i] = str(temp[i]).strip()

    unlabel_num = len(temp)

    text_list = mySegment(temp) # 分词
    text_list = quTYC(text_list, stop_word_list) # 去停用词
    text_list = feature_process(text_list, my_feature_set) # 有关特征词处理

    f = open('./结巴分词/yuliao_unlabel.nlpresult', 'w', encoding='utf-8')
    for doc in text_list:
        if doc[-1] != []:
            for i in range(0, len(doc) - 1):
                f.write(doc[i] + '|')
            f.write( ' '.join(doc[-1]) + '\n' )
    f.close()

    print('unlabel Done')
    # 处理 unlabel


    # 处理 test
    f3 = open("./结巴分词/yuliao_test.csv", 'r', encoding="utf-8")
    content = f3.read()
    f3.close()
    temp = content.split('\n')

    temp.remove(temp[-1])
    for i in range(0, len(temp)):
        temp[i] = str(temp[i]).strip()

    test_num = len(temp)

    text_list = mySegment(temp) # 分词
    text_list = quTYC(text_list, stop_word_list) # 去停用词
    text_list = feature_process(text_list, my_feature_set) # 有关特征词处理

    f = open('./结巴分词/yuliao_test.nlpresult', 'w', encoding='utf-8')
    for doc in text_list:
        if doc[-1] != []:
            for i in range(0, len(doc) - 1):
                f.write(doc[i] + '|')
            f.write( ' '.join(doc[-1]) + '\n' )
    f.close()

    print('test Done')
    # 处理 test
    # io 预备

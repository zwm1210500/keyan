import os
import sys
import codecs
import jieba


pos_num = 0
unlabel_num = 0
test_num = 0
stop_word_list = []
my_feature_set = []


def loadDocs(filePath, encoding='utf-8'):
    f = codecs.open(filePath, 'r', encoding=encoding)
    content = f.read()
    f.close()
    text_list = str(content).split('\n')
    text_list.remove( text_list[-1] )
    for i in range(0, len(text_list)):
        text_list[i] = text_list[i].strip()
    return text_list

# 分词
def mySegment(text_list):
    for i in range(0, len(text_list)):
        parts = text_list[i].split('|')
        sResult = jieba.lcut(parts[-1], cut_all=False)
        text_list[i] = parts
        text_list[i].remove( text_list[i][-1] )
        text_list[i].append( sResult )
        print('mySegment', i)
    return text_list
# 分词


# 读取停用词
def loadTYC():
    f = codecs.open('./data/stop_word_UTF_8.txt', 'r', encoding='utf-8')
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
        print('quTYC', i)
    return text_list
# 去停用词


# 匹配 特征集
def loadFeature():
    f = codecs.open('./data/feature_set.txt', 'r', encoding='utf-8')
    content = f.read()
    f.close()
    my_feature_set = content.split('\n')
    my_feature_set.remove( my_feature_set[-1] )
    return my_feature_set
def feature_process(text_list, my_feature_set):
    for i in range(0, len(text_list)):
        j = 0
        while j < len(text_list[i][-1]):
            word = text_list[i][-1][j]
            if word in my_feature_set:
                j += 1
            else:
                text_list[i][-1].remove(word)
        print('feature_process', i)
    return text_list

# 匹配 特征集


if __name__ == '__main__':
    stop_word_list = loadTYC() # 读取停用词集
    my_feature_set = loadFeature() # 读取特征集


    # io 预备
    # 处理 pos
    text_list = loadDocs("./结巴分词/yuliao_pos.csv")

    pos_num = len(text_list)

    text_list = mySegment(text_list) # 分词
    text_list = quTYC(text_list, stop_word_list) # 去停用词
    text_list = feature_process(text_list, my_feature_set) # 有关特征词处理

    f = codecs.open('./Lpu_Input/yuliao_pos.nlpresult', 'w', encoding='utf-8')
    for doc in text_list:
        if doc[-1] != []:
            for i in range(0, len(doc) - 1):
                f.write(doc[i] + '|')
            f.write( ' '.join(doc[-1]) + '\n' )
    f.close()

    print('pos Done')
    # 处理 pos


    # 处理 unlabel
    text_list = loadDocs("./结巴分词/yuliao_unlabel.csv")

    unlabel_num = len(text_list)

    text_list = mySegment(text_list) # 分词
    text_list = quTYC(text_list, stop_word_list) # 去停用词
    text_list = feature_process(text_list, my_feature_set) # 有关特征词处理

    f = codecs.open('./Lpu_Input/yuliao_unlabel.nlpresult', 'w', encoding='utf-8')
    for doc in text_list:
        if doc[-1] != []:
            for i in range(0, len(doc) - 1):
                f.write(doc[i] + '|')
            f.write( ' '.join(doc[-1]) + '\n' )
    f.close()

    print('unlabel Done')
    # 处理 unlabel

    
    # 处理 test
    text_list = loadDocs("./结巴分词/yuliao_test.csv")

    test_num = len(text_list)

    text_list = mySegment(text_list) # 分词
    text_list = quTYC(text_list, stop_word_list) # 去停用词
    text_list = feature_process(text_list, my_feature_set) # 有关特征词处理

    f = open('./Lpu_Input/yuliao_test.nlpresult', 'w', encoding='utf-8')
    for doc in text_list:
        if doc[-1] != []:
            for i in range(0, len(doc) - 1):
                f.write(doc[i] + '|')
            f.write( ' '.join(doc[-1]) + '\n' )
    f.close()

    print('test Done')
    # 处理 test
    # io 预备
    
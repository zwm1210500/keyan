import jieba
import jieba.posseg as pseg
import os
import sys
import numpy as np
import math
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

pos_num = 0
unlabel_num = 0

# word = set() # 特征集


# 小函数
def cal_len(vec):
    vec = np.mat(vec)
    num = (float)(vec * vec.T)
    return math.sqrt(num)

def norm(vec):
    vec = np.mat(vec)
    return vec / cal_len(vec)
# 小函数

# io 预备
# 读取 pos
f1 = open("./结巴分词/yuliao_pos.csv", 'r', encoding = "utf-8")
content = f1.read()
f1.close()
text_list = content.split('\n')

text_list.remove(text_list[-1])
for i in range(0, len(text_list)):
    text_list[i] = str(text_list[i]).strip()

pos_num = len(text_list)
# 读取 pos

# 读取 unlabel
f2 = open("./结巴分词/yuliao_unlabel.csv", 'r', encoding = "utf-8")
content = f2.read()
f2.close()
temp = content.split('\n')

temp.remove(temp[-1])
for i in range(0, len(temp)):
    temp[i] = str(temp[i]).strip()

unlabel_num = len(temp)
# 读取 unlabel

# pos, unlabel 合并一起
text_list.extend(temp)
print('pos: ' + str(pos_num) + ', unlabel: ' + str(unlabel_num))
# pos, unlabel 合并一起
# io 预备


# 分词
jieba.add_word('不喜欢')
jieba.add_word('耗油')
jieba.add_word('不合格')

for i in range(0, len(text_list)):
    text_list[i] = text_list[i].split('|')
    seg_list = jieba.cut( text_list[i][-1] )
    text_list[i] = list(seg_list)

# for i in range(0, len(text_list)):
#     print('#' + str(i) + '\t' + text_list[i])
# 分词


# 去停用词 # 并收集词库，用作特征集(目前这后一步不做了)
# 读取停用词
f = open('./结巴分词/stop_word_UTF_8.txt', 'r', encoding='utf-8')
content = f.read()
f.close()
stop_word_list = content.split('\n')
stop_word_list.remove( stop_word_list[-1] )

# for i in range(0, len(stop_word_list)):
#     print('#' + str(i) + '\t' + stop_word_list[i])
# 读取停用词

f = open('./jieba_segment.txt', 'w', encoding='utf-8')

for i in range(0, len(text_list)):
    mlist = []
    for a in text_list[i]:
        if a in stop_word_list:
            continue
        else:
            mlist.append(a)
            # word.add(a)
    text_list[i] = mlist
    f.write(' '.join(text_list[i]) + '\n')

f.close()

# for i in range(0, len(text_list)):
#     print('#' + str(i) + '\t' + ' '.join(text_list[i]))
# 去停用词 # 并收集词库，用作特征集(目前这后一步不做了)

'''
# test tfidf
f = open('./word_set.txt', 'w', encoding='utf-8')
word_num = len(word)
word_id = {}
id_word = {}
i = 0
for w in word:
    word_id[w] = i
    id_word[i] = w
    f.write(str(w) + ' ' + str(i) + '\n')
    i += 1
f.close()

# 词频矩阵(tf)
tf_arr = []
for i in range(0, len(text_list)):
    tf_arr.append([0] * word_num)
    cnt = 0
    for w in text_list[i]:
        tf_arr[i][ int(word_id[w]) ] += 1
        cnt += 1
    if cnt != 0: # 0 ???
        for j in range(0, len(tf_arr[i])):
            tf_arr[i][j] /= cnt
# 词频矩阵(tf)

D_num = len(text_list)
for i in range(0, len(text_list)):
    for j in range(0, len(text_list[i])):
        if tf_arr[i][j] != 0:
            cnt = 0
            for a in text_list:
                if text_list[i][j] in a:
                    cnt += 1
            temp = math.log( D_num / cnt) + 1
            tf_arr[i][j] *= temp

for i in range(0, len(tf_arr)):
    tf_arr[i] = np.array(norm(tf_arr[i]))
    tf_arr[i] = tf_arr[i].tolist()
    
weight = tf_arr

print('\nweight')
for a in weight:
    print(a)
print('weight\n')


# f = open('./testtfidf.txt', 'w', encoding='utf-8')
# for a in weight:
#     mstr = ''
#     for b in a:
#         mstr += str(b) + ' '
#     # print(mstr)
#     f.write(mstr.strip() + '\n')
# f.close()

f = open("./testtfidf.txt", 'w', encoding = "utf-8")
for i in range(0, len(weight)): #打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    out_str = ''
    for j in range(0, len(weight[i])):
        out_str += str(id_word[j]) + ':' + str(weight[i][j]) + ' '
    f.write(out_str.strip() + '\n')
f.close()
# test tfidf
'''


# 计算 tfidf
for i in range(0, len(text_list)):
    text_list[i] = (' '.join(text_list[i])).strip()

corpus = text_list
vectorizer = CountVectorizer() # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
transformer = TfidfTransformer() # 该类会统计每个词语的tf-idf权值
tfidf = transformer.fit_transform( vectorizer.fit_transform(corpus) ) # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
word_set = vectorizer.get_feature_names() # 获取词袋模型中的所有词语
weight = tfidf.toarray() # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

print(tfidf)

print('\nweight')
for a in weight:
    print(a)
print('weight\n')

f = open('./word_set_1.txt', 'w', encoding='utf-8')
for i in range(0, len(word_set)):
    f.write(str(word_set[i]) + ' ' + str(i) + '\n')
f.close()


f = open("./tfidf_result.txt", 'w', encoding = "utf-8")
for i in range(len(weight)): #打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    out_str = ''
    for j in range(len(word_set)):
        out_str += str(word_set[j]) + ':' + str(weight[i][j]) + ' '
    f.write(out_str.strip() + '\n')
    # print(out_str)
f.close()
print('tfidf 结束')
print( 'total feature ' + str(len(word_set)) )

# for a in weight:
#     mstr = ''
#     for b in a:
#         mstr += str(b) + ' '
#     print(mstr)
# 计算 tfidf



# 计算 中心向量
def getCenter(p_vector, u_vector):
    Alpha = 16
    Beta = 4

    p_vector = np.mat(p_vector)
    p_sum = p_vector.sum( axis=0 )
    u_vector = np.mat(u_vector)
    u_sum = u_vector.sum( axis=0 )

    p_center = Alpha * p_sum / pos_num - Beta * u_sum / unlabel_num
    u_center = Alpha * u_sum / unlabel_num - Beta * p_sum / pos_num

    return p_center, u_center

p_vector = weight[0:pos_num]
u_vector = weight[pos_num:]

p_center, u_center = getCenter(p_vector, u_vector)    

# print('p_center:\n', p_center)
# print('u_center:\n', u_center)

# print(p_center)
# print(u_center)
# 计算 中心向量


# 找 可靠负例
# 余弦距离
def cos_sim(v1, v2):
    v1 = np.mat(v1)
    v2 = np.mat(v2)
    num = (float)(v1 * v2.T)
    return num / (cal_len(v1) * cal_len(v2))
# 余弦距离

# print('\nu_vector')
# for a in u_vector:
#     print(a)
# print('u_vector\n')


RN_id = []
RN_vector = []
i = 1
for d in u_vector:
    if cos_sim(d, p_center) <= cos_sim(d, u_center):
        RN_id.append(i)
        RN_vector.append(d)
    i += 1

print(RN_id)
# print(RN_vector)

print('total ' + str(len(RN_id)))

# 找 可靠负例

print('First Done')


# 聚类，重新找负例
RN_vector = np.array(RN_vector)
# print(RN_vector)
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(RN_vector)
labels = kmeans.labels_.tolist()
print('kmeans labels:', labels)

# N_id = [[] for i in range(0, n_clusters)]
N = [[] for i in range(0, n_clusters)]
# N = []
# for i in range(0, n_clusters):
#     N.append([])

RN_vector = RN_vector.tolist()
for i in range(0, len(labels)):
    # N_id[labels[i]].append(i)
    N[labels[i]].append(RN_vector[i])

# for i in range(0, len(N)):
#     for j in range(0, len(N[i])):
#         print(i, ', ', j, N_id[i][j])
        # print(i, ', ', j, N[i][j])

# p_vector 单位化
p_vector = p_vector.tolist()
for i in range(0, len(p_vector)):
    p_vector[i] = norm(p_vector[i])
p_vector = np.mat(p_vector)
# p_vector 单位化

# 计算各组的中心向量
p_center = [[] for i in range(0, n_clusters)]
u_center = [[] for i in range(0, n_clusters)]
for i in range(0, n_clusters):
    p_center[i], u_center[i] = getCenter(p_vector, N[i])
# 计算各组的中心向量

RN_vector_pre = RN_vector
RN_id = []
RN_vector = []

# print('\ntest')
# print('RN_vector_pre[0]:')
# print(RN_vector_pre)
# print('\n')
# print(p_center)
# # for a in p_center:
# #     print(a)
# print('test\n')

# 计算余弦距离，重新确定可靠负例
for i in range(0, len(RN_vector_pre)):
    d = RN_vector_pre[i]
    # 找到距离当前文档最近的正例中心向量
    temp_dist = []
    for j in range(0, len(p_center)):
        temp_dist.append(cos_sim(d, p_center[j]))

    # print('#' + str(i))
    # print(temp_dist, '\n')

    p_d_dist = max(temp_dist)
    # 找到距离当前文档最近的正例中心向量
    for j in range(0, len(u_center)):
        if p_d_dist <= cos_sim(d, u_center[j]):
            RN_id.append(i)
            RN_vector.append(d)
            break
# 计算余弦距离，重新确定可靠负例

print('Here is them: ')
for i in range(0, len(RN_id)):
    print('id: ' + str(i))
    # print(RN_vector[i], '\n')

# 聚类，重新找负例

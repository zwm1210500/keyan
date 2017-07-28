import os
import codecs
import jieba
import numpy as np
import math
from sklearn.cluster import KMeans

NEW_LINE = '\r\n'

words = 0
size = 0

def cal_len(vec):
    vec = np.mat(vec)
    num = (float)(vec * vec.T)
    return math.sqrt(num)

def norm(vec):
    vec = np.mat(vec)
    return vec / cal_len(vec)

def cos_sim(v1, v2):
    v1 = np.mat(v1)
    v2 = np.mat(v2)
    num = (float)(v1 * v2.T)
    return num

def getCenter(p_vector, u_vector):
    global pos_num, unlabel_num
    Alpha = 16
    Beta = 4

    p_vector = np.mat(p_vector)
    p_sum = p_vector.sum( axis=0 )
    u_vector = np.mat(u_vector)
    u_sum = u_vector.sum( axis=0 )

    p_center = Alpha * p_sum / pos_num - Beta * u_sum / unlabel_num
    u_center = Alpha * u_sum / unlabel_num - Beta * p_sum / pos_num

    p_center = norm(p_center)
    u_center = norm(u_center)
    return p_center, u_center

def loadVector(filePath):
    global words, size
    fr = codecs.open(filePath, 'r', 'utf-8')
    content = fr.read()
    fr.close()
    text_list = content.split(NEW_LINE)
    temp = text_list[0].split(' ')
    words = int(temp[0])
    size = int(temp[1])
    text_list.remove(text_list[0])
    text_list.remove(text_list[-1])
    word2vec = {}
    i = 0
    for text in text_list:
        parts = text.split(' ')
        word = parts[0]
        while parts[-1] == '':
            parts.remove(parts[-1])
            parts.remove(parts[0])
        for j in range(0, len(parts)):
            parts[j] = float(parts[j])
        word2vec[word] = norm( np.mat(parts) )
        print('load vector', i)
        i += 1
    return word2vec


def loadDoc(filePath, encoding='utf-8'):
    fr = codecs.open(filePath, 'r', encoding)
    content = fr.read()
    fr.close()
    text_list = content.split(NEW_LINE)
    text_list.remove(text_list[-1])
    for i in range(0, len(text_list)):
        parts = text_list[i].split('|')
        text_list[i] = parts[-1].strip().split(' ')
    return text_list

def toVector(text_list, word2vec):
    zero_vec = np.mat([0.0 for ii in range(0, size)])
    for i in range(0, len(text_list)):
        temp = word2vec.get(text_list[i][0], zero_vec)
        for j in range(1, len(text_list[i])):
            if text_list[i][j] in word2vec.keys():
                temp += word2vec[ text_list[i][j] ]
        text_list[i] = norm(temp)
    return text_list

if __name__ == '__main__':
    pos_num = 0
    unlabel_num = 0

    word2vec = loadVector('./InputFile/vectors.txt')

    pos_list = loadDoc('./InputFile/yuliao_pos.nlpresult')
    unlabel_list = loadDoc('./InputFile/yuliao_unlabel.nlpresult')
    pos_num = len(pos_list)
    unlabel_num = len(unlabel_list)

    p_vector = toVector(pos_list, word2vec)
    u_vector = toVector(unlabel_list, word2vec)
    
    # test_list = loadDoc('./InputFile/yuliao_test.nlpresult')
    # test_list = toVector(test_list, word2vec)


    # 计算 中心向量
    p_id = list( range(1, pos_num + 1) )
    u_id = list( range(1, unlabel_num + 1) )

    # i = 0
    # while i < len(p_vector):
    #     if cal_len(p_vector[i]) > 0:
    #         i += 1
    #     else:
    #         p_id.remove(p_id[i])
    #         p_vector.remove(p_vector[i])
    #         continue

    # i = 0
    # while i < len(u_vector):
    #     if cal_len(u_vector[i]) > 0:
    #         i += 1
    #     else:
    #         u_id.remove(u_id[i])
    #         u_vector.remove(u_vector[i])
    #         continue

    for i in range(0, len(p_vector)):
        p_vector[i] = (np.array(p_vector[i]).tolist())[0]
    for i in range(0, len(u_vector)):
        u_vector[i] = (np.array(u_vector[i]).tolist())[0]
    # print(p_vector)

    p_center, u_center = getCenter(p_vector, u_vector)

    # print('p_center:\n', p_center.tolist())
    # print('u_center:\n', u_center.tolist())
    # 计算 中心向量

    
    # 找 可靠负例
    RN_id = []
    RN_vector = []

    # u_vector = u_vector.tolist()
    for i in range(0, len(u_vector)):
        d = u_vector[i]
        if cos_sim(d, p_center) <= cos_sim(d, u_center):
            RN_id.append(u_id[i])
            RN_vector.append(d)

    # print(RN_id)
    # print(RN_vector)

    # print('first:', RN_id)
    print('[first]total ', len(RN_id), '/', unlabel_num)
    # 找 可靠负例



    # 聚类，重新找负例
    RN_vector = np.array(RN_vector)
    # print(RN_vector)

    n_clusters = 8
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(RN_vector)
    labels = kmeans.labels_.tolist()
    # print('kmeans labels:', labels)
    
    N = [[] for i in range(0, n_clusters)] # 为分类计算 p u 中心向量而设，不需记录 id

    RN_vector = RN_vector.tolist()
    for i in range(0, len(labels)):
        # N_id[labels[i]].append(i)
        N[labels[i]].append(RN_vector[i])

    p_center_pre = p_center
    # 计算各组的中心向量
    p_center = [[] for i in range(0, n_clusters)]
    u_center = [[] for i in range(0, n_clusters)]
    for i in range(0, n_clusters):
        p_center[i], u_center[i] = getCenter(p_vector, N[i])
    # 计算各组的中心向量

    RN_id_pre = RN_id
    RN_vector_pre = RN_vector
    RN_id = []
    RN_vector = []
    # 计算余弦距离，重新确定可靠负例
    for i in range(0, len(RN_vector_pre)):
        d = RN_vector_pre[i]
        # 找到距离当前文档最近的正例中心向量
        temp_dist = []
        for j in range(0, len(p_center)):
            temp_dist.append(cos_sim(d, p_center[j]))

        p_d_dist = max(temp_dist)
        # 找到距离当前文档最近的正例中心向量
        for u in u_center:
            u_d_dist = cos_sim(d, u)
            if p_d_dist <= u_d_dist:
                RN_id.append(RN_id_pre[i])
                RN_vector.append(d)
                break
    # 计算余弦距离，重新确定可靠负例

    print('Here is them: ', len(RN_id), '/', len(RN_id_pre), '/', unlabel_num)
    # print(RN_id)
    # for i in range(0, len(RN_id)):
    #     print('id: ' + str(i))
        # print(RN_vector[i], '\n')
    # 聚类，重新找负例
    
    # for i in range(0, len(p_vector)):
    #     p_vector[i] = (np.array(p_vector[i]).tolist())[0]
    # for i in range(0, len(RN_vector)):
    #     RN_vector[i] = (np.array(RN_vector[i]).tolist())[0]
    # print(p_vector)
    # print(RN_vector)

    # fw = codecs.open('./p_vector.txt', 'w', 'utf-8')
    # for doc in p_vector:
    #     for w in doc:
    #         fw.write(w + ' ')
    #     fw.write(NEW_LINE)
    
    
    p_center = p_center_pre
    best_d = []
    best_vector = []
    # to be continue...

    '''
    fw = codecs.open('../svm/train.txt', 'w', 'utf-8')
    a = 1
    for doc in p_vector:
        out_str = '1'
        for i in range(0, len(doc)):
            if doc[i] != 0:
                out_str += ' ' + str(i + 1) + ':' + str(doc[i])
        if out_str != '1':
            fw.write(out_str)
            fw.write(NEW_LINE)
            print('write pos', a)
            a += 1
    a = 1
    for doc in RN_vector:
        out_str = '-1'
        for i in range(0, len(doc)):
            if doc[i] != 0:
                out_str += ' ' + str(i + 1) + ':' + str(doc[i])
        if out_str != '-1':
            fw.write(out_str)
            fw.write(NEW_LINE)
            print('write neg', a)
            a += 1
    fw.close()
    '''
    
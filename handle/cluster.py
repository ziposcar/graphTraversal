#encoding:utf-8
from __future__ import division    # from __future__ imports must occur at the beginning of the file
import obtain_efsm_info2
from decimal import Decimal
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
# import savReaderWriter
import pandas as pd
from Levenshtein import *
import math

def tran_event_to_metrix():
    keys = []
    value = []
    dict = {}
    event = obtain_efsm_info2.obtain_tran_event()   # the information of transition event which store in dict
    # print event
    for k in event:
        t = k.strip("T")
        key = int(t)
        dict[key] = event[k]
    for k in dict:
        num = k -1    #将迁移名-1，方便对应编号
        keys.append(num)
        value.append(dict[k])
    # print dict
    print keys
    print value
    metrix = []
    for i in value:
        # print i
        i = i.split(";")
        if i[0] == "":
            i[0] = 0
        else:
            temp = i[0].split(",")
            i[0] = len(temp)
        tt = i[1].split("=")
        i[1] = tt[0]
        # print i
        metrix.append(i)
    print metrix   # this is metrix
    # print metrix[0][1]  # 打印矩阵metrix第一行第2列的元素
    print len(metrix)
    f = open('E:/schoolmate1.txt', 'w+')
    for i in range(len(metrix)):
         # print metrix[i]
         T = "T"+ str(i+1)
         f.write(str(T) + ",")
         for j in range(len(metrix[i])):
             # print metrix[i][j]
             t = metrix[i][j]
             f.write(str(t)+",")
         # print metrix[i]
         f.write("\n")
    f.close()
    return metrix


def findSubstrings(s1,s2):
    m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]  # 生成0矩阵，为方便后续计算，比字符串长度多了一列
    mmax = 0  # 最长匹配的长度
    p = 0  # 最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
                    p = i + 1
    return s1[p - mmax:p]  # 返回最长子串   其长度mmax


#这个公式还有在考虑，因为只要两个迁移之间输入个数不一样就为0，全为0后面怎么聚类，需要在考虑
def similarity_measure(Ti, Tj):
    # print "Ti", Ti
    # print "Tj",Tj
    if Ti[0] != Tj[0]:
        # Sij = Decimal('0.000').quantize(Decimal('0.00'))
        Sij = 0.0
    else:
        str1 = Ti[2] + Ti[1]
        str2 = Tj[2] + Tj[1]
        # 自创公式
        substring = findSubstrings(str1,str2)
        s = (2 * len(substring))/(len(str1) + len(str2))   #得到的是小数，
        Sij = s
    # print Sij
    return Sij
def similarity_metrix(metrix):  # 获得相似矩阵S
    n = len(metrix)
    similar_metrix = [None] * n
    for i in range(len(similar_metrix)):
        similar_metrix[i] = [0] * n

    for i in range(len(metrix)):
        for j in range(len(metrix)):
            Sij = similarity_measure(metrix[i],metrix[j])
            # print s
            #取高斯核函数
            # if i == j:
            #      Sij = 0.0
            # else:
            #     Sij = math.exp(-(math.pow(s,2)/(2*math.pow(0.65,2))))
            similar_metrix[i][j] = Sij
    # for i in range(len(similar_metrix)):
    #      print similar_metrix[i]
    return similar_metrix

def similarity_measure2(Ti, Tj):
    # print "Ti", Ti
    # print "Tj",Tj
    if Ti[0] != Tj[0]:
        # Sij = Decimal('0.000').quantize(Decimal('0.00'))
        Sij = 0.0
    else:
        str1 = Ti[2] + Ti[1]
        str2 = Tj[2] + Tj[1]
        # 自创公式
        # substring = findSubstrings(str1,str2)
        # s = (2 * len(substring))/(len(str1) + len(str2))   #得到的是小数，
        if str1 == str2:
            s = 1.0
        else:
            t = max(len(str1),len(str2))
            s = distance(str1,str2) / t # 得到的是整数，建立矩阵时会出错
        # print s
        Sij = s
    # print Sij
    return Sij

def similarity_metrix2(metrix):  # 获得相似矩阵S
    n = len(metrix)
    similar_metrix = [None] * n
    for i in range(len(similar_metrix)):
        similar_metrix[i] = [0] * n

    for i in range(len(metrix)):
        for j in range(len(metrix)):
            Sij = similarity_measure2(metrix[i],metrix[j])
            # print s
            #取高斯核函数
            # if i == j:
            #      Sij = 0.0
            # else:
            #     Sij = math.exp(-(math.pow(s,2)/(2*math.pow(0.65,2))))
            similar_metrix[i][j] = Sij
    # for i in range(len(similar_metrix)):
    #      print similar_metrix[i]
    return similar_metrix


def getD(S):    # 获得度矩阵
    points_num = len(S)
    D = np.diag(np.zeros(points_num))
    for i in range(points_num):
        D[i][i] = sum(S[i])
    # for k in range(len(D)):
    #     print D[k]
    return D


def getL(W,D):  # 获得拉普拉斯矩阵L
    L = D - W
    Dn = np.power(np.linalg.matrix_power(D, -1), 0.5)
    Lbar = np.dot(np.dot(Dn, L), Dn)
    return Lbar


def getEigVec(L,cluster_num):  #从拉普拉斯矩阵获得特征矩阵
    eigval,eigvec = np.linalg.eig(L)  #eigval存放特征值，行向量。eigvec存放特征向量，每一列带别一个特征向量。特征值和特征向量是一一对应的
    dim = len(eigval)
    dictEigval = dict(zip(eigval,range(0,dim)))
    kEig = np.sort(eigval)[0:cluster_num]
    ix = [dictEigval[k] for k in kEig]
    return eigval[ix],eigvec[:,ix]


def randRGB():
    return (random.randint(0, 255)/255.0,
            random.randint(0, 255)/255.0,
            random.randint(0, 255)/255.0)


def plot(matrix,C,centers,k):
    colors = []
    for i in range(k):
        colors.append(randRGB())
    for idx,value in enumerate(C):   # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中
        plt.plot(matrix[idx][0],matrix[idx][1],'^',color=colors[int(C[idx])])
    for i in range(len(centers)):
        plt.plot(centers[i][0],centers[i][1],'rx')
    plt.show()


def getCenters(data,C):  # 获得中心位置
    centers = []
    for i in range(max(C)+1):
        points_list = np.where(C==i)[0].tolist()
        centers.append(np.average(data[points_list],axis=0))
    return centers


def loaddata():
    file = "D:\pycharm\graphTraversal\dataset\schoolmate_tran4_dataset.csv"
    # data = savReaderWriter.SavReader(file)
    data = pd.read_csv(file,sep=",", encoding='utf-8')
    dataset = np.array(data)
    # print dataset
    # print len(dataset)
    return dataset


def pitruce(c):
    c = str(c)
    c = c.strip("[")
    c = c.strip("]")
    c = c.split(" ")
    # print c
    colors=[]
    index = []
    flag = []
    s = set(c)
    for i in range(len(s)):
        colors.append(randRGB())
    for idx,val in enumerate(c):
        # plt.plot(idx, val, '^', color=colors[int(c[idx])])
        # print "idx,val",idx,val
        index.append(idx +1)  #x轴值
        flag.append(val)  # y轴值
    # plt.show()

    p = zip(flag,index)
    # print p
    y = list(set(flag))
    # print len(y)
    for i in range(len(y)):
        # print "i",i
        for j in range(len(p)):
            # print "p[j][0],p[j][1]", p[j][0],p[j][1]
            if int(p[j][0]) == i:
                plt.plot( p[j][1],i, '^', color=colors[i])
    plt.xlabel(r"The serial number of the transition")

    plt.ylabel(r'Cluster mark')
    plt.grid(linestyle='--')
    plt.title('Clustering results of Transitions behavior pattern ',fontsize=15)
    plt.show()

def handle_c(c):
    c = str(c)
    c = c.strip("[")
    c = c.strip("]")
    c = c.strip("\n")
    c = c.split(" ")
    return c


def handle_xy(c):
    Tindex = []
    flag = []
    for idx,val in enumerate(c):
        # plt.plot(idx, val, '^', color=colors[int(c[idx])])
        # print "idx,val",idx,val
        Tindex.append(idx +1)  #x轴值
        flag.append(val)  # y轴值
    return flag,Tindex

def pitruce2(c,cc):
    c = handle_c(c)

    # print c
    colors=[]
    s = set(c)
    ss = set(cc)
    for i in range(len(s)):
        colors.append(randRGB())
    print "colors",colors
    flag,Tindex = handle_xy(c)
    flag1,Tindex1 = handle_xy(cc)
    p = zip(flag,Tindex)
    pp = zip(flag1,Tindex1)
    # print "p", p
    # print "pp",pp
    y = list(set(flag))
    yy = list(set(flag1))
    # print len(y)
    for i in range(len(y)):
         # print "i",i
         for j in range(len(p)):
             # print "p[j][0],p[j][1]", p[j][0],p[j][1]
             if int(p[j][0]) == i:  #p[j][0]表示p列表中第j个元素的第0个位置即=5，元素时元组如('5', 1)
                 # plt.plot( p[j][1],i, '^', color=colors[i])
                 plt.plot(p[j][1], i, 'g^')
                 plt.plot(p[j][1], i, 'bx')
    for ii in range(len(yy)):
         for jj in range(len(pp)):
             if int(pp[jj][0]) == ii:  #p[j][0]表示p列表中第j个元素的第0个位置即=5，元素时元组如('5', 1)
                 plt.plot( p[jj][1],ii, 'r.')

    p3 = plt.scatter(143, 10, marker='^', color='g')
    p4 = plt.scatter(143, 10, marker='.', color='r')
    p5 = plt.scatter(143, 10, marker='x', color='b')
    plt.xlabel(r"The serial number of the transition")
    plt.ylabel(r'Cluster mark')
    plt.grid(linestyle='--')
    plt.title('Clustering results of Transitions behavior pattern ',fontsize=15)
    plt.legend([p3, p4, p5], ['my', 'edit','manual'], loc='best', scatterpoints=1)
    plt.show()

def cf(s):
    s = handle_c(s)
    c =[]
    for kk in range(len(s)):
        if s[kk]!="":
            c.append(s[kk])
    # print c
    result = []
    temp = []
    s = set(c)
    for k in range(len(s)):
        for j in range(len(c)):
            if int(c[j]) == k:
                temp.append(j)
        result.append(temp)
        temp = []
    # print result
    dict = {}
    dict1 = {}
    for ii in range(len(result)):
        dict[ii] = len(result[ii])
        dict1[ii] = result[ii]
    list=sorted(dict.items(), key=lambda dict: dict[1])
    return list,dict1

def handle_c_flag(c1,c2):
    list1,dict1=cf(c1)
    list2,dict2 = cf(c2)
    index = []
    m ={}
    for i in range(len(list1)):
        index.append(list1[i][0])
    for j in range(len(list2)):
        t = index[j]
        d = list2[j][0]
        m[t] = dict2[d]
    print list1
    print list2
    print"dict1", dict1
    print "dict2",dict2
    print "m",m
    newc = []
    for i in range(len(c1)):
        for key in m:
            temp = m[key]
            for j in range(len(temp)):
                if temp[j] == i:
                    newc.append(key)
    print "newc", newc
    return newc


def mian_Ldistance():
    dataset = loaddata()
    metrix = tran_event_to_metrix()
    cluster_num = 6    #这个值确定很重要
    s = similarity_metrix2(metrix)
    d = getD(s)
    L = getL(s,d)
    eigval, eigvec = getEigVec(L, cluster_num)
    # print eigval,eigvec
    clf = KMeans(n_clusters=cluster_num)
    s = clf.fit(eigvec)
    C = s.labels_  #聚类结果
    print C,len(C)
    return C


def mian_substing():
    dataset = loaddata()
    metrix = tran_event_to_metrix()
    cluster_num = 6    #这个值确定很重要
    s = similarity_metrix(metrix)
    d = getD(s)
    L = getL(s,d)
    eigval, eigvec = getEigVec(L, cluster_num)
    # print eigval,eigvec
    clf = KMeans(n_clusters=cluster_num)
    s = clf.fit(eigvec)
    C = s.labels_  #聚类结果
    # print C,len(C)
    return C

def tongji(c1):
    c = str(c1)
    c = c.strip("[")
    c = c.strip("]")
    c = c.strip("\n")
    c = c.split(" ")
    # cc = []
    # for i in c :
    #     cc.append(int(i))
    # print cc
    # index = []
    # for i in range(len(cc)):
    #     if cc[i] != c2[i]:
    #         index.append(i)
    # print index
    print c,len(c)
    f = open("D:\\pycharm\\graphTraversal\\dataset\\cluster_FAQ_our.txt", "a")
    for line in c:
        f.write(line + '\n')
    f.close()
    return c

def main(c1,c2):
    # newc = handle_c_flag(c1,c2)
    # pitruce2(c1,newc)
    pitruce2(c1,c2)


if __name__ == '__main__':
    # c1 = mian_substing()
    # print"c1", c1
    c2 = mian_Ldistance()
    print "c2", c2
    c11 ="4 4 4 0 8 0 0 5 5 0 0 1 5 5 0 1 0 1 0 0 6 6 0 1 0 6 6 0 1 0 1 0 0 7 7 0 1\
 0 7 2 0 1 0 1 0 0 0 0 3 3 0 1 0 3 3 1 3 0 1 0 1 0 0 5 5 0 1 0 5 5 0 1 0 1\
 0 0 3 3 0 1 0 3 3 0 1 0 1 0 0 3 3 0 1 0 3 3 0 1 0 1 0 0 4 4 0 1 0 4 4 0 1\
 0 1 0 4 4 4 0 1 0 1 0 5 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    # c1 =tongji(c1)
    c22="4 4 4 0 0 0 0 5 5 0 0 1 5 5 0 1 0 1 0 0 6 6 0 1 0 8 8 0 1 0 1 0 0 7 7 0 1\
 0 7 2 0 1 0 1 0 0 0 0 3 3 0 1 0 3 3 1 3 0 1 0 1 0 0 5 5 0 1 0 5 5 0 1 0 1\
 0 0 3 3 0 1 0 3 3 0 1 0 1 0 0 3 3 0 1 0 3 3 0 1 0 1 0 0 4 4 0 1 0 4 4 0 1\
 0 1 0 4 4 4 0 1 0 1 0 5 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    # c2=[4, 4, 4, 0, 6, 0, 0, 5, 5, 0, 0, 2, 5, 5, 0, 2, 0, 2, 0, 0, 7, 7, 0, 2, 0, 8, 8, 0, 2, 0, 2, 0, 0, 6, 6, 0, 2, 0, 6, 1, 0, 2, 0, 2, 0, 0, 0, 0, 3, 3, 0, 2, 0, 3, 3, 0, 3, 0, 2, 0, 2, 0, 0, 5, 5, 0, 2, 0, 5, 5, 0, 2, 0, 2, 0, 0, 3, 3, 0, 2, 0, 3, 3, 0, 2, 0, 2, 0, 0, 3, 3, 0, 2, 0, 3, 3, 0, 2, 0, 2, 0, 0, 4, 4, 0, 2, 0, 4, 4, 0, 2, 0, 2, 0, 4, 4, 4, 0, 2, 0, 2, 0, 5, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    c2 = tongji(c2)
    # main(c1,c2)
    # tran_event_to_metrix()




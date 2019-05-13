#encoding:utf-8
# 初始化种群，在模型上生成序列，可行性判断后，在生成数据
import sys
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../DUfile")

import random
from random import choice
from collections import Counter
import obtain_efsm_info2


def handle_def_use_file():
    list2 = []
    list = []
    modelfiledir = '../DUfile/'
    modelfile = "def_use_user2.txt"
    inputfile = modelfiledir + modelfile
    for line in open(inputfile):
        line = line.strip('\n')
        list2.append(line)
    print 'list2', list2
    return list2
    '''for v in list2:取定位点值
        # print v
        s = v.split(',')
        print"s的值", s
        for i in s:
            print"s中i的值", i'''

def validpath_matrix():  # 将efsm迁移关系存储在矩阵中 经过调试，发现存储成功！
    traninfolist = obtain_efsm_info2.obtain_tran_info()
    matrix = []
    for line in range(len(traninfolist)):
        temp = []
        for row in range(len(traninfolist)):
            if traninfolist[line].tgt.name == traninfolist[row].src.name:
                temp.append(1)
            else:
                temp.append(0)
        matrix.append(temp)

    return matrix
    # print matrix


def get_endtran_from_matrix():  # 行全0的为end transition,针对有结束结点的模型
    m = validpath_matrix()
    endtran = []
    for i in range(len(m)):
        if 1 not in m[i]:
            endtran.append(i)  # +1为了直观看出迁移ID
    return endtran


def get_startran_from_matrix():  # 列全0的为start transition 针对有开始结点的模型
    m = validpath_matrix()
    startran = []
    l = map(list, zip(*m))  # 转置矩阵
    # print l
    # print len(l)
    for k in range(len(l)):
        if 1 not in l[k]:
            startran.append(k)  # +1为了直观看出迁移ID
    return startran  # 这里startan的值为空，导致后面数组越界。


def digui(aa):
    aaa = int(aa)
    a = aaa - 1 #def位置要-1，与矩阵对应，矩阵是从0开始计数，矩阵中的0迁移对应的是我们的迁移1
    path = []
    path_new = []
    startlist = get_startran_from_matrix()
    m = validpath_matrix()
    path.append(a)

    while 1:
        v = []
        for i in range(len(m)):
            if (m[i][a] == 1):
                v.append(i)
        while 1:
            # randnum = random.randint(0, len(m) - 1)
            if (len(v)> 0):
                randnum = choice(v)
                path.append(randnum)
                break
        a = randnum
        if a in startlist:
            break
    path.reverse() # 路径翻转顺序，因为我们是逆推产生路径
    for index in range(len(path)):
        tran = 'T' + str(path[index] + 1)
        path_new.append(tran)
    return path_new


def handle_digui(aa):
    while 1:
        p = digui(aa)
        timeslist = Counter(p).values()  # 每个重复出现的迁移的出现次数
        maxtimes = max(timeslist)
        if len(p) < 12 and len(p) > 2 and maxtimes < 3:  # 这里的限定需要再做考虑！！
            break
    return p


def digui2(bb,aa):
    aaa = int(aa)
    a = aaa - 1
    bbb = int(bb)
    b = bbb - 1 #def位置要-1，与矩阵对应，矩阵是从0开始计数，矩阵中的0迁移对应的是我们的迁移1
    path = []
    path_new = []
    m = validpath_matrix()
    path.append(b)
    v = []
    while 1:
        for i in range(len(m)):
            if (m[i][b] == 1):
                v.append(i)
        while 1:
            # randnum = random.randint(0, len(m) - 1)
            # print"m[i]长度", len(m)
            # if (m[randnum][b] == 1):
            #     path.append(randnum)
            #     break
            if (len(v)> 0):
                randnum = choice(v)
                path.append(randnum)
                break
        b = randnum
        if b == a:
            break
    path.reverse() # 路径翻转顺序，因为我们是逆推产生路径
    for index in range(len(path)):
        tran = 'T' + str(path[index] + 1)
        path_new.append(tran)
    return path_new


def handle_digui2(bb,aa):
    while 1:
        p = digui2(bb,aa)
        timeslist = Counter(p).values()  # 每个重复出现的迁移的出现次数
        maxtimes = max(timeslist)
        if len(p) < 12 and len(p) > 2 and maxtimes < 3:  # 这里的限定需要再做考虑！！
            break
    return p


def generate_path():
    path = []
    total = []
    local = handle_def_use_file()
    print"所有的定义使用对", local
    cou=0
    for v in local: # 取定位点值
        cou=cou+1
        s = v.split(',')
        apoint = s[0]
        bpoint = s[1]
        # print "def",apoint
        # print "use", bpoint
        # path = digui(apoint)
        # path2 = digui2(bpoint, apoint)
        print "第",cou,"对定义使用对",v
        path = handle_digui(apoint)
        # path = digui(apoint)

        print "第",cou,"个def", path
        path2 = handle_digui2(bpoint, apoint)
        # path2 = digui2(bpoint, apoint)
        print"第",cou,"个use", path2

        path3 = path2[1:]  # 截取path2的元素，不取第一个元素，因为拼接时已有一个拼接点
        path.extend(path3) # 凭借两个列表
        print"序列为", path
        total.append(path)
    fileObject = open('../seq_result/data.txt', 'a')
    for seq in total:
        fileObject.write(str(seq))  # 要做str转换，不然会报TypeError错误
        fileObject.write('\n')
    fileObject.close()
    print"total:\n", total
    return total


def chromsome():  # 个体=a path，对path的长度、重复迁移个数进行限制
    while 1:
        p = generate_path()
        timeslist = Counter(p).values()  # 每个重复出现的迁移的出现次数
        maxtimes = max(timeslist)
        if len(p) < 17 and len(p) > 2 and maxtimes < 3:  # 这里的限定需要再做考虑！！
            break
    return p


def initialpop_feasible(popsize):  # 初始化种群，使得种群中全部path 潜在可行
    pop = []
    for k in range(popsize):
        while 1:
            path = chromsome()
            if is_feasible(path) == True and (path not in pop):
                pop.append(path)
                break
    return pop


def is_feasible(currpath):  # 可行性判断
    conflictTran = {}
    # conflictTran["T5"] = ["T11", "T16", "T20", "T22"]
    # conflictTran["T6"] = ["T12", "T15", "T19", "T21"]
    conflictTran["T3"] = ["T4"]
    tempPath = currpath[:]
    while tempPath:
        firstTran = tempPath[0]
        restTranList = tempPath[1:]
        if firstTran in conflictTran.keys():
            for tran in restTranList:
                if tran in conflictTran[firstTran]:
                    return False
        tempPath = restTranList
    return True


if __name__ == '__main__':  # not execute when import as a module
    # print is_feasible(test)
    # print random_subpath_length('T5')
    # print chromsome()
    # print get_endtran_from_matrix()
    # print get_startran_from_matrix()
    # print random_path()validpath_matrix()
    # handle_def_use_file()
    # print initialpop_feasible(5)
    print generate_path()
    # aa = 7
    # lookpath(aa)














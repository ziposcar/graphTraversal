#encoding: utf-8
from __future__ import division
import sys
import copy
import random
from random import choice
from collections import Counter
import obtain_efsm_info2
import execute
import sensitive_path_info
import recordFun
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../DUfile")

# elitist_seq = {}  # 放当代种群中被选为精英的个体序列
# elitist_data = {}  # 放当代种群中被选为精英的个体数据
# elitist_path = {}  #精英个体集合所覆盖的敏感路径，该集合由当代种群中被选为精英的个体构成
# elitist_M = {} #精英个体对应的M
elitist_seq = []  # 放当代种群中被选为精英的个体序列
elitist_data = [] # 放当代种群中被选为精英的个体数据
elitist_path = []  #精英集合所覆盖的敏感路径
elitist_M = [] #精英个体对应的M
e_fitness_list = []  # 放当代种群中被选为精英的个体适应度值
# ##################### the part is about deal with EFSM modoule ##############################
def validpath_matrix(SM):   # 将efsm迁移关系存储在矩阵中 经过调试，发现存储成功！
    traninfolist = SM.transitionList
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


def get_endtran_from_matrix(m):  # 行全0的为end transition,针对有结束结点的模型
    endtran = []
    for i in range(len(m)):
        if 1 not in m[i]:
            endtran.append(i)  # +1为了直观看出迁移ID
    return endtran


def get_endstran_for_efsm(SM):  #从模型角度，取得终止迁移
    m = validpath_matrix(SM)
    path = get_endtran_from_matrix(m)
    end_new = []
    for index in range(len(path)):
        tran = 'T' + str(path[index] + 1)
        end_new.append(tran)
    return end_new

def get_startran_from_matrix(m):  # 列全0的为start transition 针对有开始结点的模型
    startran = []
    l = map(list, zip(*m))  # 转置矩阵
    for k in range(len(l)):
        if 1 not in l[k]:
            startran.append(k)  # +1为了直观看出迁移ID
    return startran  # 这里startan的值为空，导致后面数组越界。


def get_startran_for_efsm(SM):  #从模型角度，取得开始迁移
    m = validpath_matrix(SM)
    path = get_startran_from_matrix(m)
    end_new = []
    for index in range(len(path)):
        tran = 'T' + str(path[index] + 1)
        end_new.append(tran)
    return end_new


###################### the part is about deal with seq's feasible ##############################
# 可行性判断，生成一条序列就判断，采用数据流冲突判断
def is_feasible(currpath):  # 可行性判断
    conflictTran = {}
    # conflictTran["T5"] = ["T11", "T16", "T20", "T22"]
    # conflictTran["T6"] = ["T12", "T15", "T19", "T21"]
    conflictTran["T3"] = ["T6","T23"] #webchess
    # conflictTran["T3"] = [1]
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
    #schoolmate
    # if "T24" in currpath:
    #     return False
    # else:
    #     return True


def del_infeasible_after_mutant(pop):
    newpop=[]
    for i in range(len(pop)):
        if is_feasible(pop[i]) == True:
            newpop.append(pop[i])
    return newpop


def is_feasible_list(pop):
    list=[]
    for i in range(len(pop)):
        list.append(is_feasible(pop[i]))
    return list


def delete_repeat_chrom(pop):
    temp = []
    for i in pop:
        if not i in temp:
            temp.append(i)
    return temp


###################### the part is about initialize pop   #####################################3
def random_path(SM):  # 从关系矩阵中随机得到一条efsm有效序列
    path = []
    path_new = []
    m = validpath_matrix(SM)
    # for j in m:
    #     print j
    startlist = get_startran_from_matrix(m)   #faqforg用这个产生不了开始迁移列表
    # startlist = SM.startTransitionList  #得到的是元素为string的list，要int型的
    if len(startlist) == 0:  # 对startlist的取值结果做处理，否则会因为startlist的值为空而出现数组越界的错误
        i = random.choice([0, 2, 3])  # 模型中开始迁移T1，T3，T4，在矩阵中行号表示为0，2,3
        path.append(i)
    else:
        i = choice(startlist)
        path.append(i)
    endlist = get_endtran_from_matrix(m)
    while 1:
        while 1:
            randnum = random.randint(0, len(m[i]) - 1)
            if (m[i][randnum] == 1):
                path.append(randnum)
                break
        i = randnum  # 有可能会出现死循环，一直在某个迁移中不出来,所以死循环时路径长度为5时就出来
        # timeslist = Counter(path).values()  # 每个重复出现的迁移的出现次数不超过1，
        # maxtimes = max(timeslist)
        # if i in endlist or len(path) == 14 or maxtimes > 1:   # 路径长度小于等于14，14的制定跟迁移数有关
        # if i in endlist or len(path) == 14:
        if i in endlist  :
            break
    for index in range(len(path)):
        tran = 'T' + str(path[index] + 1)
        path_new.append(tran)
    return path_new


def chromsome(SM):  # 个体=a path，对path的长度、重复迁移个数进行限制
    # object_t = object_T()
    # flag = 0
    while 1:
        p = random_path(SM)
        # for k in object_t:
        #     if k in p:
        #         flag += 1
        # if flag >0:
        #     break
        timeslist = Counter(p).values()  # 每个重复出现的迁移的出现次数
        maxtimes = max(timeslist)
        if len(p) < 17 and len(p) > 2 and maxtimes < 3 and "T22" not in p and "T33"not in p and "T38" not in p and "T37" not in p:  #phpcss
        # if len(p) < 17 and len(p) > 2 and maxtimes < 3 and "T11" not in p:  #addressbook
        # if len(p) < 17 and len(p) > 2 and maxtimes < 3 and "T25" not in p:   #teacher
        # if len(p) < 17 and len(p) > 2 and maxtimes < 3 : # 这里的限定需要再做考虑！！schoolmate（2-17）
        # if len(p) < 17 and len(p) > 2 and maxtimes < 3 and "T9" not in p:  # 这里的限定需要再做考虑！！
           #T9是为faqfore限定的
            break
    return p


def initialpop_feasible(popsize,SM):  # 初始化种群，使得种群中全部path 潜在可行
    print " 初始化种群"
    pop = []
    for k in range(popsize):
        while 1:  # 初始化种群这里出现问题，容易找不到符合要求的序列而陷入死循环
            path = chromsome(SM)
            if is_feasible(path) == True and (path not in pop):
                pop.append(path)
                break
    return pop


###################### the part is about fitness calculate   #####################################3
# 基于搜索的测试序列生成，一个种群生成覆盖多个目标迁移的序列集，以目标序列集覆盖个数为fitness，指导产生种群序列
# 可行性判断，生成一条序列就判断，采用数据流冲突判断,个体fitness制定
def object_T():   #  敏感路径对应的迁移
    modelfiledir = '../DUfile/'
    modelfile = "object_transition.txt"
    inputfile = modelfiledir + modelfile
    text = open(inputfile)
    object = text.read()
    text.close()
    object = object.split(",")
    # print object
    return object


def pop_coverage(pop,object):
    print " 计算种群覆盖的目标迁移数，如果全部覆盖则种群已满足停止条件"
    total_covT = []
    had_covT = []
    not_covT = []
    for seq in pop:
        for T in seq:
            if T not in total_covT:
                total_covT.append(T)
    for i in object:
        if i in total_covT:
            had_covT.append(i)
        else:
             not_covT.append(i)
    print " 目标迁移集：",object
    print " 已覆盖的目标迁移：",had_covT
    print " 未覆盖的目标迁移：",not_covT
    return had_covT


def covfitness(path):   #计算个体(path)的覆盖的目标迁移个数
    cover_tran=len(set(path))
    '''cover_tran = 0
    object = object_T()
    for i in object:
        if i in path:
            cover_tran = cover_tran + 1'''
    return cover_tran


def pop_fitlist_cov(pop):  #种群中全部个体的coverage的list
    fitlist=[]
    for i in range(len(pop)):
        fitlist.append(covfitness(pop[i]))
    return fitlist
####################################  selection  ###############################################


def cumcomfit(fitlist):   #将种群中每个fitness标准化，得到累积fitness列表，为 轮盘赌 做准备
    print " 个体覆盖的目标迁移数", fitlist
    norfitlist=[]
    sumfitness = 0
    for i in range(len(fitlist)):
        sumfitness = sumfitness + fitlist[i]  #种群中全部个体的fitness之和
    if sumfitness == 0:
        sumfitness = sumfitness + 1  # 消0，防止分母为0，
    for i in range(len(fitlist)):
        norfitlist.append(fitlist[i]/sumfitness)
    cumfitlist = []
    for i in range(len( norfitlist)):
        t = 0
        j = 0
        while (j <= i):
            t +=  norfitlist[j]
            j = j + 1
        cumfitlist.append(t)
    return cumfitlist

def fitprocess_before_RS(pop):     #将 种群的 fitness计算和累积fitness合并到一个函数，在 轮盘赌 中调用
    fit_list = pop_fitlist_cov(pop)  # 以 coverage
    #print fit_list   #for test
    cumfit_list=cumcomfit(fit_list)
    return cumfit_list

def fit_handl(list_global_fitness):
    #个体对所有路径的覆盖加和作为一个个体的fit
    fit_list = list_global_fitness
    # print " 选择部分，table为",table
    # for i in range(len(table)):
    #     f = sum(table[i])
    #     fit_list.append(f)
    #每个个体fit标准化
    norfitlist = []
    sumfitness = 0
    for i in range(len(fit_list)):
        sumfitness = sumfitness + fit_list[i]  # 种群中全部个体的fitness之和
    if sumfitness == 0:
        sumfitness = sumfitness + 1  # 消0，防止分母为0，
    for i in range(len(fit_list)):
        norfitlist.append(fit_list[i] / sumfitness)
    cumfitlist = []
    for i in range(len(norfitlist)):
        t = 0
        j = 0
        while (j <= i):
            t += norfitlist[j]
            j = j + 1
        cumfitlist.append(t)   #标准化结果
    return cumfitlist

def selection(pop,list_global_fitness):
    print " 开始选择操作"
    selectedchrolist = []
    templist = fit_handl(list_global_fitness)
    print " 所有个体fitness列表", len(templist),templist                  #for test
    for i in range(len(pop)):  # 若种群大小为M，则用随机数选择M次，将这些父母按被选择的顺序存入selectedchro列表中，父母会重复被选择
        randnum = random.uniform(0, 1)
        # print randnum                  #for test
        for j in range(len(pop)):
            if randnum <= templist[j]:
                selectedchrolist.append(pop[j])
                break

    # print '选择后的种群：',selectedchrolist
    print " 选择操作结束"
    return selectedchrolist

####################################  crossover  ###############################################
def crossover(selectedchrolist,pc,SM):
    crossedchrolist = []
    print " 开始交叉操作"
    for i in range(0,len(selectedchrolist),2):    #每两个个体作为一对父母
        momchro=selectedchrolist[i]
        dadchro=selectedchrolist[i+1]
        randnum=random.uniform(0,1)       #随机数决定是否执行交叉
        if randnum <= pc:
            # 得到全部transition信息
            traninforlist = SM.transitionList
            for num in range(5):  #最多重选5次，如果仍找不到可交叉的子path，则不进行交叉
                crosstran = choice(momchro)  # 在mom path 中随机选择一个 交叉transition
                tran_index = momchro.index(crosstran)  # 获得该transition的位置

                temp1=momchro[0:tran_index] #将mom拆分成两部分
                temp2=momchro[tran_index:]

                samesrc_tranlist=[]   #存放crosstran的兄弟迁移
                for item in traninforlist:
                    if item.name == crosstran:
                        src_state=item.src.name
                        for i in traninforlist:
                            if i.src.name == src_state:
                                samesrc_tranlist.append(i.name)
                        break
                intersectionlist=list(set(samesrc_tranlist).intersection(set(dadchro))) #dad path与兄弟迁移的交集
                if len(intersectionlist) != 0:
                    crosstran_indad=choice(intersectionlist)
                    index_indad=dadchro.index(crosstran_indad)  #若该tran在dad中是重复出现的，只能每次选靠前的那一个作为交叉点
                    temp3=dadchro[0:index_indad]
                    temp4=dadchro[index_indad:]

                    newpath1=temp1+temp4   # 得到交叉后的两个path
                    newpath2=temp3+temp2
                    crossedchrolist.append(newpath1)  #将交叉后的path存入新种群中
                    crossedchrolist.append(newpath2)
                    #print '交叉成功'
                    break
                if num == 4:
                    crossedchrolist.append(momchro)
                    crossedchrolist.append(dadchro)
                    #print '交叉失败'
        else:   #不进行交叉的情况
            crossedchrolist.append(momchro)
            crossedchrolist.append(dadchro)
            #print '不交叉'
    print " 交叉操作结束"
    return crossedchrolist


####################################  mutantion  ###############################################
def random_subpath(transition,SM):  #以给定transition为开始的子path
    tran_matrix_index=int(transition[1:])-1  #将字符串迁移编号转换成矩阵的行号
    path = []
    path_new = []
    m = validpath_matrix(SM)
    endlist = get_endtran_from_matrix(m)
    i = tran_matrix_index
    path.append(i)
    while 1:
        while 1:
            randnum = random.randint(0, len(m[i]) - 1)
            if (m[i][randnum] == 1):
                path.append(randnum)
                break
        i = randnum
        timeslist = Counter(path).values()  # 每个重复出现的迁移的出现次数
        maxtimes = max(timeslist)
        # if len(path) == 5 or i in endlist or maxtimes > 2:
        if len(path) == 5 or maxtimes > 3 :
            break
    for index in range(len(path)):
        tran = 'T' + str(path[index] + 1)
        path_new.append(tran)
    return path_new

def mutantion2(crossedchrolist,pm,SM):
    # print " 开始变异操作"
    mutantedchrolist = []
    for i in range(len(crossedchrolist)):
        mutantedchro=crossedchrolist[i]
        print " 变异个体",mutantedchro
        # randnum = random.uniform(0,1)  # 随机数 决定进行哪个变异算子
        #
        # if randnum<=(pm/2):   # 变异1：随机改变一个子path
        traninforlist = SM.transitionList
        endtranlist = get_endstran_for_efsm(SM)
        for num in range(5):  # 最多重选5次，如果仍找不到可变异的子path，则不进行变异
            tran_index = random.randint(1, len(mutantedchro) - 2)  # 获得该transition的位置
            mutantran = mutantedchro[tran_index]  # 记录该transition的name
            print " 变异迁移",mutantran
            temp1 = mutantedchro[0:tran_index]  # 将原path（个体）拆分成两部分
            # print " 变异个体前半段",temp1
            # temp2=mutantedchro[tran_index:]

            samesrc_tranlist = []  # 存放mutantran的兄弟迁移
            for item in traninforlist:
                if item.name == mutantran:
                    src_state = item.src.name
                    for i in traninforlist:
                        if (i.src.name == src_state) and (i.name not in endtranlist) and (i.name != mutantran):
                            samesrc_tranlist.append(i.name)
                    break
            if len(samesrc_tranlist) != 0:  # 有可替换的兄弟迁移，则随机选择一兄弟，随机生成由该兄弟出发的子path
                print " 同源迁移" ,samesrc_tranlist

                newtran = choice(samesrc_tranlist)  # newtran不能为终止迁移之一！
                print " 选择的同源迁移",newtran
                # while 1:
                p = random_subpath(newtran, SM)
                    # if len(p) < 6:
                    #     break
                print " 兄弟迁移",p
                newpath = temp1 + p
                print " 新迁移",newpath
                mutantedchrolist.append(newpath)
                # print '1变异成功'
                break
            if num == 4:  # 始终没找到可以改变的subpath
                mutantedchrolist.append(mutantedchro)
                # print '1变异失败'
        continue
    # print " 变异操作结束"
    return mutantedchrolist
def mutantion(crossedchrolist,pm,SM):
    print " 开始变异操作"
    mutantedchrolist = []
    for i in range(len(crossedchrolist)):
        mutantedchro=crossedchrolist[i]
        # print " 变异个体",mutantedchro
        randnum = random.uniform(0,1)  # 随机数 决定进行哪个变异算子
        print " randnum",randnum
        #
        kk = pm/2
        print " kk",kk
        if randnum <= (pm/2):   # 变异1：随机改变一个子path   randnum < 0.4
            print " 变异1"
            traninforlist = SM.transitionList
            endtranlist = get_endstran_for_efsm(SM)
            for num in range(5):  # 最多重选5次，如果仍找不到可变异的子path，则不进行变异
                tran_index = random.randint(1, len(mutantedchro) - 2)  # 获得该transition的位置
                mutantran = mutantedchro[tran_index]  # 记录该transition的name
                print " 变异迁移", mutantran
                temp1 = mutantedchro[0:tran_index]  # 将原path（个体）拆分成两部分
                print " 变异个体前半段",temp1
                # temp2=mutantedchro[tran_index:]

                samesrc_tranlist = []  # 存放mutantran的兄弟迁移
                for item in traninforlist:
                    if item.name == mutantran:
                        src_state = item.src.name
                        for i in traninforlist:
                            if (i.src.name == src_state) and (i.name not in endtranlist) and (i.name != mutantran):
                                samesrc_tranlist.append(i.name)
                        break
                if len(samesrc_tranlist) != 0:  # 有可替换的兄弟迁移，则随机选择一兄弟，随机生成由该兄弟出发的子path
                    print " 同源迁移", samesrc_tranlist

                    newtran = choice(samesrc_tranlist)  # newtran不能为终止迁移之一！
                    print " 选择的同源迁移", newtran
                    # while 1:
                    p = random_subpath(newtran, SM)
                        # if len(p) < 6:
                        #     break
                    print " 兄弟迁移",p
                    newpath = temp1 + p
                    print " 新迁移", newpath
                    mutantedchrolist.append(newpath)
                    # print '1变异成功'
                    break
                if num == 4:  # 始终没找到可以改变的subpath
                    mutantedchrolist.append(mutantedchro)
                    # print '1变异失败'
            continue
        elif randnum<=(pm):  #变异2：随机替换一个同源同目标状态的迁移  randnum <=0.8
           # 得到全部transition信息
            print " 变异2"
            traninforlist = SM.transitionList
            for num in range(5):
                mutantran = choice(mutantedchro)  # 随机选择一个 变异transition,
                tran_index = mutantedchro.index(mutantran)  # 获得该transition的位置
                src = []  # 存储该迁移的源状态
                tgt = []  # 存储该迁移的目标状态
                for item in traninforlist:
                    if item.name == mutantran:
                        src.append(item.src.name)
                        tgt.append(item.tgt.name)
                        break
                candidate_tran = []  # 用来存储同源同目标的transition
                for item in traninforlist:
                    if (item.src.name == src[0]) and (item.tgt.name == tgt[0]) and (item.name != mutantran):
                        candidate_tran.append(item.name)
                if len(candidate_tran) != 0:
                    r = random.randint(0, len(candidate_tran) - 1)
                    mutantedchro[tran_index]=candidate_tran[r]
                    mutantedchrolist.append(mutantedchro)
                    # print '2变异成功'
                    break
                if num == 4:
                    mutantedchrolist.append(mutantedchro)
                    # print '2变异失败'
            continue
        else:  # 不变异情况
            mutantedchrolist.append(mutantedchro)
            print ' 不变异'''
    print " 变异操作结束"
    return mutantedchrolist


def mutantion1_bak(crossedchrolist, pm, SM):
    print " 开始变异操作"
    mutantedchrolist = []
    for i in range(len(crossedchrolist)):  # 对种群中的每一条序列依次进行随机变异
        mutantedchro = crossedchrolist[i]
        # 变异2：对一个个体随机替换一个同源同目标状态的迁移
        traninforlist = SM.transitionList
        for num in range(5):
            '''虽然是单点交叉，但是交叉点看怎么选，不会老集中在一个地方，随机也随机的老在那，很烦人
            我觉得可以看一个迁移的出度，根据出度大小来选择交叉点。出度大的，它到达的迁移范围就广。就有可能去到新的迁移。
            '''
            mutantran = choice(mutantedchro)  # 随机选择一个 变异transition,
            print " 变异迁移", mutantran
            tran_index = mutantedchro.index(mutantran)  # 获得该transition的位置
            src = []  # 存储该迁移的源状态
            tgt = []  # 存储该迁移的目标状态
            for item in traninforlist:  # 获得变异迁移的源状态及目标状态
                if item.name == mutantran:
                    src.append(item.src.name)
                    tgt.append(item.tgt.name)
                    break
            candidate_tran = []  # 用来存储同源同目标的transition
            for item in traninforlist:
                if (item.src.name == src[0]) and (item.tgt.name == tgt[0]) and (item.name != mutantran):
                    candidate_tran.append(item.name)
            if len(candidate_tran) != 0:  # 若存在可替换的同源同目标状态的迁移
                r = random.randint(0, len(candidate_tran) - 1)  # 则随机选取其中一个 ，进行替换
                '''我觉得不应该随机，可以在候选迁移集中选择当前迁移序列没有的迁移'''
                for r in range(len(candidate_tran)):
                    if candidate_tran[r] not in mutantedchro:
                        mutantedchro[tran_index] = candidate_tran[r]
                        mutantedchrolist.append(mutantedchro)
                        # print '2变异成功'
                        break

            if num == 4:
                mutantedchrolist.append(mutantedchro)
                # print '2变异失败'
        continue
        # else:  # 不变异情况
        #     mutantedchrolist.append(mutantedchro)
        # print '不变异'''
    print " 变异操作结束"
    return mutantedchrolist

def obtain_candate(mutantran,traninforlist):
    src = []  # 存储该迁移的源状态
    tgt = []  # 存储该迁移的目标状态
    for item in traninforlist:  # 获得变异迁移的源状态及目标状态
        if item.name == mutantran:
            src.append(item.src.name)
            tgt.append(item.tgt.name)
            break
    candidate_tran = []  # 用来存储同源同目标的transition
    for item in traninforlist:
        if (item.src.name == src[0]) and (item.tgt.name == tgt[0]) and (item.name != mutantran):
            candidate_tran.append(item.name)

    return candidate_tran

def obtain_src_candate(mutantran,traninforlist):
    src = []  # 存储该迁移的源状态
    for item in traninforlist:  # 获得变异迁移的源状态及目标状态
        if item.name == mutantran:
            src.append(item.src.name)
            break
    candidate_src = []  # 用来存储同源的transition
    for item in traninforlist:
        if (item.src.name == src[0])  and (item.name != mutantran):
            candidate_src.append(item.name)
    return candidate_src

def obtain_point(seq,traninforlist):
    total = []
    totalcandate = []
    for T in seq:
        c = obtain_src_candate(T,traninforlist)
        total.append(len(c))
        totalcandate.append(c)
    return total,totalcandate


def mutantion3(crossedchrolist,pm,SM):
    print " 开始变异操作"
    mutantedchrolist = []
    traninforlist = SM.transitionList
    m = validpath_matrix(SM)
    endlist = get_endtran_from_matrix(m)
    print "endlist",endlist
    for i in range(len(crossedchrolist)): # 对种群中的每一条序列依次进行随机变异
        mutantedchro=crossedchrolist[i]
        randnum = random.uniform(0, 1)  # 随机数 决定进行哪个变异算子
        if(randnum >=0 and randnum <0.33):
            # 变异1：对一个个体的每一个迁移替换一个同源同目标状态的迁移
            print " 变异1"
            for mt in range(1,len(mutantedchro)-1):  # 每一个迁移都判断是否能变异，引入新transition,
                '''虽然是单点交叉，但是交叉点看怎么选，不会老集中在一个地方，随机也随机的老在那，很烦人
                我觉得可以看一个迁移的出度，根据出度大小来选择交叉点。出度大的，它到达的迁移范围就广。就有可能去到新的迁移。
                '''
                print " 变异迁移", mutantedchro[mt]
                candidate_tran = obtain_candate(mutantedchro[mt], traninforlist)  # 获得该迁移的可替换迁移候选集
                print " 变异迁移的候选集", candidate_tran
                if len(candidate_tran) != 0:  # 若存在可替换的同源同目标状态的迁移
                    '''我觉得不应该随机，可以在候选迁移集中选择当前迁移序列没有的迁移'''
                    for r in range(len(candidate_tran)):
                        t = random.randint(0, len(candidate_tran) - 1)  # 则随机选取其中一个 ，进行替换
                        # if candidate_tran[t] not in mutantedchro:
                        #     print "替换成迁移", candidate_tran[t]
                        mutantedchro[mt] = candidate_tran[t]
                        break
            mutantedchrolist.append(mutantedchro)
        elif(randnum >= 0.33 and randnum <= 0.66):
            print " 变异2"
            for num in range(6):
                mutantran = choice(mutantedchro)  # 随机选择一个 变异transition,
                print " 变异迁移", mutantran
                tran_index = mutantedchro.index(mutantran)  # 获得该transition的位置
                candidate_tran = obtain_candate(mutantran,traninforlist)
                if len(candidate_tran) != 0:  # 若存在可替换的同源同目标状态的迁移
                    temps = []
                    for ti in range(len(candidate_tran)):
                        # r = random.randint(0, len(candidate_tran) - 1)  # 则随机选取其中一个 ，进行替换
                        if candidate_tran[ti] not in mutantedchro:
                            temps.append(ti)
                    if len(temps)!=0:
                        r = choice(temps)
                        mutantedchro[tran_index] = candidate_tran[r]
                        mutantedchrolist.append(mutantedchro)
                    else:
                        r = random.randint(0, len(candidate_tran) - 1)
                        mutantedchro[tran_index] = candidate_tran[r]
                        mutantedchrolist.append(mutantedchro)
                if num == 5:
                    mutantedchrolist.append(mutantedchro)
                    # print '2不变异'
        else:
            print " 变异3"
            #变异2，单点变异+子path替换
            newpath = []
            path = []
            path_new = [] #序列后半段
            total,totalcandi = obtain_point(mutantedchro,traninforlist)
            maxvalue = max(total)
            index = total.index(maxvalue)  #取得变异点的索引
            print " mutantedchro", mutantedchro[index]
            print " index",index
            mtran = mutantedchro[index]  # 变异迁移
            print " 变异迁移",mtran
            candidate_tran = totalcandi[index]
            print " 变异迁移的候选迁移",candidate_tran
            pre_path = mutantedchro[0:index]    # 序列前半段
            print " 序列前半段",pre_path
            if(len(candidate_tran) != 0):
                newtran = choice(candidate_tran)  #以给定newtran为开始的子path
                print " newtran",newtran
                if newtran in SM.endTransitionList:
                    path_new.append(newtran)
                else:
                    tran_matrix_index = int(newtran[1:]) - 1
                    i = tran_matrix_index
                    print " i",i
                    path.append(i)
                    # while 1:
                    while 1:
                        while 1:
                            randnum = random.randint(0, len(m[i]) - 1)
                            if (m[i][randnum] == 1):
                                path.append(randnum)
                                break
                        i = randnum
                        times = Counter(path).values()  # 每个重复出现的迁移的出现次数
                        maxt = max(times)
                        if len(path) < 5 and len(path) >1 and maxt < 3:
                            break
                    print " path", path
                    for index in range(len(path)):
                        tran = 'T' + str(path[index] + 1)
                        path_new.append(tran)
                    newpath = pre_path + path_new
                        # timeslist = Counter(newpath).values()  # 每个重复出现的迁移的出现次数
                        # maxtimes = max(timeslist)
                        # if len(newpath) <15 and len(newpath)>2 and maxtimes <4:
                        #     break
                print " 新路径",newpath
            mutantedchrolist.append(newpath)
    print " 变异操作结束"
    return mutantedchrolist

####################################  update pop  ##############################################
def isCoverAllPath(coverpath):
    cflag = 0
    spath = sensitive_path_info.obtain_spath()
    if len(coverpath) == len(spath):
        cflag = 1
    return cflag


def UpdatePopulation(child,popsize,newM,testdata):  #选择覆盖敏感路径数多的个体组成规模为popsize的新种群
    print " 开始更新操作"
    sub_fitnesslist = []
    print " newM",newM
    for row in newM:
        c = row.count(0.0)
        sub_fitnesslist.append(c)
    all_fitlist=e_fitness_list + sub_fitnesslist #合并elitist，child的 覆盖敏感路径数（fitness）
    print " 精英与子代种群适应度值合并all_fitlist", all_fitlist
    all_pop=elitist_seq + child #合并elitist（字典），child种群
    print " 精英与子代种群序列合并all_pop", all_pop
    totalM= elitist_M + newM
    newpopdata = elitist_data + testdata

    newpop = []
    NewM = []
    NewDate = []
    coverpath = []
    # 这里有个疑虑，按fitness值大小来选，构建出来的NewM有可能错过一些fitness值小，但是覆盖特殊敏感路径的个体，怎么办？
    # 这里的更新策略还差一点，就是怎么保留下fitness值小，但是覆盖特殊敏感路径的个体？
    '''解决策略：
    1.首先，从fitness集合中选择覆盖路径数最多的个体（fitness大的个体），将它覆盖的敏感路径加入coverpath中
    2.其次，按fitness值由大到小的顺序依次寻找个体，判断个体是否覆盖的路径是coverpatn中没有包含的，
        如果是，则选择该个体；
        如果不是，则放弃该个体。
    //循环次数不能是popsize，不然遍历不完全，但构建新种群又要满足种群大小，怎么办？
    4.循环len(all_fitlist)次，所有的个体都判断一遍，
       如果选出来的集合覆盖了所有的敏感路径,cflag=1；
       如果选出来的集合没有覆盖所有的敏感路径cflag =0，那么从集合中选择popsize大小的pop，继续去进化
    '''
    temp_all_fit = all_fitlist
    for k in range(len(all_fitlist)):
        cfount = 0
        maxfit = max(all_fitlist)
        maxfit_index = all_fitlist.index(maxfit)
        temp = totalM[maxfit_index]
        for v in range(len(temp)):
            if temp[v] == 0.0:
                if v not in coverpath:
                    coverpath.append(v)
                    cfount += 1
        if cfount !=0:   # 有新路径被覆盖，则对应的个体被add
            newpop.append(all_pop[maxfit_index])
            print " 选择个体后的newpop", newpop
            NewM.append(totalM[maxfit_index])
            NewDate.append(newpopdata[maxfit_index])
            all_fitlist[maxfit_index] = (-100)  # 避免选过的最优个体再次被选
    cflag = isCoverAllPath(coverpath)
    print " cflag",cflag
    if cflag == 0:
        if len(newpop) < popsize:
            number = 0
            number = popsize - len(newpop)
            print " number",number
            for i in range(number):
                maxfit = max(temp_all_fit)
                maxfit_index = all_fitlist.index(maxfit)
                newpop.append(all_pop[maxfit_index])
                print " 选择个体后的newpop",newpop
                NewM.append(totalM[maxfit_index])
                NewDate.append(newpopdata[maxfit_index])
                temp_all_fit[maxfit_index] = (-100)  # 避免选过的最优个体再次被选
        print " 更新的newpop", len(newpop),newpop
        print " newpop对应的M",len(NewM), NewM
        return newpop, NewM,NewDate,cflag
    else:
        print " 完全覆盖路径==更新后newpop", newpop
        print " 完全覆盖路径===newpop对应的M", NewM
        return newpop, NewM,NewDate,cflag

    # print " 更新操作结束"


def update_cov(parent,child,popsize,originM,newM,ntestdata,testdata,List_global_fitness):  #选择覆盖迁移多的个体组成规模为M的新种群
    print " 开始更新操作"
    c_fitnesslist = []
    print "newM", newM
    for row in newM:
        c = row.count(0.0)
        c_fitnesslist.append(c)

    all_fitlist = List_global_fitness + c_fitnesslist  # 合并elitist，child的 覆盖敏感路径数（fitness）
    print " 合并all_fitlist", len(all_fitlist),all_fitlist
    all_pop = parent + child  # 合并种群
    print " 合并all_pop", len(all_pop),all_pop
    totalM = originM + newM
    print " 合并M"
    for m in totalM:
        print m
    newpopdata = testdata + ntestdata

    NewM = []
    NewDate = []
    coverpath = []
    newpop=[]
    for i in range(popsize):
        maxfit = max(all_fitlist)
        maxfit_index = all_fitlist.index(maxfit)
        temp = totalM[maxfit_index]
        for v in range(len(temp)):
            if temp[v] == 0.0:
                if v not in coverpath:
                    coverpath.append(v)
        newpop.append(all_pop[maxfit_index])
        print " 选择个体后的newpop", newpop
        NewM.append(totalM[maxfit_index])
        NewDate.append(newpopdata[maxfit_index])
        all_fitlist[maxfit_index] = (-100)  # 避免选过的最优个体再次被选
    cflag = isCoverAllPath(coverpath)
    print " 更新操作结束"
    return newpop, NewM,NewDate,cflag
################################  the part is the  GA algorihm  ##############################################

def Global_fitness_Evaluation(M):
    list_global_fitness = []
    for i in range(len(M)):
        a = M[i]
        b = a.count(0.0)
        list_global_fitness.append(b)
    return list_global_fitness

def isCoverNewPath_origin(m):
    # print " m",m
    flag = 0
    old_path = []
    m_cover_path = []
    temp = []
    for j in range(len(m)):
        if m[j] == 0.0:
            m_cover_path.append(j)
    if len(elitist_path)!= 0:
        for key in elitist_path:
            # print " elitist_path[key]",elitist_path[key]
            old_path.extend(elitist_path[key])
            # print"old_path", old_path
            # print"m_cover_path", m_cover_path
            temp = m_cover_path + old_path  #新旧覆盖路径合并
            old_path =[]
    else:
        temp = m_cover_path
    # print " temp",temp
    s = list(set(temp)) # 去重
    # print " 去重后的覆盖",s
    if len(s) > len(elitist_path):  # s的长度大于现有覆盖的路径条数，说明覆盖了新路径
        flag = 1
    # print flag
    return flag


def SelectEliteInd_origin(pop, List_global_fitness,testdata,M):
    '''精英个体选择策略：若有能覆盖新的路径的个体，则加入精英个体
    步骤：若当代种群中某一个个体覆盖新的敏感路径，则该个体为精英个体；
         若当代种群没有覆盖新路径的个体，通过判断成员（包含）关系，确保不会消掉覆盖某一条路径的某一个体情况下，
         依照fitness值大的替换原先的精英个体；
         只是完成基础，还没按规则写 2018-06-19
         已经更新，规则就是（优先）覆盖新路径才作为精英个体，覆盖的路径数多就作为精英个体
    '''
    coverp = []
    elitist_long = len(elitist_seq)
    print " 精英选择"
    print "pop",pop
    print "List_global_fitness",List_global_fitness,len(List_global_fitness)
    for i in range(len(List_global_fitness)):
        if List_global_fitness[i] > 0:
            coverNewPath = isCoverNewPath_origin(M[i])
            print " 是否覆盖新路径coverNewPath",coverNewPath
            if coverNewPath == 1:  # 有个问题，每次增加新的键值对，若都按i添加则会重复会覆盖，考虑一下怎么解决整个问题？？
                elitist_seq[elitist_long] = pop[i]  # {1：[t1...tk],2：[tm...tg],3：[t1...tb]...}
                elitist_data[elitist_long] = testdata[i]  # {1:[v1...vn],2:[vd...vb],3:[vk...vn]...}
                elitist_M[elitist_long] = M[i]  # {1:[2,..0.0,2,2],2:[0.0,..0.0,2,2],3:[2,..0.0,2,2]...}
                # print "精英序列", elitist_seq
                # print "精英序列的数据", elitist_data
                # print "精英序列的M", elitist_M
                row = M[i]
                # print "row", M[i]
                for value in range(len(row)):
                    if row[value] == 0.0:
                        coverp.append(value)
                # print "精英个体覆盖的路径", coverp
                elitist_path[elitist_long] = coverp  # {1:[p1...pn],2:[p4...pk],3:[pf...pn]...}  4个elitist以键值对应
                coverp = []
            elitist_long += 1  # 把三者变为全局变量，每次添加精英个体到字典时，看一下当前字典的长度，新增的键值=当前字典长度+1
       # return elitist_seq,elitist_data,elitist_path 不用return，是全局变量，哪里都可以调用,
    print " =======全局精英信息========："
    print " elitist_seq", elitist_seq
    print " elitist_data", elitist_data
    print " elitist_path",elitist_path
    print " elitist_M", elitist_M


def SelectEliteInd(pop, List_global_fitness,testdata,M):
    '''精英个体选择策略：若有能覆盖新的路径的个体，则加入精英个体
    步骤：若当代种群中某一个个体覆盖新的敏感路径，则该个体为精英个体；
         若当代种群没有覆盖新路径的个体，通过判断成员（包含）关系，确保不会消掉覆盖某一条路径的某一个体情况下，
         依照fitness值大的替换原先的精英个体；
         只是完成基础，还没按规则写 2018-06-19
         已经更新，规则就是（优先）覆盖新路径才作为精英个体，覆盖的路径数多就作为精英个体
    '''
    print " 精英选择"
    print " pop",pop
    print " List_global_fitness",List_global_fitness,len(List_global_fitness)
    for i in range(len(List_global_fitness)):
        if List_global_fitness[i] > 0:
            row = M[i]
            for p in range(len(row)):  #row:一个测试用例对所有路径的覆盖情况
                if row[p] == 0.0 : #如果某一条路径被覆盖，
                    if p not in elitist_path: #且该路径为新路径，则将个体添加到精英集合中
                        elitist_seq.append(pop[i])  # {[t1...tk],[tm...tg],[t1...tb]...}
                        elitist_data.append(testdata[i])  # {[v1...vn],[vd...vb],[vk...vn]...}
                        elitist_M.append(M[i])  # {[2,..0.0,2,2],[0.0,..0.0,2,2],[2,..0.0,2,2]...}
                        e_fitness_list.append(List_global_fitness[i]) # [2,4,3,1,2,...] fitness值
                        elitist_path.append(p)

    print " =======全局精英信息========："
    print " elitist_seq",len(elitist_seq), elitist_seq
    print " elitist_data",len( elitist_data), elitist_data
    print " e_fitness_list",len(e_fitness_list),e_fitness_list
    print " elitist_path",len(elitist_path),elitist_path,
    print " elitist_M", len(elitist_M),elitist_M


def GA(pop,pc,pm,popsize,SM,M,testdata):
    List_global_fitness = Global_fitness_Evaluation(M)
    SelectEliteInd(pop, List_global_fitness, testdata, M)  # 选个体是把序列数据都记录进去的

    # temp = copy.deepcopy(pop) #保留父代  父代已经被选过一次了，不用在参与更新了
    # 计算种群fitness，评估种群
    print " 变异前的种群",pop
    selectedpop = selection(pop,List_global_fitness) #选择fitness小的
    crossedpop = crossover(selectedpop, pc,SM)
    # mutantedpop = mutantion1(crossedpop, pm,SM)  #3种变异策略
    mutantedpop = mutantion3(crossedpop, pm, SM)  #single point mutant
    childpop_fealible = del_infeasible_after_mutant(mutantedpop)
    # print 'fesible删不可行path后剩余条数：', len(childpop_fealible)
    childpop_repeat = delete_repeat_chrom(childpop_fealible)
    # print 'repeat删重复个体后剩余的种群：', len(childpop_repeat),childpop_repeat

    #需要对去重后的个体进行执行评估，不然没办法依据fitness更新
    print " 变异后去重的种群",len(childpop_repeat),childpop_repeat
    strm = "变异后去重的种群"
    recordFun.recordInitalPop(strm,childpop_repeat)


    print " 进入更新的种群大小", len(childpop_repeat),childpop_repeat
    ntestdata, newM = execute.gdata(childpop_repeat, SM)  # 为序列产生数据，执行测试用例，获取新子种群的评估矩阵M

    # update功能 重写，加入精英策略的更新 2018-06-19
    '''更新策略，精英集合与变异后的集合种群参与更新，从中选出新种群
    个体fitness大的更新
    '''
    # newpop, NewM, NewDate, cflag = update_cov(temp,childpop_repeat,popsize,M,newM,ntestdata,testdata,List_global_fitness)
    newpop,NewM,NewDate,cflag = UpdatePopulation(childpop_repeat, popsize,newM,ntestdata)  #My
    print " 新种群大小",len(newpop)
    return newpop,NewM,NewDate,cflag

def generate_seq_by_ga(SM,popsize):
    # popsize = 10
    pc = 0.8
    pm = 0.8
    count = 0
    object_ST = object_T()
    pop = initialpop_feasible(popsize,SM)
    print " 父代种群：",pop
    j = 0
    while 1:
        count = count + 1
        popcov = pop_coverage(pop,object_ST)  # 评估种群
        # print 'population covered t:', popcov
        print " 种群覆盖目标迁移数",len(popcov)
        print " 目标迁移数",len(object_ST)
        if len(popcov) == len(object_ST) or count == 10000:
             print '================================================'
             print '生成代数:', count
             break
        else:
             j=j+1
             print " 第", j, "代进化=========="
             pop = GA(pop, pc, pm, popsize,SM)
    for subpop in pop:
        print subpop,"\n"
    return pop

if __name__ == '__main__':
    SM = obtain_efsm_info2.obtain_efsm()
    SM.allPathNum()
    print " %s has %s states and  %s transitions" % (SM.name, len(SM.stateList), len(SM.transitionList))
    print " start transition：", SM.startTransitionList
    print " end transition：", SM.endTransitionList
    # popsize = 50
    # generate_seq_by_ga(SM,popsize)
    # object_T()'''
    # m = [2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2, 2, 2]
    # a = isCoverNewPath(m)
    # print a
    # newM= [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0,
    #   0.0, 2],
    #  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0,
    #   0.0, 2]]
    #
    # elitist_seq=[
    #     ['T46', 'T49', 'T50', 'T47', 'T48', 'T47', 'T48', 'T81'], ['T38', 'T41', 'T42', 'T41', 'T42', 'T43', 'T44',
    #                                                                'T45', 'T80']]
    # elitist_data=[['xz27o5', 'yJTn2P', 'gA4RbT', 'e3RLub', 'R1qJzf', 'GoQqbd', 'Q2zBap', 'DfCO3P'], ['T2Vctg', 'NeGDTz',
    #                                                                                                 '7Gb0qb']]
    # e_fitness_list=[2, 3]
    # elitist_path=[[36, 37], [10, 36, 37]]
    # elitist_M=[
    #     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1.004950495049505, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    #      2, 2, 2, 2, 0.0, 0.0, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    #                                 2, 2, 2, 2, 2, 2, 2, 2, 2, 0.0, 0.0, 2]]
    #
    # child=[['T1', 'T2', 'T75'], ['T27', 'T30', 'T31', 'T30', 'T31', 'T28', 'T29', 'T79']]
    # UpdatePopulation(child,2,newM,2)
    # pop = initialpop_feasible(26,SM)
    pop = [['T3', 'T4', 'T5', 'T4', 'T5', 'T87', 'T16', 'T17', 'T18', 'T14', 'T15', 'T14', 'T15', 'T12', 'T13', 'T14', 'T15', 'T77'],
['T46', 'T51', 'T52', 'T53', 'T92', 'T93', 'T83'],
['T46', 'T49', 'T50', 'T47', 'T48', 'T92', 'T82'],
['T3', 'T87', 'T16', 'T17', 'T18', 'T14', 'T15', 'T12', 'T13', 'T14', 'T15', 'T77'],
['T38', 'T39', 'T40', 'T43', 'T44', 'T45', 'T80'],
['T3', 'T87', 'T16', 'T17', 'T18', 'T14', 'T15', 'T88', 'T22', 'T23', 'T89', 'T28', 'T29', 'T90', 'T80'],
['T3', 'T4', 'T5', 'T4', 'T5', 'T8', 'T9', 'T10', 'T76'],
['T1', 'T2', 'T75'],
['T11', 'T88', 'T22', 'T23', 'T89', 'T28', 'T29', 'T90', 'T80'],
['T19', 'T20', 'T21', 'T78'],
['T3', 'T4', 'T5', 'T4', 'T5', 'T8', 'T9', 'T10', 'T76'],
['T3', 'T87', 'T12', 'T13', 'T14', 'T15', 'T12', 'T13', 'T14', 'T15', 'T77'],
['T67', 'T68', 'T69', 'T70', 'T71', 'T70', 'T71', 'T68', 'T69', 'T85'],
['T3', 'T4', 'T5', 'T4', 'T5', 'T87', 'T88', 'T22', 'T23', 'T89', 'T28', 'T29', 'T90', 'T80'],
['T11', 'T16', 'T17', 'T18', 'T14', 'T15', 'T14', 'T15', 'T12', 'T13', 'T14', 'T15', 'T77'],
['T11', 'T88', 'T22', 'T23', 'T89', 'T28', 'T29', 'T90', 'T80'],
['T56', 'T94', 'T60', 'T61', 'T84'],
['T19', 'T20', 'T21', 'T78'],
['T67', 'T68', 'T69', 'T70', 'T71', 'T70', 'T71', 'T68', 'T69', 'T85'],
['T67', 'T72', 'T73', 'T74', 'T85'],
['T11', 'T88', 'T89', 'T32', 'T33', 'T37', 'T90', 'T91', 'T81'],
['T54', 'T55', 'T82'],
['T54', 'T55', 'T93', 'T57', 'T58', 'T94', 'T84'],
['T67', 'T68', 'T69', 'T85'],
['T3', 'T87', 'T12', 'T13', 'T77'],
['T11', 'T14', 'T15', 'T77'],['T56', 'T57', 'T58', 'T83'],['T67', 'T72', 'T73', 'T74', 'T72', 'T73', 'T74', 'T68', 'T69', 'T85']]
#     mpop =[['T1', 'T3', 'T5', 'T4'],['T1', 'T3', 'T4'],['T1', 'T3', 'T8', 'T4'],['T1', 'T3', 'T5', 'T8', 'T8', 'T11', 'T21', 'T7', 'T4']
# ,['T1', 'T3', 'T6', 'T7', 'T11', 'T14', 'T19', 'T20', 'T19', 'T20', 'T14', 'T21', 'T7', 'T5', 'T4'],['T1', 'T3', 'T6', 'T7', 'T4']]
    mpop = initialpop_feasible(6,SM)
    print " 变异前"
    for i in mpop:
        print i
    newpop = mutantion1(mpop,0.9,SM)
    print " 变异后"
    for j in newpop:
        print j


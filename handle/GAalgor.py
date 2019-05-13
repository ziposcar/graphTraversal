# -*-  coding: utf-8 -*-
import random
import math
import cal_data_fit
import seq_to_script
import recordFun
import time
from datetime import datetime
import sensitive_path_info
import execute
import copy
class GA:
    def __init__(self, varType , pathT, tevent,pathIndex,p_fit_current):
        self.min = 0
        self.max = 8000
        self.varType = varType
        self.pathT = pathT
        self.tevent = tevent

        self.objectPathIndex = pathIndex
        self.p_fit_current = p_fit_current


    ######################  进制转换  ##############################
    def dec2bin(self,num):
        la = []
        re = ''
        while True:
            num, remainder = divmod(num, 2)  #divmod函数把除数和余数运算结果结合起来
            la.append(str(remainder))
            if num == 0:
                result = ''.join(la[::-1])
                if len(result) < 7:
                    l = 7-len(result)
                    for i in range(l):
                        re += '0'
                    result = re + str(result)
                    # print result
                return result


    def bin2dec(self,string_num):
        # return str(int(string_num, 2))
        return int(string_num, 2)

    ######################  编码及初始解确定  ########################
    def GenerateRandomString(self):
        ''' 在三个范围内，随机选择n个字符组成长度long为n的string型数据  '''
        # basechars = [chr(i) for i in x]  #把ASCII转为具体字符
        x1 = range(97, 123)
        basechars1 = [chr(i) for i in x1]
        x2 = range(65, 91)
        basechars2 = [chr(i) for i in x2]
        x3 = range(48, 58)
        basechars3 = [chr(i) for i in x3]
        res = ''
        # long = random.randint(6, 15)
        long = 6
        for i in range(long):
            h = [1, 2, 3]
            c = random.choice(h)  # 97-122 a-z, 65-90 A-Z, 48-57 0-9  #代表从1到5(不包含5),因此范围要+1
            if c == 1:
                r = random.choice(basechars1)
            elif c == 2:
                r = random.choice(basechars2)
            else:
                r = random.choice(basechars3)
            res += r
        return res  # 这样是一个变量的值

    def GenerateRandomInt(self):
        ret = random.choice(range(0, 8000))
        return ret

    def GenerateRandomdate(self):
        # 创建日期辅助表
        datestart = '2018-01-01'
        dateend = '2021-12-30'
        # 转为日期格式
        datestart = datetime.datetime.strptime(datestart, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(dateend, '%Y-%m-%d')
        date_list = []
        date_list.append(datestart.strftime('%Y-%m-%d'))
        while datestart < dateend:
            # 日期叠加一天
            datestart += datetime.timedelta(days=+1)
            # 日期转字符串存入列表
            date_list.append(datestart.strftime('%m-%d'))
        print(date_list)
        ret = random.choice(date_list)
        return ret

    def Initial_data(self,varType):
        solve = []
        for num in varType:
            if num == 'Boolean':
                data = random.randint(0, 1)
                solve.append(data)
            elif num == 'string':
                str = self.GenerateRandomString()
                solve.append(str)
            elif num == 'date':
                str = self.GenerateRandomdate()
                solve.append(str)
            else:
                str1 = self.GenerateRandomInt()
                solve.append(str1)
        return solve


    def mutanForString(self,mlist,base):
         x1 = range(97, 123)
         basechars1 = [chr(i) for i in x1]
         x2 = range(65, 91)
         basechars2 = [chr(i) for i in x2]
         x3 = range(48, 58)
         basechars3 = [chr(i) for i in x3]
         h = [1, 2, 3]
         c = random.choice(h)  # 97-122 a-z, 65-90 A-Z, 48-57 0-9  #代表从1到5(不包含5),因此范围要+1
         if c == 1:
             r = random.choice(basechars1)
         elif c == 2:
             r = random.choice(basechars2)
         else:
             r = random.choice(basechars3)
         rand = [1,3]
         mtype = random.choice(rand)
         local = random.choice(base)  # 选择变异位置
         if mtype == 1:   # 替换一个字符
             mlist[local] = r
         # elif mtype == 2:  # 删除一个字符
         #     del mlist[local]
         elif mtype == 3:   # 任意位置插入一个字符
             location = random.choice(range(0,len(mlist)))
             mlist.insert(location, r)
         return mlist


    def mutanForInt(self,change_object):
        print "change_object", change_object
        temp = []
        t = 0.6  # t = T当前温度/T初温  初始温度是高温，当前温度肯定低于初温
        num = self.dec2bin(change_object)

        L = len(num)
        P = int(L * t)
        pos = random.choice(range(P, L))
        poss = random.choice(range(0, P-1))
        pos0 = L - pos + 1  # 从右边数起第pos0位取反
        pos1 = L - poss -1
        local=[pos0 , pos1]

        randnum = random.uniform(0, 1)
        if randnum < 0.5:
            res = ''
            for i in num:
                temp.append(i)
            if temp[pos0] == '1':
                temp[pos0] = '0'
            else:
                temp[pos0] =  '1'
            for i in temp:
                res += i
        else:
            res = ''
            for i in num:
                temp.append(i)
            for i in local:
                if temp[i] == '1':
                    temp[i] = '0'
                else:
                    temp[i] = '1'
            for i in temp:
                res += i
        data = self.bin2dec(res)
        print "修正后", data
        return data

    def fit_handl(self,dataM):
        fit_list = []
        #取每个个体对目标路径的fit
        for i in dataM:
            fit_list.append(i[self.objectPathIndex])

        # 每个个体fit标准化
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
            cumfitlist.append(t)  # 标准化结果
        return cumfitlist

    def selection(self,pop,dataM):
        print "开始选择操作"
        selectedchrolist = []
        templist = self.fit_handl(dataM)
        print"所有个体fitness列表", len(templist), templist  # for test
        for i in range(len(pop)):  # 若种群大小为M，则用随机数选择M次，将这些父母按被选择的顺序存入selectedchro列表中，父母会重复被选择
            randnum = random.uniform(0, 1)
            # print randnum                  #for test
            for j in range(len(pop)):
                if randnum <= templist[j]:
                    selectedchrolist.append(pop[j])
                    break

        # print '选择后的种群：',selectedchrolist
        print "选择操作结束"
        return selectedchrolist


    def crossover(self,selectedchrolist,pc):
        crossedchrolist = []
        print "开始交叉操作"
        for i in range(0, len(selectedchrolist), 2):  # 每两个个体作为一对父母
            momchro = selectedchrolist[i]
            dadchro = selectedchrolist[i + 1]
            randnum = random.uniform(0, 1)  # 随机数决定是否执行交叉
            if randnum <= pc:
                crosspoint = random.randint(0,len(momchro)-1)
                temp = momchro[crosspoint]
                momchro[crosspoint]=dadchro[crosspoint]
                dadchro[crosspoint]=temp
                crossedchrolist.append(momchro)
                crossedchrolist.append(dadchro)
            else:  # 不进行交叉的情况
                crossedchrolist.append(momchro)
                crossedchrolist.append(dadchro)
                # print '不交叉'
        print "交叉操作结束"
        return crossedchrolist


    def mutantion(self,crossedchrolist,pm):
        mutanchrolist = []
        for i in range(len(crossedchrolist)):
            mutan = crossedchrolist[i]
            randnum = random.uniform(0, 1)  # 随机数决定是否执行交叉
            if randnum <= pm:
                mutanpoint = random.randint(0, len(mutan) - 1)
                newmutan = self.mutanForString(mutan,mutanpoint)
                mutanchrolist.append(newmutan)
            else:
                mutanchrolist.append(mutan)

        return mutanchrolist


    def updata(self,oldpop,newpop,oldM,newM,popsize):
        oldfit = []
        for i in oldM:
            oldfit.append(i[self.objectPathIndex])
        newfit = []
        for j in newM:
            newfit.append(self.objectPathIndex)

        totalpop = oldpop + newpop
        totalfit = oldfit + newfit

        Newpop = []
        for k in range(popsize):
            maxfit = max(totalfit)
            index = totalfit.index(maxfit)
            Newpop.append(totalpop[index])
            totalfit[index] = -100  # 避免选过的最优个体再次被选
        return Newpop
        # 搜索算法5： 遗传算法
        # 原理： 首先随机生成一组解，我们称之为种群，在优化过程的每一步，算法会计算整个种群的成本函数，
        #       从而得到一个有关题解的有序列表。随后根据种群构造进化的下一代种群，方法如下：
        #       遗传：从当前种群中选出代价最优的一部分加入下一代种群，称为“精英选拔”
        #       变异：对一个既有解进行微小的、简单的、随机的修改
        #       交叉：选取最优解中的两个解，按照某种方式进行交叉。方法有单点交叉，多点交叉和均匀交叉
        # 一个种群是通过对最优解进行随机的变异和配对处理构造出来的，它的大小通常与旧的种群相同，尔后，这一过程会
        #       一直重复进行————新的种群经过排序，又一个种群被构造出来，如果达到指定的迭代次数之后题解都没有得
        #       改善，整个过程就结束了
        # 参数：
        # popsize-种群数量 step-变异改变的大小 mutprob-交叉和变异的比例 elite-直接遗传的比例 maxiter-最大迭代次数

    def geneticoptimize(self):
        mm = sensitive_path_info.build_m()
        # 初始化种群
        popsize = 30
        pc = 0.85
        pm = 0.1
        datapop = []
        dataM=[]
        searchFlag = 0
        for i in range(popsize):
            datapop.append(self.Initial_data(self.varType))
        #评估初始种群
        for data in datapop:
            seq_to_script.runcase(self.tevent, self.pathT, data)  # 执行当前序列
            test_fit, coverage = cal_data_fit.array_spath()  # 获取对各条路径的覆盖情况 test_fit，及完全覆盖路径的覆盖率
            if test_fit[self.objectPathIndex] == 0.0 :
                print "满足结果的测试数据为",zip(self.pathT,data)
                searchFlag = 1
                return searchFlag,data
            else:
                if len(test_fit) == 0:  # 构造覆盖矩阵dataM
                    dataM.append(mm)
                else:
                    dataM.append(test_fit)
        iteration = 0
        while iteration <= 500:
            temp = copy.deepcopy(datapop)  # 保留父代
            oldM = dataM
            # 选择
            selectpop = self.selection(datapop, dataM)
            # 交叉
            crosspop = self.crossover(selectpop, pc)
            # 变异
            mutanpop = self.mutantion(crosspop, pm)
            # 评估新种群
            dataM = []
            for data in mutanpop:
                seq_to_script.runcase(self.tevent, self.pathT, data)  # 执行当前序列
                test_fit, coverage = cal_data_fit.array_spath()  # 获取对各条路径的覆盖情况 test_fit，及完全覆盖路径的覆盖率
                if test_fit[self.objectPathIndex] == 0.0:
                    print "满足结果的测试数据为", data
                    searchFlag = 1
                    return searchFlag,zip(self.pathT, data)
                else:
                    if len(test_fit) == 0:  # 构造覆盖矩阵dataM
                        dataM.append(mm)
                    else:
                        dataM.append(test_fit)
            # 更新
            datapop = self.updata(temp, mutanpop, oldM, dataM, popsize)
            iteration += 1
            # 这里会直接到while True那句话再开始


if __name__ == '__main__':
    testdata = ['f83YY1', '9xdi5O', '74x02T', 'G4TR7B', 'OlvHct', '19oTXc', '2sEU26', 'ivL3x5', 'PnHzo6', 'z1Orq5', '57jK2Y', '8R2bO2']
    dormsol = GA("s", "s","s", testdata, "s")
    # dormsol.annealingoptimize(domain)
    # var = ['string','int','Boolean']
    # r = dormsol.Initial_solution(var)
    # # print r
    # # # s = dormsol.GenerateRandomString()
    # t = dormsol.interfer_fun(r,var)
    # print t
    dormsol.geneticoptimize()

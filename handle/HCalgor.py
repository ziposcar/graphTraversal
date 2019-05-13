# -*-  coding: utf-8 -*-
import random
import math
import cal_data_fit
import seq_to_script
import recordFun
import time
from datetime import datetime
class HC:
    def __init__(self, varType , pathT, tevent,pathVarData,pathIndex,p_fit_current):
        self.min = 0
        self.max = 8000
        self.varType = varType
        self.pathT = pathT
        self.tevent = tevent
        self.testdata = pathVarData
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
            c = random.choice(h) # 97-122 a-z, 65-90 A-Z, 48-57 0-9  #代表从1到5(不包含5),因此范围要+1
            if c == 1:
                r = random.choice(basechars1)
            elif c == 2:
                r = random.choice(basechars2)
            else:
                r = random.choice(basechars3)
            res += r
        return res    # 这样是一个变量的值

    def GenerateRandomInt(self):
        ret = random.choice(range(self.min,self.max))
        return ret

    def solution(self, vartype):
        var = []
        for num in vartype:
            if num == 'Boolean':
                data = random.randint(0, 1)
                var.append(data)
            elif num == 'string':
                str = self.GenerateRandomString()
                var.append(str)
            else:
                str1 = self.GenerateRandomInt()
                var.append(str1)
        return var

    # 参数varType是变量的类型
    def Initial_solution(self, varType):
        solve = self.solution(varType)
        print "初始解",solve
        return solve

    ######################  扰动函数产生新解  ########################
    """扰动方式：对一个变量a['e7SJF0', '71tU15', '4lY1Qw']的任意一个或多个位置元素a[i]进行变异（替换，删除，添加），
       要求扰动后的元素不能超过解的范围，未解决，打算靠变量的类型确定
       有个问题是：对于n个变量，扰动几个变量呢？得好好想想,目前随机选一个变量
    """
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

    def GenerateRandomdate(self,current):
        # 创建日期辅助表
        datestart = '2018-01-01'
        dateend = '2021-12-30'
        # 转为日期格式
        datestart = datetime.datetime.strptime(datestart, '%Y-%m-%d')
        date = datetime.datetime.strptime(current, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(dateend, '%Y-%m-%d')
        date_list_small = []
        date_list_big = []
        date_list_small.append(datestart.strftime('%Y-%m-%d'))
        date_list_big.append(date.strftime('%Y-%m-%d'))
        while datestart < current:
            # 日期叠加一天
            datestart += datetime.timedelta(days=+1)
            # 日期转字符串存入列表
            date_list_small.append(datestart.strftime('%m-%d'))
        while current < dateend:
            # 日期叠加一天
            current += datetime.timedelta(days=+1)
            # 日期转字符串存入列表
            date_list_big.append(current.strftime('%m-%d'))
        return date_list_small,date_list_big
    def Perturbation(self,old_solve,varType):   # 扰动函数

        print "old_solve",old_solve
        index_solve = random.randint(0, len(old_solve)-1) # 随机选一个位置
        change_object = old_solve[index_solve]  # 确定该位置上的元素，将它作为扰动对象
        print "待变异对象",change_object
        if varType[index_solve] == 'string':
            base = []
            for i in range(len(change_object)):
                base.append(i)
            # print "base",base
            tem = []
            temp = []
            result = ''
            for x in change_object:  # 'N6Md10'
                tem.append(x)
            # print "change_object转为list后：", tem
            k = random.choice(base)  # 随机确定变异几次
            for j in range(k):
                 temp = self.mutanForString(tem, base)
                 # print "变异后的chang_object",temp
                 tem = temp
            for b in temp:
                result = result + b
            print "完成变异后的新数据", result
            old_solve[index_solve] = result
        elif varType[index_solve] == 'int':
            newdata = self.mutanForInt(change_object)
            old_solve[index_solve] = newdata
        elif varType[index_solve] == 'Boolean':
            if change_object == 1:
                change_object =0
            else:
                change_object = 1
            old_solve[index_solve]=change_object
        new_solve = old_solve
        print "new_solve", new_solve
        return new_solve
    def neighbor_solve(self,newneighbor):
        value = 0
        temp = list(newneighbor)
        index = [0,len(newneighbor)-1] #修改值的开头和结尾字符，产生临近解
        for i in index:
            solve_ascii = ord(newneighbor[i])
            if solve_ascii == 65 or solve_ascii == 97 or solve_ascii == 48:
                value = solve_ascii + 1
            elif solve_ascii == 122 or solve_ascii == 90 or solve_ascii == 57:
                value = solve_ascii - 1
            else:
                sflag = random.randint(0,1)
                if sflag == 0:
                    value = solve_ascii + 1
                else:
                    value = solve_ascii - 1
            c = chr(value)
            temp[i]=c
            newneighbor=''.join(temp)
        return newneighbor

        # 搜索算法2：爬山法
        # 首先将原解作为种子解，每次寻找这个种子相近的解，如果相近的解有代价更小的解，则把这个新的解作为种子
        # 依次循环进行，当循环到某种子附近的解都比该种子的代价大时，说明到达了局部极小值点，搜索结束
    def neighbor_solve2(self,newneighbor):
        date_list_small,date_list_big = self.GenerateRandomdate(newneighbor)
        r = random.randint(0,1)
        if r <0.5:
            newneighbor = random.choice(date_list_small)
        else:
            newneighbor = random.choice(date_list_big)
        return newneighbor

        # 搜索算法2：爬山法
        # 首先将原解作为种子解，每次寻找这个种子相近的解，如果相近的解有代价更小的解，则把这个新的解作为种子
        # 依次循环进行，当循环到某种子附近的解都比该种子的代价大时，说明到达了局部极小值点，搜索结束
    def HCOptimize(self):
        #初始解
        seed = self.testdata  #当前解
        originfit = self.p_fit_current
        count = 0
        searchFlag = 0
        while count < 500:
            print "第",count,"代"
            print "种子seed", len(seed), seed
            print "原始适应度", originfit

            neighbor_list = []
            fit = []
            # 循环改变解的每一个值产生一个临近解的列表 ,目前列表产生几个临近解合适？
            for ttt in range(4):
                neighbor = []
                for i in range(len(seed)):
                    newneighbor = self.neighbor_solve(seed[i])
                    neighbor.append(newneighbor)
                # print "neighbor", neighbor
                neighbor_list.append(neighbor)

            print "临近解集合"
            for vv in neighbor_list:
                print vv

            # 对所有的临近解计算代价，排序，得到代价最小的解

            for v in neighbor_list:
                time.sleep(2)
                # startTime = datetime.now()
                seq_to_script.runcase(self.tevent, self.pathT, v)
                # endTime = datetime.now()
                # usertime = endTime - startTime
                m1,covrage = cal_data_fit.array_spath()
                print "路径编号",self.objectPathIndex
                print "m1",m1
                f = m1[self.objectPathIndex]
                fit.append(f)
            newfit = min(fit)
            print "最小newfit",newfit
            newindex = fit.index(newfit)
            if newfit == 0.0: #如果最小fit值为0.0，则搜到数据，退出循环
                # seed = neighbor_list[newindex]
                searchFlag = 1
                break
            else:# 如果新的最小代价 > 原种子代价，则跳出循环
                if newfit > originfit:
                    break
            # 新的代价更小的临近解作为新的种子
            seed = neighbor_list[newindex]
            originfit = newfit
            count += 1

        return searchFlag,seed
if __name__ == '__main__':
    testdata = ['f83YY1', '9xdi5O', '74x02T', 'G4TR7B', 'OlvHct', '19oTXc', '2sEU26', 'ivL3x5', 'PnHzo6', 'z1Orq5', '57jK2Y', '8R2bO2']
    dormsol = HC("s", "s","s", testdata, "s",0.78)
    # dormsol.annealingoptimize(domain)
    # var = ['string','int','Boolean']
    # r = dormsol.Initial_solution(var)
    # # print r
    # # # s = dormsol.GenerateRandomString()
    # t = dormsol.interfer_fun(r,var)
    # print t
    dormsol.HCOptimize()

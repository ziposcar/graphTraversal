# -*-  coding: utf-8 -*-
import random
import math
import cal_data_fit
import seq_to_script
import recordFun
class SA:
    def __init__(self, varType , pathT, tevent,pathVarData,pathIndex):
        self.min = 0
        self.max = 8000
        self.varType = varType
        self.pathT = pathT
        self.tevent = tevent
        self.testdata = pathVarData
        self.objectPathIndex = pathIndex

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

    # 搜索算法4：模拟退火算法
    # 参数：T代表原始温度，cool代表冷却率，step代表每次选择临近解的变化范围
    # 原理：退火算法以一个问题的随机解开始，用一个变量表示温度，这一温度开始时非常高，而后逐步降低
    #      在每一次迭代期间，算啊会随机选中题解中的某个数字，然后朝某个方向变化。如果新的成本值更
    #      低，则新的题解将会变成当前题解，这与爬山法类似。不过，如果成本值更高的话，则新的题解仍
    #      有可能成为当前题解，这是避免局部极小值问题的一种尝试。
    # 注意：算法总会接受一个更优的解，而且在退火的开始阶段会接受较差的解，随着退火的不断进行，算法
    #      原来越不能接受较差的解，直到最后，它只能接受更优的解。
    # 算法接受较差解的概率 P = exp[-(highcost-lowcost)/temperature]
    def SAOptimize(self):
        T = 500.0
        cool = 0.98
        # 在原来测试数据值的基础上扰动产生新值
        # vec = self.Initial_solution(self.varType)
        C_Individual = self.Perturbation(self.testdata,self.varType)
        # 循环
        count = 0
        searchFlag = 0
        while T > 0.1:
            # 能量函数设计: 一个候选解的能量值 = approach_level + Normalized(distance) 能量值越小越逼近目标路径
            # 计算当前候选解产生的能量值和新的候选节产生的能量值
            seq_to_script.runcase(self.tevent, self.pathT, C_Individual)
            m1 = cal_data_fit.array_spath()
            power1 = m1[self.objectPathIndex]
            print "power1",power1
            if power1 == 0 or 0.0:
                searchFlag = 1
                break
            else:
                N_Individual = self.Perturbation(C_Individual, self.varType)  # 扰动产新解
                seq_to_script.runcase(self.tevent, self.pathT, N_Individual)
                m2,coverage = cal_data_fit.array_spath()
                power2 = m2[self.objectPathIndex]
                print "power2", power2
                if power2 == 0 or 0.0:
                    C_Individual = N_Individual
                    searchFlag = 1
                    break
                else:
                    # 判断新的解是否优于原始解 或者 算法将以一定概率接受较差的解
                    if power2 < power1 or random.random() < math.exp(-(power2 - power1) / T):
                        C_Individual = N_Individual
            T = T * cool  # 温度冷却
            # print "当前温度",T
            count += 1
        # recordFun.recordSAcount(self.objectPathIndex,count)
        return searchFlag,C_Individual
# 如果搜完没找到呢？置标识searchFlag ，searchFlag = 1搜到，=0，没搜索到
if __name__ == '__main__':
    dormsol = SA()
    # dormsol.annealingoptimize(domain)
    var = ['string','int','Boolean']
    r = dormsol.Initial_solution(var)
    # print r
    # # s = dormsol.GenerateRandomString()
    t = dormsol.interfer_fun(r,var)
    print t

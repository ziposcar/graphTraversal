# coding: utf-8
from __future__ import division
from Levenshtein import *
# distance(str1, str2) 编辑距离
# hamming(str1, str2) 海明距离
# ratio(str1, str2) 类编辑距离
# jaro(s1, s2) jaro距离
# jaro_winkler(s1, s2) jaro_winkler距离   the above function all can be called directly
import math
import os
import datetime
import redis
import shutil
import sensitive_path_info
from decimal import Decimal
import recordFun
K = 1
import config
file,file2,redis_path = config.getInstrumentFile()

r = redis.Redis(host="127.0.0.1", port=6379, db=0)

def deletefile():
    r.set(redis_path, "")


def hand_instru():
    result = []
    path_info = []
    path=[]
    branch_exe = []
    cond_data = []
    path_e = []
    lines = r.get(redis_path).split("\r\n")  # 读取全部内容
    for line in lines:
        line = line.strip("\n")
        if line != "*********" and line != "":
           result.append(line)
    # print result
    # print"changdu ", len(result)
    # for i in range(len(result)):
    #     print "原始信息",result[i]

    for i in range(0, len(result), 4):  # jump 2 step date
        # print "==========",i
        # print result[i]
        # print result[i+1]
        # print result[i+2]
        # print result[i+3]
        path_info.append(result[i])
        # print"path_info", path_info
        path_e.append(result[i+1])
        # print"pathlong", path_e,len(path_e)
        cond_data.append(result[i+2])
        branch_exe.append(result[i+3])
    upath_info = []
    ucond_data = []
    ubranch_exe = []
    for k in range(len(path_e)):
        if path_e[k] == "E":
            upath_info.append(path_info[k])
            ucond_data.append(cond_data[k])
            ubranch_exe.append(branch_exe[k])
    # print "路径信息" ,upath_info
    # print "分支信息",ucond_data
    # print "分支执行信息",ubranch_exe

    deletefile()
    bexcu_seq = []
    cinfo=[]
    pbdict = {}
    pcdict = {}
    for p in upath_info:
        if p not in path:
            path.append(p)
    for i in path:
        for j in range(len(upath_info)):
            if upath_info[j] == i:
                # bexcu_seq.append(ubranch_exe[j])   #old
                # cinfo.append(ucond_data[j])
                temp1 = ubranch_exe[j]      # new unpadta by 2018-04-02
                temp2 = ucond_data[j]
                if len(temp1)>=2:
                    temp2 = temp2.split("#")
                    temp2.pop()   # 去掉尾部空格
                    for k in range(len(temp2)):
                        bexcu_seq.append(temp1[k])
                        cinfo.append(temp2[k])
                else:
                    bexcu_seq.append(temp1)
                    cinfo.append(temp2)

        pbdict[i] = bexcu_seq
        pcdict[i] = cinfo
        bexcu_seq = []
        cinfo = []
    # print "路径信息",path
    # print "路径分支执行信息",pbdict
    # print "路径分支条件信息", pcdict
    return pbdict,pcdict


def hand_instru_webchess():
    result = []
    path_info = []
    path=[]
    branch_exe = []
    cond_data = []
    path_e = []
    lines = r.get(redis_path).split("\r\n")  # 读取全部内容
    f.close()
    for line in lines:
        line = line.strip("\n")
        if line != "*********" and line != "":
           result.append(line)
    # print result
    # print"changdu ", len(result)
    # for i in range(len(result)):
    #     print "原始信息",result[i]

    for i in range(0, len(result), 4):  # jump 2 step date
        # print "==========",i
        # print result[i]
        # print result[i+1]
        # print result[i+2]
        # print result[i+3]
        path_info.append(result[i])
        # print"path_info", path_info
        path_e.append(result[i+1])
        # print"pathlong", path_e,len(path_e)
        cond_data.append(result[i+2])
        branch_exe.append(result[i+3])
    upath_info = []
    ucond_data = []
    ubranch_exe = []
    for k in range(len(path_e)):
        if path_e[k] == "E":
            upath_info.append(path_info[k])
            ucond_data.append(cond_data[k])
            ubranch_exe.append(branch_exe[k])
    # print "路径信息" ,upath_info
    # print "分支信息",ucond_data
    # print "分支执行信息",ubranch_exe

    # deletefile(t_index)
    bexcu_seq = []
    cinfo=[]
    pbdict = {}
    pcdict = {}
    for p in upath_info:
        if p not in path:
            path.append(p)
    for i in path:
        for j in range(len(upath_info)):
            if upath_info[j] == i:
                # bexcu_seq.append(ubranch_exe[j])   #old
                # cinfo.append(ucond_data[j])
                temp1 = ubranch_exe[j]      # new unpadta by 2018-04-02
                temp2 = ucond_data[j]
                if len(temp1)>=2:
                    temp2 = temp2.split("#")
                    temp2.pop()   # 去掉尾部||空格
                    for k in range(len(temp2)):
                        bexcu_seq.append(temp1[k])
                        cinfo.append(temp2[k])
                else:
                    bexcu_seq.append(temp1)
                    cinfo.append(temp2)

        pbdict[i] = bexcu_seq
        pcdict[i] = cinfo
        bexcu_seq = []
        cinfo = []
    # print "路径信息",path
    # print "路径分支执行信息",pbdict
    # print "路径分支条件信息", pcdict
    return pbdict,pcdict



def judge(cond_data,branch_exe):  # 判断一条分支的分支距离
    # judge  branch_exe 1 or 0 , which 1 mean the corresponding branch has covered ,
    # otherwise not,then it need deal with Levenshtein distance
    temp = []
    op = ["<",">","<=",">=","==","!="]
    for i in range(0, len(branch_exe)):
        if branch_exe[i] == "0":  # 未执行的分支计算其分支距离
            str = cond_data[i]   # 提取对应的分支condition
            str = str.split("||")  # 由||将复杂分支切割为多个简单分支
            str.pop()
            # print"不满足条件的分支", str
            for val in str:  # 对多个简单分支依次计算分支的距离
                vall = val.split()
                # print "拆解条件",vall
                if len(vall) == 2 and vall[0] in op:  # 数据处理，E2为空时，会被上一步的val.split()消掉E2，so填补" "
                    vall.insert(0, " ")
                elif len(vall) == 2:
                    vall.append(" ")
                elif len(vall) == 1:
                    vall.insert(0," ")
                    vall.append(" ")
                # print "不满足条件的分支数据",vall  # val= ['hhh', '!=', ' '] 或 val=['1','5','8']
                # 这里根据op类型采用不同距离计算公式
                # 2018-3-21这里发现问题，根据op类型采用不同的距离计算公式没有问题，但是还需要更详尽的分类来计算
                # 如 hfdjhfdj != ""  这已经满足条件d应为0，但是直接用距离公式计算处理的分支距离却是d=8,需要改进
                if vall[1] == "==" : # 由op 确定变量为 string 型
                    d = distance(vall[0], vall[2])
                    temp.append(d)
                elif vall[1] == "!=" or vall[1] == "<>":
                    d = distance(vall[0], vall[2])
                    if d != 0:
                        temp.append(0)  #如果d不等于0，则这两个变量值不相等，已经满足！=，则其距离为0
                    else:
                        temp.append(1)  #如果d等于0，则这两个变量值相等，不满足条件！=，则只需任意变动一位即可达到目的，其距离为1
                elif vall[1] == "<" or vall[1] == "<=":  # 由op 确定变量为number 型
                    d = int(vall[0]) - int(vall[2]) + K    # val的元素在分割后变成了string型，需要转为int型，如：'1'--> 1

                    # d = distance(vall[0], vall[2])  #teacher
                    temp.append(d)
                elif vall[1] == ">" or vall[1] == ">=":  # 由op 确定变量为number 型
                    d = int(vall[2]) - int(vall[0]) + K
                    # print "vall[0]", vall[0]
                    # str1 = vall[0].strip("")
                    # print "vall[2]", vall[2]
                    # str2 = vall[2].strip("")
                    # print "vall[2]", str2
                    # d1 = datetime.datetime.strptime(str1, '%Y-%m-%d')
                    # d2 = datetime.datetime.strptime(str2, '%Y-%m-%d')
                    # d = d1 - d2
                    # d = distance(vall[0], vall[2])  #teacher
                    temp.append(d)
            break
    # print "子条件的分支距离",temp
    return temp


# obj_i=temp
# 复合分支中的子分支的分支距离
def rule_Tracy(obj_i):
    op = "&&"  # 想办法取得操作标识符&&，||之类的，让程序识别，目前直接定为&&，因为发现基本上复合分支上的逻辑词都是&&
    result_distance = 0
    if op =="and" or op == "&&":
        result_distance = sum(obj_i)
    elif op == "or" or op == "||":
        result_distance = min(obj_i)
    return result_distance


def judge_new(pcdict,pbdict):  # 判断每条路径的fitness
    # judge  branch_exe 1 or 0 , which 1 mean the corresponding branch has covered ,
    # otherwise not,then it need deal with Levenshtein distance
    path_fit = {}
    show_fit = {}
    for key in pbdict:
        # print "key",key
        branch_exe = pbdict[key]
        cond_data = pcdict[key]
        # print "分支执行情况", branch_exe
        # print "分支条件信息" , cond_data
        obj_i = judge(cond_data,branch_exe)  #子分支距离计算
        path_distance = rule_Tracy(obj_i) #一条路径的分支距离计算,# 根据复合分支的分支距离的计算结果确定
        count = 0
        for i in branch_exe:
            if i == "1":
                count = count + 1
            else:
                break
        # need to understand approch_level is Continuous branch or discontinuous ? answer：continue
        approch_level = len(branch_exe) - count

        # print "d",d
        temp = 1 - 1 / math.pow(1.01, path_distance)  # need Normalized
        # distance_level = Decimal(temp).quantize(Decimal('0.0000'))  # Keep 4 decimal places
        distance_level = temp
        # print "approch_level", approch_level
        # print "distance_level", distance_level
        fitness = approch_level + distance_level
        Fi = fitness / len(branch_exe) #schoomate   归一化有问题，后面再改

        path_fit[key] = Fi
        if Fi==0.0:
            show_fit[key] =Fi
    print " 该测试用例覆盖的路径fit", show_fit
    recordFun.recordCoverPath(path_fit)
    return path_fit

# 所有的测试用例对所有路径的覆盖情况可以构成一张二维表
#要得到一张这样的表，需要所有的测试用例都执行一遍，把每一个测试用例对所有路径的覆盖情况记录下来
#循环n = 测试用例个数 次，依次添加到表中，
# 一行就是一个测试用例对所有路径的覆盖情况，一列就是多个测试用例对同一条路径的覆盖情况

#array_spath 获取一个测试用例对所有路径的覆盖情况
def array_spath():
    pbdict, pcdict = hand_instru()  # schoolmate,faqforge
    # pbdict, pcdict = hand_instru_webchess() #webchess
    path_fit = judge_new(pcdict, pbdict)
    spath = sensitive_path_info.obtain_spath()
    m = sensitive_path_info.build_m()
    # print "m",m
    for key in path_fit:
        # print "path_fit_key",key
        index = spath.index(key)
        # print "index in spath"
        # print index
        m[index] = path_fit[key]
    t= m.count(0.0)
    covrage = t / len(m)
    print m,t," 个体覆盖率",covrage
    return m,covrage  #返回该个体对各条路径的覆盖情况matrix，及完全覆盖路径的覆盖率


if __name__=='__main__':

    # print cfitness()
    # hand_instru()
    # pbdict, pcdict = hand_instru()
    # path_fit = judge_new(pcdict,pbdict)
    # array_spath()
    # hand_info(c,b)
    # deletefile()
    # l = [2, 2, 2, 0.0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    #  0.0, 0.0, 2, 2, 2]
    # t = l.count(0.0)
    # c =t / len(l)
    # print t,c
    array_spath()
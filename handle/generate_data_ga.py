# encoding:utf-8
import obtain_efsm_info2
import random
import seq_to_script
import cal_data_fit
import datetime


def obtain_var_from_path(SM, currPathT):
    SM.repeatTranVarDict = {}
    SM.repeatTranFuncDict = {}  ####store repeat transition
    SM.currPathTranVarDict = {}
    pathVarType2 = []
    SM.copyPathInfo()
    for tran in currPathT:  # change the varibale name for the same T
        if currPathT.count(tran) > 1:
            SM.repeatTrans(currPathT)
            break
    SM.pathInputVar(currPathT)  # identify input variable in events relating to the current path
    SM.pathProProcess(currPathT)  # rewrite identical variables, ---stored in self.pathDefVar
    varname = SM.originalDef
    sp=["aperc","bperc","cperc","dperc","total"]  # teacher
    sp1 = ["bday",  "aday"]  # addressbook
    sp2 = [ "bmonth",  "amonth"]  # addressbook
    for num in varname:
        if num =="txtReload" or num in sp or num in sp1:
            pathVarType2.append('int')
        elif num == "duedate" or num == "assigneddate" or num == "gradedate" or num == "wasdate":
            pathVarType2.append('date')
        elif num in sp2:
            pathVarType2.append('month')
        elif num in sp1:
            pathVarType2.append('day')
        else:
            pathVarType2.append('string')
    return varname, pathVarType2

def GenerateRandomString():
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

def GenerateRandomInt():
    ret = random.choice(range(0,8000))
    return ret
def GenerateRandomdate():
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
        date_list.append(datestart.strftime('%Y-%m-%d'))
    # print(date_list)
    ret = random.choice(date_list)
    return ret

def GenerateRandomMonth():
    month = ["January","February","March","April","May","June","July","August",
             "September","October","November","December",]
    ret = random.choice(month)
    return ret


def GenerateRandomDay():
    ret = random.randint(1,31)
    return ret


def Initial_data(vartype):
    solve = []
    for num in vartype:
        if num == 'Boolean':
            data = random.randint(0, 1)
            solve.append(data)
        elif num == 'string':
            str = GenerateRandomString()
            solve.append(str)
        elif num == 'date':
            str = GenerateRandomdate()
            solve.append(str)
        elif num == 'day':
            str = GenerateRandomDay()
            solve.append(str)
        elif num == 'month':
            str = GenerateRandomMonth()
            solve.append(str)
        else:
            str1 = GenerateRandomInt()
            solve.append(str1)
    return solve


def testProcee(SM, currPathT):
    coverage = 0
    varname, pathVarType = obtain_var_from_path(SM, currPathT)  #获得序列上的变量名和变量类型
    test_fit =[]
    if len(SM.originalDef) > 0:  ##There exist input variables on the path
        vecdata = Initial_data(pathVarType)  #为变量产生数据
        print " 变量上的数据：",vecdata
        print " 执行当前序列:"
        seq_to_script.runcase(SM.TEvent, currPathT, vecdata) # 执行当前序列
        test_fit,coverage = cal_data_fit.array_spath()  # 获取对各条路径的覆盖情况 test_fit，及完全覆盖路径的覆盖率
        data = vecdata
    else:
        print"The path has no variables"
        data = [0]

    return data,test_fit,coverage


if __name__ == '__main__':
    # SM = obtain_efsm_info2.obtain_efsm()
    # SM.allPathNum()
    # print "%s has %s states and  %s transitions" % (SM.name, len(SM.stateList), len(SM.transitionList))
    # pathT = ['T3', 'T101', 'T102', 'T104']  #来自模型schoolmate_Vtest.txt
    # populationSize = 10
    # testProcee(SM,pathT,)
    GenerateRandomdate()

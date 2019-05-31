#encoding:utf-8
from __future__ import division # 必须放在文件首行
import sclexer
import random
# import testcase_seq.runcase
from random import choice
from datetime import datetime
import copy
# import handle.generate_seq_graph_traversal  #EFSM_handle 与它互相引用，会出错，具体怎么解决在想，
# 考虑通过第三方文件作为桥梁，或者，复制一份EFSM_handle，改名，generate_seq引用改名后的EFSM_handle的功能
import computer_fitness
import os
class SLIMException(Exception):
    """
    """

    def __init__(self, currState):
        """The string argument is the name of the current state."""
        self.state = currState

class State:
    """ The state of EFSM """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<State %s>" % self.name


###########################
class Transition:
    """ The transition of EFSM """

    def __init__(self, name, src=None, tgt=None, event=None, cond=None, action=None):
        self.name = name
        if src is not None:
            if isinstance(src, State):
                self.src = src
            else:
                print 'source must be a State type'
        if tgt is not None:
            if isinstance(tgt, State):
                self.tgt = tgt
            else:
                print 'target must be a State type'
        self.event = event
        self.cond = cond
        self.action = action

    def __repr__(self):
        return "<Transition %s %s %s %s %s %s>" % (self.name, self.src, self.tgt, self.event, self.cond, self.action)
        #       return "<Transition %s>" % self.name


###########################
class Path(list):
    """Path is a sequence of transitions, and T.tgt==successor(T).src"""
    def is_feasiable_ATM(self):
        """ filter infeasiable path in ATM model
        """
        conflictTran = {}
        conflictTran["T5"] = ["T11", "T16", "T20", "T22"]
        conflictTran["T6"] = ["T12", "T15", "T19", "T21"]
        tempPath = self[:]
        while tempPath:
            firstTran = tempPath[0]
            restTranList = tempPath[1:]
            if firstTran in conflictTran.keys():
                for tran in restTranList:
                    if tran in conflictTran[firstTran]:
                        return False
            tempPath = restTranList
        return True


class EFSM(object):
    """Instances of this class represent a EFSM machine.
    A machine is set of states and trsitions.
        """

    def __init__(self, name, transitionList=[]):
        self.name = name.split('/')[-1].split('.')[0]
        self.stateList = []
        self.transitionList = transitionList
        self.startStateList = []  # the start states list
        self.endStateList = []  # the end states list
        self.startTransitionList = []  # the start transition list
        self.endTransitionList = []  # the end transition list
        self.succDict = {}  # direct successor key: transition.name, value:transitionList
        self.tranSuccDict = {}  # transitive successors key: transition.name, value:transitionSet
        self.tranVarDict = {}  # key transition.name, value:dict
        # {eventVdef:vlist, condVuse:vlist, actionVdef:vlist, actionVuse,vlist}
        self.tranFuncDict = {}  # key transition.name, value:dict
        # {eventFunc:vlist, condFunc:vlist, actionFunc:vlist}
        self.transPathList = {}  # key:transition.name, value:Pathlist
        # more than 10 path list for a given transition
        self.pathDefVar = []  ### variables defined on current path with different names
        self.originalDefVar = []  ### variable defined on curent path, may with the same names
        self.pathVarValue = {}  ### key: variable on current path, value: genome value

        self.currPathTranVarDict = {}  # transition information in Current path copying from self.tranVarDict and self.tranfUNCdICT
        #   key transition.name, value:dict
        # {eventVdef:vlist, condVuse:vlist, actionVdef:vlist, actionVuse,vlist}
        self.currPathTranFuncDict = {}  # key transition.name, value:dict
        # {eventFunc:vlist, condFunc:vlist, actionFunc:vlist}
        self.pathTestGen = {}  ###  key: the length of ipath, value: test generation flag, 1=successful, 0=no successful
        self.repeatTranFlag = 0  ## there are no identical transitons on the path
        self.repeatTranVarDict = {}
        self.repeatTranFuncDict = {}  ####store repeat transition
        self.min = 0
        self.max = 8191
        self.condlist = {}
        self.TEvent = {}   ##store all transition's event for create test script


    def __repr__(self):
        return "<EFSM %s>" % self.name

    def state(self, name=None):
        if name == None:
            return self.stateList
        else:
            for state in self.stateList:
                if state.name == name:
                    return state
        print 'can not find %s in the state machine' % name


    def addState(self, newstate):
        """Add a state to the stateList.
                   """
        if isinstance(newstate, State):
            if newstate in self.stateList:
                print 'State %s is in the machine' % newstate.name
            else:
                self.stateList.append(newstate)


    def addTransition(self, newtransition):
        """Adds a transition to the transition list.
                    """
        if isinstance(newtransition, Transition):
            if newtransition in self.transitionList:
                print 'Transition %s is in the machine' % newtransition.name
            else:
                self.transitionList.append(newtransition)


    def initTransitionSuccessor(self):
        """ return a list of transitions that are
                    the surccessors of the given transition
                    """

        for currTransition in self.transitionList:
            self.succDict[currTransition.name] = \
                self.transitionSuccessor(currTransition)


    def transitionSuccessor(self, currTransition):
        """ return a list of transitions that are
                    the surccessors of the given transition
                    """
        return [item for item in self.transitionList \
                if item.src == currTransition.tgt]


    def findStartTransition(self):
        """ computer start transitions which source is START state
                    """

        templist = [item.name for item in self.transitionList \
                    if item.src.name == "START"]
        if templist:
            self.startTransitionList = templist[:]
        else:
            self.startTransitionList = []
            # print '\tstartTransitionList ',self.startTransitionList


    def findEndTransition(self):
        """ reuten a list of end transition which target is Exit
                    """
        templist = [item.name for item in self.transitionList
                    if item.tgt.name == "Exit" or item.tgt.name == "EXIT"]
        # if item.tgt.name == "CLOSED" or item.tgt.name == "CLOSED" ]
        if templist:
            self.endTransitionList = templist[:]
        else:
            self.endTransitionList = []
        # print '\tendTransitionList ',self.endTransitionList


    ################### find all path for a given transition###############
    def vDefUseList(self, currTransition):
        """compute vDef and vUse list for currTransition
        """
        tranVarDict = {}
        tranFuncDict = {}
        # compute event Vdef
        statements = currTransition.event
        vlist = []
        eventlist = []
        ss = statements.split(";")
        # 这里只取分割后的第一部分就好，不用for，并考虑stat为空不为空的情况即有无输入参数的情况。
        sclexer.lex.input(ss[0])
        while 1:
            tok = sclexer.lex.token()
            if not tok:
                break
            else:
                if tok.type == 'ID':
                    vlist.append(tok.value)
                elif tok.type == 'LPAREN':
                    vlist.pop()
        tranVarDict['eventVdef'] = vlist[:]  #
        eventlist.append(statements)
        tranFuncDict['eventFunc'] = eventlist[:]
        # print"----",currTransition.name
        # print "eventVdef:", vlist

        # compute cond Vuse
        statements = currTransition.cond
        vlist = []
        condlist = []
        for stat in statements.split(";"):
            sclexer.lex.input(stat)
            while 1:
                tok = sclexer.lex.token()
                if not tok:
                    break
                else:
                    if tok.type == 'ID':
                        vlist.append(tok.value)
        condlist.append(statements)
        tranFuncDict['condFunc'] = condlist[:]
        tranVarDict['condVuse'] = vlist[:]
        # print "condVuse:",vlist

        # compute action Vdef and Vuse
        statements = currTransition.action
        vdef = []
        vuse = []
        actionlist = []
        for stat in statements.split(";"):
            vlist = []
            sclexer.lex.input(stat)
            while 1:
                tok = sclexer.lex.token()
                if not tok:
                    break
                else:
                    if tok.type == 'ID':
                        vlist.append(tok.value)
                    elif tok.type == 'LPAREN':
                        vlist.pop()
                    elif tok.type == 'EQUALS':
                        vdef.extend(vlist[:])
                        actionlist.append(stat)
                        vlist = []
            vuse.extend(vlist)
            tranFuncDict['actionFunc'] = actionlist[:]
        tranVarDict['actionVdef'] = vdef
        tranVarDict['actionVuse'] = vuse
        self.tranVarDict[currTransition.name] = tranVarDict
        self.tranFuncDict[currTransition.name] = tranFuncDict
        ###store all transition's event to self.TEvent for create test script
        self.TEvent[currTransition.name] = currTransition.event
        # print "actionVdef:",vdef
        # print "actionVuse:",vuse

    def condition_handle(self, currTransion):
        cond = currTransion.cond
        self.condlist[currTransion.name] = cond
        # print "condlist: ", self.condlist



    def initTranVarFuncList(self):
        for transition in self.transitionList:
            # print '%s variables:'%transition.name
            self.vDefUseList(transition)
            self.condition_handle(transition)
        # print '===================================================='

    def allPathNum(self):
        """initiate and find all path
                    """

        self.findStartTransition()
        self.findEndTransition()
        self.initTransitionSuccessor()
        self.initTranVarFuncList()




    def repeatTrans(self, curPath):
        """
        rename identical transition on a path
        """

        for tran in curPath:
            if curPath.count(tran) > 1:
                for i in range(curPath.count(tran) - 1):
                    new = tran + '_' + repr(i + 1)
                    tranVar = {}
                    tranFun = {}
                    tranVar = copy.deepcopy(self.currPathTranVarDict[tran])
                    tranFun = copy.deepcopy(self.currPathTranFuncDict[tran])
                    eventVdef = []
                    eventVdef.extend(tranVar['eventVdef'])
                    tempEventFunc = []
                    tempEventFunc.extend(tranFun['eventFunc'])
                    for tempevent in tempEventFunc:
                        eventstr = tempevent
                        for var in tranVar['eventVdef']:
                            newvar = var + '_' + new
                            rindex = eventstr.rfind(var)
                            if rindex >= 0:
                                eventstr = eventstr[0:rindex] + newvar + eventstr[rindex + len(var):]
                        tempEventFunc.append(eventstr)
                        tempEventFunc.remove(tempevent)
                    for var in tranVar['eventVdef']:
                        newvar = var + '_' + new
                        eventVdef.append(newvar)
                        eventVdef.remove(var)
                    tranVar['eventVdef'] = eventVdef
                    tranFun['eventFunc'] = tempEventFunc
                    self.repeatTranVarDict[new] = tranVar
                    self.repeatTranFuncDict[new] = tranFun

    def pathProProcess(self, currPath):
        """  process path in advance
            rename variable name for the same event
            rewrite relevant eventFunc, eventVdef,
            hold unchanging on condDefVar, condFunc, actionDefVar and actionFunc
        """

        oldDefVar = []
        self.pathDefVar = []
        oldDefVar.extend(self.originalDef)
        for old in oldDefVar:
            if oldDefVar.count(old) > 1:
                for i in range(oldDefVar.count(old) - 1):
                    new = old + repr(i)
                    oldDefVar.append(new)
                    oldDefVar.remove(old)
                    for vtran, vdict in self.currPathTranVarDict.iteritems():
                        if vtran in currPath:
                            for ftran, fdict in self.currPathTranFuncDict.iteritems():
                                if ftran == vtran:
                                    flag = 0
                                    if old in vdict['eventVdef']:
                                        tempEventVar = vdict['eventVdef']
                                        tempEventVar.append(new)
                                        tempEventVar.remove(old)
                                        vdict['eventVdef'] = tempEventVar
                                        for tempevent in fdict['eventFunc']:
                                            tempEventFunc = fdict['eventFunc']
                                            rindex = tempevent.rfind(old)
                                            if rindex >= 0:
                                                eventstr = tempevent[0:rindex] + new + tempevent[rindex + len(old):]
                                                tempEventFunc.append(eventstr)
                                                tempEventFunc.remove(tempevent)
                                                flag = 1
                                                break  ## break for tempevent loop
                                    break  ## break ftran,fdict loop
                            if (flag == 1): break
        self.pathDefVar.extend(oldDefVar)



    def pathInputVar(self, currPath):

        self.originalDef = []  ## variables defined on the path's events
        tranDealFlag = {}

        for tran in currPath:
            tranDealFlag[tran] = 0  ### deaf flag =0
        i = 0
        while (i < len(currPath)):
            currTrans = currPath[i]
            if tranDealFlag[currTrans] == 0:
                for vtran, vdict in self.currPathTranVarDict.iteritems():
                    if vtran == currTrans:
                        tempvdict = []
                        #####deal with event variables######
                        tempvdict.extend(vdict['eventVdef'])
                        while tempvdict != []:
                            self.originalDef.append(tempvdict.pop(0))
                        # tranDealFlag[currTrans] = 1
                        break
            i = i + 1
        for vtran, vdict in self.repeatTranVarDict.iteritems():
            tempvdict = []
            tempvdict.extend(vdict['eventVdef'])
            while tempvdict != []:
                self.originalDef.append(tempvdict.pop(0))
        # print " 当前迁移上原始定义变量originaDef", self.originalDef

    def copyPathInfo(self):
        """
        copy path information into current Path Dictionary
        """

        self.currPathTranVarDict = copy.deepcopy(self.tranVarDict)
        self.currPathTranFuncDict = copy.deepcopy(self.tranFuncDict)

    def GenerateRandomString(self):
        '''xss = ["<script>/*", "*/alert(1)/*", "%c1;alert(/xss/);//", "><!--", "hash", "src", "<a href=''>xss",
               "<a onclick=alert(18)>M", "<scr<script>ipt>", "</scr<script>ipt>", "*/</script>", "</a>", "<h1>xss<h1>",
               "<a href="">xss</a>", "alert(document.cookie)", "<ScRipt>ALeRt(1)</sCRipT>","'or 1=1"]
        x = range(97, 123)  # 97-122 a-z, 65-90 A-Z, 48-57 0-9
        basechars = [chr(i) for i in x]
        ret = ''
        y = random.choice(xss)
        listd = [0, 2]
        long = random.choice(listd)
        for i in range(long):
            ret += random.choice(basechars)
        ret = y + ret  '''

        long = random.randint(6, 15)
        x = range(97, 123)  # 97-122 a-z, 65-90 A-Z, 48-57 0-9
        basechars = [chr(i) for i in x]
        ret = ''
        for i in range(long):
            ret += random.choice(basechars)
        return ret

    def GenerateRandomInt(self):
        x = range(97, 123)  # 97-122 a-z, 65-90 A-Z, 48-57 0-9
        basechars = [chr(i) for i in x]
        ret = ''
        # long = random.randint(6, 15)
        long = 6
        for i in range(long):
            ret += random.choice(basechars)
        return ret

    def generatedata(self, vartype):
        var = []
        for num in vartype:
            if num == 'Boolean':
                data = random.randint(self.min, 1)
                var.append(data)
            elif num == 'string':
                str = self.GenerateRandomString()
                var.append(str)
            else:
                str1 = self.GenerateRandomInt()
                var.append(str1)
        return var

    def funt(self, str,varname, d, listt, datalist):
        data ={}
        # datalist = []
        str = str.strip()
        str = str.strip('(')
        str = str.strip(')')
        operList = ["==", "!=", "<=", ">=", "<", ">","="]
        for oper in operList:
            if oper in str:
                list = str.split(oper)
                left = list[0]
                left = left.strip()
                right = list[1]
                right = right.strip() # delete "" false
                right = right.strip('"')
                if left in varname:  # 确保op左边的是输入变量,排除condition上有而self.originalDef中没有的，即不是输入入变量
                    listt.append(left)
                    if right in varname:  # 确定op右边边的是输入变量还是“”，数字，字符串，如果password ==password2这种的就要比较左右变量产生的值
                        listt.append(right)
                        if oper == "==" or oper == "=":
                            if d[0] != d[1]:
                                d[0] = d[1]
                                data[left] = d[0]
                                data[right] = d[0]
                                datalist.append(d[0])
                                datalist.append(d[0])
                                d.pop(0)
                                d.pop(0)
                                break
                        elif oper == "!=":
                            if d[0] != d[1]:
                                data[left] = d[0]
                                data[right] = d[1]
                                datalist.append(d[0])
                                datalist.append(d[1])
                                d.pop(0)
                                d.pop(0)
                                break
                        elif oper == "<=":
                            if d[0] <= d[1]:
                                data[left] = d[0]
                                data[right] = d[1]
                                datalist.append(d[0])
                                datalist.append(d[1])
                                d.pop(0)
                                d.pop(0)
                                break
                            else:
                                tt = random.randint(self.min, d[1])
                                data[left] = tt
                                data[right] = d[1]
                                datalist.append(tt)
                                datalist.append(d[1])
                                d.pop(0)
                                d.pop(0)
                                break
                        elif oper == ">=":
                            if d[0] >= d[1]:
                                data[left] = d[0]
                                data[right] = d[1]
                                datalist.append(d[0])
                                datalist.append(d[1])
                                d.pop(0)
                                d.pop(0)
                                break
                            else:
                                tt = random.randint(d[1], self.max)
                                data[left] = tt
                                data[right] = d[1]
                                datalist.append(tt)
                                datalist.append(d[1])
                                d.pop(0)
                                d.pop(0)
                                break
                        elif oper == "<":
                            if d[0] < d[1]:
                                data[left] = d[0]
                                data[right] = d[1]
                                datalist.append(d[0])
                                datalist.append(d[1])
                                d.pop(0)
                                d.pop(0)
                                break
                            else:
                                tt = random.randint(self.min, d[1] - 1)
                                data[left] = tt
                                data[right] = d[1]
                                datalist.append(tt)
                                datalist.append(d[1])
                                d.pop(0)
                                d.pop(0)
                                break
                        elif oper == ">":
                            if d[0] > d[1]:
                                data[left] = d[0]
                                data[right] = d[1]
                                datalist.append(d[0])
                                datalist.append(d[1])
                                d.pop(0)
                                d.pop(0)
                                break
                            else:
                                tt = random.randint(d[1] + 1, self.max)
                                data[left] = tt
                                data[right] = d[1]
                                datalist.append(tt)
                                datalist.append(d[1])
                                d.pop(0)
                                d.pop(0)
                                break
                    else:   # 如果password =="",123,"string"这种的就要比较左变量和该常量的值是否符合条件
                        if oper == "==" or oper == "=":
                            if d[0] != right:
                                data[left] = right
                                datalist.append(right)
                                d.pop(0)
                                break
                        elif oper == "!=":
                            if d[0] != right:
                                data[left] = d[0]
                                datalist.append(d[0])
                                d.pop(0)
                                break
                        elif oper == "<=":
                            if d[0] <= right:
                                data[left] = d[0]
                                datalist.append(d[0])
                                d.pop(0)
                                break
                            else:
                                dd = random.randint(self.min, right)
                                data[left] = dd
                                datalist.append(dd)
                                d.pop(0)
                        elif oper == ">=":
                            if d[0] >= right:
                                data[left] = d[0]
                                d.pop(0)
                                break
                            else:
                                ff = random.randint(right, self.max)
                                data[left] = ff
                                datalist.append(ff)
                                d.pop(0)

                        elif oper == "<":
                            if d[0] < right:
                                data[left] = d[0]
                                datalist.append(d[0])
                                d.pop(0)

                                break
                            else:
                                dd = random.randint(self.min, right - 1)
                                data[left] = dd
                                datalist.append(dd)
                                d.pop(0)

                        elif oper == ">":
                            if d[0] > right:
                                data[left] = d[0]
                                datalist.append(d[0])
                                d.pop(0)

                                break
                            else:
                                ff = random.randint(right + 1, self.max)
                                data[left] = ff
                                datalist.append(ff)
                                d.pop(0)
        return datalist, listt

    def Constraint_handle(self, currPath, varname, d):
        currpathcond  = []
        listt = []
        varlist = []
        datalist = []
        datalists = []
        generatedate =[]
        condlist = []
        for T in currPath:
            for key in self.condlist:
                if T == key:
                    currpathcond.append(self.condlist[key])  # 不用字典用列表，是为了有序，按路径迁移的顺序摆出条件
        # print "当前路径上的约束条件集合1:", currpathcond
        for value in currpathcond:
            if value != '':
                condlist.append(value)
        print "当前路径上的约束条件集合2:", condlist
        for v in condlist:
            if '&' in v:
                list = v.split('&')
                for str in list:
                    datalists, varlist = self.funt(str,varname, d, listt, datalist)
            elif '||' in v:
                list = v.split('||')
                for str in list:
                    datalists, varlist = self.funt(str,varname, d, listt,  datalist)
            else:
                str1 = v
                datalists, varlist = self.funt(str1, varname, d,listt,  datalist)
        return varlist, datalists  # varlist 是变量顺序，generatedata 是对应的数据

    def testdate_unrelate(self, currPath):
        special_var = ['type']
        s_var = ['Admin', 'Teacher', 'Substitute', 'Student', 'Parent']
        s = []
        ss = []
        self.repeatTranVarDict = {}
        self.repeatTranFuncDict = {}  ####store repeat transition
        self.currPathTranVarDict = {}
        pathVarType2 = []
        self.copyPathInfo()
        for tran in currPath:  # change the varibale name for the same T
            if currPath.count(tran) > 1:
                self.repeatTrans(currPath)
                break
        self.pathInputVar(currPath)  # identify input variable in events relating to the current path
        self.pathProProcess(currPath)  # rewrite identical variables, ---stored in self.pathDefVar
        # print"重命名当前路径上的定义变量名pathDefVar", self.pathDefVar
        # print "当前路径上的变量类型pathVarType :", pathVarType
        varname = self.originalDef

        # ##############特殊变量处理 如type
        for var in varname:
            if var in special_var:
                ss.append(var)
                s.append(choice(s_var))
                varname.remove(var)
        varname2 = varname
        print '****特殊变量产生', ss, s
        print '删掉特殊变量的变量列表', varname2

        for num in varname2:
            pathVarType2.append('string')

        if len(self.pathDefVar) > 0:
            d = self.generatedata(pathVarType2)
            tt, ff = self.Constraint_handle(currPath, varname2, d)
            tt.extend(ss)
            ff.extend(s)
            print '变量顺序: ', tt
            print '对应数据: ', ff
            varDate = zip(tt,ff)
            print "****满足约束条件的数据", varDate
            return varDate

    def unpdata_pop(self,oldFit,newFit,old_pop,new_pop,populationSzie):
        o = []
        n = []
        all_fit = []
        all_pop = []
        newpop = []
        for i in range(len(oldFit)):
            o.append(oldFit[i])
        for i in range(len(newFit)):
            n.append(newFit[i])
        all_fit = o + n
        all_pop = old_pop + new_pop
        for i in range(populationSzie):
            max_value = max(all_fit)
            max_index = all_fit.index(max_value)
            newpop.append(all_pop[max_index])
            all_fit[max_index] = (-100)  # 避免选过的最优个体再次被选
        return newpop




if __name__ == '__main__':
    print "efsm part"
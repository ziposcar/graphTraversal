# encoding:utf-8
from __future__ import division  # 必须放在文件首行
import sclexer
import random
import testcase_seq.runcase
from random import choice
from datetime import datetime
import copy
import handle.generate_seq_graph_traversal
import computer_fitness
import os


class SLIMException(Exception):
    """
    """

    def __init__(self, currState):
        """The string argument is the name of the current state."""
        self.state = currState


###############################
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


class GA:
    """
    simple Genetic Algorithms
    """

    def __init__(self, populationSize, inputVarNum, crossoverRate=0.7, mutationRate=0.08, maxGeneration=200):

        self.crossoverRate = crossoverRate
        self.mutationRate = mutationRate
        self.populationSize = populationSize
        self.genomeLen = inputVarNum
        self.generation = 0
        self.genomes = []
        self.bestFitness = {}  ##key: index, value: bestFitnessScore
        self.worstFitness = {}
        #    self.totalFitnessScore = 0
        self.maxGeneration = maxGeneration
        #    self.max=100  ### cruiseControl: max=100
        self.max = 8191  ### Cashier, ATM: max=10000,
        #    self.max=500   ### fulePump
        self.min = 0

    def GenerateRandomString(self):
        '''xss = ["<script>/*", "*/alert(1)/*", "%c1;alert(/xss/);//", "><!--", "hash", "src", "<a href=''>xss",
               "<a onclick=alert(18)>M","<scr<script>ipt>","</scr<script>ipt>","*/</script>","</a>","<h1>xss<h1>",
               "<a href="">xss</a>","alert(document.cookie)","<ScRipt>ALeRt(1)</sCRipT>"]
        x = range(97, 123)  # 97-122 a-z, 65-90 A-Z, 48-57 0-9
        basechars = [chr(i) for i in x]
        ret = ''
        # long = random.randint(6, 15)
        y = random.choice(xss)
        listd =[0,2]
        long = random.choice(listd)
        for i in range(long):
            ret += random.choice(basechars)
        ret = y+ret '''
        long = random.randint(6, 15)
        x = range(97, 123)  # 97-122 a-z, 65-90 A-Z, 48-57 0-9
        basechars = [chr(i) for i in x]
        ret = ''
        for i in range(long):
            ret += random.choice(basechars)
        return ret

    def GenerateRandomInt(self):
        x = range(48, 58)
        basechars = [chr(i) for i in x]
        ret = ''
        # long = random.randint(6, 18)
        long = 6
        for i in range(long):
            ret += random.choice(basechars)
        return ret

    def genome(self, vartype):
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

    def creatStartPopulation(self, varType):
        self.genomes = []
        gen = []
        for i in range(self.populationSize):
            gen = self.genome(varType)
            self.genomes.append(gen)
        return self.genomes

    def fitnessScore(self, geneFitness):
        """ compute normalised fitness
             compute the best and worst fitness
        """

        sumFitness = 0
        normFit = []

        for i, value in geneFitness.iteritems():
            sumFitness = sumFitness + value

        for i, value in geneFitness.iteritems():
            tempScore = value / sumFitness
            normFit.append(tempScore)
        return normFit

    def accumFitness(self, normFit):
        """ compute the accumulative normalised fitness
        """

        accum = 0
        accumFit = []

        for i in range(self.populationSize):
            accum = accum + normFit[i]
            accumFit.append(accum)
        return accumFit

    def selectionGA(self, accumFit):
        """
            selecting genomes into the next generation
        """

        selectedGene = []

        for i in range(self.populationSize):
            while (len(selectedGene) < i + 1):
                rank = random.uniform(0, 1)  # 0~1 random number
                for j in range(len(accumFit)):
                    if rank < accumFit[j]:
                        selectedGene.append(self.genomes[j])
                        if len(selectedGene) == self.populationSize:
                            break
        return selectedGene

    def crossSingleGA(self, selectedGene):
        """ corss operation in GA
        """
        crossedGene = []

        for i in range(0, self.populationSize, 2):
            mumGene = selectedGene[i]
            dadGene = selectedGene[i + 1]
            baby1Gene = []
            baby2Gene = []
            rank = random.uniform(0, 1)
            if rank <= self.crossoverRate:
                crossPoint = random.randint(0, self.genomeLen - 1)
                for j in range(crossPoint):
                    baby1Gene.append(mumGene[j])
                    baby2Gene.append(dadGene[j])
                for j in range(crossPoint, self.genomeLen):
                    baby1Gene.append(dadGene[j])
                    baby2Gene.append(mumGene[j])
                crossedGene.append(baby1Gene)
                crossedGene.append(baby2Gene)
            else:
                crossedGene.append(mumGene)
                crossedGene.append(dadGene)
        return crossedGene

    def crossAddSubGA(self, selectedGene):
        """ corss operation in GA
        """
        crossedGene = []

        for i in range(0, self.populationSize, 2):
            mumGene = selectedGene[i]
            dadGene = selectedGene[i + 1]
            baby1Gene = []
            baby2Gene = []
            rank = random.uniform(0, 1)
            if rank <= self.crossoverRate:
                for j in range(self.genomeLen):
                    tempGene = abs(int(0.05 * (mumGene[j] - dadGene[j])) + mumGene[j])
                    baby1Gene.append(tempGene)
                    tempGene = abs(int(0.05 * (dadGene[j] - mumGene[j])) + dadGene[j])
                    baby2Gene.append(tempGene)
                crossedGene.append(baby1Gene)
                crossedGene.append(baby2Gene)
            else:
                crossedGene.append(mumGene)
                crossedGene.append(dadGene)
        return crossedGene

    def mutateGA(self, crossGene, vartype):
        """ mutate operation in GA
        """
        mutatedGene = []

        for i in range(self.populationSize):
            mutation = crossGene[i]  # 第i个个体进行变异,mutation = [a,b,c,d]包含4个变量
            rank = random.uniform(0, 1)
            if rank < self.mutationRate:
                mutationPoint = random.randint(0, self.genomeLen - 1)  # 变异点确定
                for i in range(len(vartype)):
                    if i == mutationPoint and vartype[i] == 'Boolean':
                        mutation[mutationPoint] = random.randint(0, 1)  # 该个体的第mutationPoint位基因根据变量类型进行变异
                        break
                    elif i == mutationPoint and vartype[i] == 'string':
                        mutation[mutationPoint] = self.GenerateRandomString()
                        break
                    elif i == mutationPoint and vartype[i] == 'int':
                        mutation[mutationPoint] = self.GenerateRandomInt()
                        break
            mutatedGene.append(mutation)
        return mutatedGene

    def GeneticAlgorithm(self, genomeFitness, genome, varType):

        """ Genetic algorithm
        """
        self.genomes = genome
        normFitness = self.fitnessScore(genomeFitness)
        accumFitness = self.accumFitness(normFitness)
        selectedGenome = self.selectionGA(accumFitness)
        crossedGenome = self.crossSingleGA(selectedGenome)
        mutatedGenome = self.mutateGA(crossedGenome, varType)
        return mutatedGenome

    def bestWorstFit(self, geneFitness):

        bestFitnessScore = 1
        worstFitnessScore = 0
        self.bestFitness = {}  ##key: index, value: bestFitnessScore
        self.worstFitness = {}
        bestIndex = 0
        worstIndex = 0
        sumFitness = 0

        for i, value in geneFitness.iteritems():
            sumFitness = sumFitness + value

        for i, value in geneFitness.iteritems():
            tempScore = value / sumFitness
            if tempScore < bestFitnessScore:  ## the smaller the better
                bestFitnessScore = tempScore
                bestIndex = i
            if tempScore > worstFitnessScore:
                worstFitnessScore = tempScore
                worstIndex = i
        self.bestFitness[bestIndex] = bestFitnessScore
        self.worstFitness[worstIndex] = worstFitnessScore

    def elistSurvive(self, oldFitness, mutatedFitness, mutatedGenome):
        """ worst genome from parent is overwrited by best genome from offspring
        """

        self.bestWorstFit(oldFitness)
        parentWorstFitness = self.worstFitness
        self.bestWorstFit(mutatedFitness)

        for i in parentWorstFitness.keys():
            for j in self.bestFitness.keys():
                self.genomes[i] = mutatedGenome[j]
        return self.genomes

    def basicSurvive(self, oldFitness, mutatedFitness, mutatedGenomes, surviveRate=0.8):
        """ worst genome from parent is overwrited by best genome from offspring
        """
        oldGene = []
        mutatedGene = []
        oldIndex = 0
        nutatedIndex = 0

        for i, value in oldFitness.iteritems():
            oldFitness[i] = 1 / value
        oldNormFitness = self.fitnessScore(oldFitness)
        oldAccumFitness = self.accumFitness(oldNormFitness)
        mutatedNormFitness = self.fitnessScore(mutatedFitness)
        mutatedAccumFitness = self.accumFitness(mutatedNormFitness)

        for i in range(self.populationSize):
            oldFlag = 0
            mutatedFlag = 0
            rank = random.uniform(0, 1)
            if rank <= surviveRate:
                rank = random.uniform(0, 1)
                for j in range(self.populationSize):
                    if rank <= oldAccumFitness[j]:
                        oldIndex = j
                        oldFlag = 1
                        break
                for j in range(self.populationSize):
                    if rank <= mutatedAccumFitness[j]:
                        mutatedIndex = j
                        mutatedFlag = 1
                        break
            if (oldFlag == 1) and (mutatedFlag == 1):
                self.genomes[oldIndex] = mutatedGenomes[mutatedIndex]
        return self.genomes


class EFSM:
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
        templist = [item.name for item in self.transitionList \
                    if item.tgt.name == "Exit" or item.tgt.name == "EXIT"]
        # if item.tgt.name == "CLOSED" or item.tgt.name == "CLOSED" ]
        if templist:
            self.endTransitionList = templist[:]
        else:
            self.endTransitionList = []
            # print '\tendTransitionList ',self.endTransitionList

    def pathAppend(self, currPath, succList):
        """return path list [path1, path2,...]

                    if item in succList does not show more than two times,
                    append it to rList
                    [a, b] and [c, d] will return [[a,b,c],[a,b,d]]
                    [a,b,c,b,c] and [b,d] will return [[a,b,c,b,c,d]]
                    If there is a self loop, the self loop is considered once
                    """
        newList = []
        for item in succList:
            if (currPath.count(item.name) < 1):
                newList.append(Path(currPath + [item.name]))
                # print 'yes'  #for test
        return newList

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
        for stat in statements.split(";"):
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
        tranVarDict['eventVdef'] = vlist[:]  #
        eventlist.append(statements)
        tranFuncDict['eventFunc'] = eventlist[:]
        print "---eventVdef:", vlist

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
        print "condVuse:", vlist

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
        print "actionVdef:", vdef
        print "actionVuse:", vuse

    def condition_handle(self, currTransion):
        vlist = []
        cond = currTransion.cond
        self.condlist[currTransion.name] = cond
        # print "condlist: ", self.condlist

    def initTranVarFuncList(self):
        for transition in self.transitionList:
            #    print '%s variables:'%transition.name
            self.vDefUseList(transition)
            self.condition_handle(transition)
        print '===================================================='

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
                        tranDealFlag[currTrans] = 1
                        break
            i = i + 1
        for vtran, vdict in self.repeatTranVarDict.iteritems():
            tempvdict = []
            tempvdict.extend(vdict['eventVdef'])
            while tempvdict != []:
                self.originalDef.append(tempvdict.pop(0))
        print "当前迁移上原始定义变量originaDef", self.originalDef

    def copyPathInfo(self):
        """
        copy path information into current Path Dictionary
        """

        self.currPathTranVarDict = copy.deepcopy(self.tranVarDict)
        self.currPathTranFuncDict = copy.deepcopy(self.tranFuncDict)

    ################### generate date for a given seq ###############
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

    def funt(self, str, varname, d, listt, datalist):
        data = {}
        # datalist = []
        str = str.strip()
        str = str.strip('(')
        str = str.strip(')')
        operList = ["==", "!=", "<=", ">=", "<", ">", "="]
        for oper in operList:
            if oper in str:
                list = str.split(oper)
                left = list[0]
                left = left.strip()
                right = list[1]
                right = right.strip()  # delete "" false
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
                    else:  # 如果password =="",123,"string"这种的就要比较左变量和该常量的值是否符合条件
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
        currpathcond = []
        listt = []
        varlist = []
        datalist = []
        datalists = []
        generatedate = []
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
                    datalists, varlist = self.funt(str, varname, d, listt, datalist)
            elif '||' in v:
                list = v.split('||')
                for str in list:
                    datalists, varlist = self.funt(str, varname, d, listt, datalist)
            else:
                str1 = v
                datalists, varlist = self.funt(str1, varname, d, listt, datalist)
        return varlist, datalists  # varlist 是变量顺序，generatedata 是对应的数据

    def deletefile(self):
        file = 'D:/wamp_php/wamp/www/schoolmate2/muser_result.txt'
        if os.path.exists(file):
            os.remove(file)
        else:
            print 'no such file:%s' % file

    def obtainIndividualFitness(self, currPathT, invidual, varname, populationSize, unTvardata):
        targetfit = {}
        invidualFit = {}
        self.pathVarValue = {}  ## key: variables on the path, value: corresponding value
        for i in range(populationSize):
            for var, val in zip(varname, invidual[i]):
                self.pathVarValue[var] = val
            # ##########这里开始考虑把所有数值传入测试用例中，约束部分数值unTvardata一直不变，变得是GA部分的相关迁移上的变量，要考虑这个
            testcase_seq.runcase.runtestcase(unTvardata, invidual[i])
            # 成功传入数据到测试用例，且执行成功，下面该插桩获取执行信息计算fiteness

            excu = computer_fitness.handle_txt()
            target = computer_fitness.handle_target()
            fitness = computer_fitness.fit_individuality(excu, target)
            fit = computer_fitness.target_fit(target)
            invidualFit[i] = fitness
            targetfit[i] = fit
            self.deletefile()
            # if fitness == fit:  ##  the current path is executed
            #     invidualFit[i] = fit
            #     self.deletefile()
            #     break
            # else:
            #     invidualFit[i] = round(1 / fitness, 4) # 保留4位小数
            #     # invidualFit[i] = 1 / fitness  # 结果为0，1除fitness
            #     self.deletefile()
        print"invidualFit", invidualFit
        return invidualFit, targetfit

    def elite_population(self, Fit, oldtarget, population):
        elite = []
        for i in range(len(Fit)):
            if Fit[i] == oldtarget[i]:
                elite.append(population[i])
        return elite

    def unpdata_pop(self, oldFit, newFit, old_pop, new_pop, populationSzie):
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
            varDate = zip(tt, ff)
            print "****满足约束条件的数据", varDate
            return varDate

    def testdate_relate(self, currPathT, unTvardata):
        print '****GA产生'
        populationSize = 10
        self.repeatTranVarDict = {}
        self.repeatTranFuncDict = {}  ####store repeat transition
        self.currPathTranVarDict = {}
        pathVarType2 = []
        self.copyPathInfo()
        for tran in currPathT:  # change the varibale name for the same T
            if currPathT.count(tran) > 1:
                self.repeatTrans(currPathT)
                break
        self.pathInputVar(currPathT)  # identify input variable in events relating to the current path
        self.pathProProcess(currPathT)  # rewrite identical variables, ---stored in self.pathDefVar
        varname = self.originalDef
        for num in varname:
            pathVarType2.append('string')

        if len(self.originalDef) > 0:  ##There exist input variables on the path
            for repeat in range(10):
                gaSample = GA(populationSize, len(varname))
                # 初始化种群
                population = gaSample.creatStartPopulation(pathVarType2)  # initiate Population according to input variable number
                print"init population", population
                # for i in range(populationSize):
                #     t = population[i]
                #     t[2] = t[1]
                j = 1
                while j <= 10000:
                    old_pop = copy.deepcopy(population)
                    print "old_pop", old_pop
                    # 计算种群个体适应度值
                    oldInvidualFit, oldtargetfit = self.obtainIndividualFitness(currPathT, population, varname,
                                                                                populationSize, unTvardata)

                    # 测试用
                    #  oldInvidualFit = {0: 0.1667, 1: 0.2667, 2: 0.3667, 3: 0.5667, 4: 0.4667, 5: 0.1667, 6: 0.1667, 7: 0.1667, 8: 0.1667, 9: 0.1667}

                    # 如果种群中有满足的测试用例将它保留到精英种群，     ￥￥￥判断满足条件还需要在考虑一下，
                    # 或者依次判断种群里每一个个体的fit是否都==0，如果是，则种群满足条件。则输出所有的测试用例
                    elite = self.elite_population(oldInvidualFit, oldtargetfit, population)
                    # 如果精英种群的个体数==初始种群个体数，即初始种群完全符合条件
                    if len(elite) == len(population):
                        for i in range(len(elite)):
                            print"满足覆盖目标的测试用例", elite[i]
                        break
                    else:  # 否则初始种群不完全符合条件，需要进化，进化是整个种群都进化
                        #  整个种群开始进化，GA（选择，交叉，变异后得到的种群）
                        temp_pop = gaSample.GeneticAlgorithm(oldInvidualFit, population, pathVarType2)
                        print"temp_pop", temp_pop

                        # 测试用
                        #      temp_pop = gaSample.creatStartPopulation(pathVarType2)

                        #  计算一下变异后的种群个体的适应度值
                        newInvidualFit = self.obtainIndividualFitness(currPathT, temp_pop, varname, populationSize,
                                                                      unTvardata)

                        # 测试用
                        #      newInvidualFit = {0: 0.1667, 1: 0.9667, 2: 0.1667, 3: 0.1667, 4: 0.1667, 5: 0.1667, 6: 0.1667, 7: 0.1667, 8: 0.1667, 9: 0.1667}

                        # 把父代种群n个体和子代种群n个体合并，通过比较2n个体的适应度值，筛选populationSize个个体构成新种群
                        population = self.unpdata_pop(oldInvidualFit, newInvidualFit, old_pop, temp_pop, populationSize)
                    print"第", j, "次迭代"
                    j += 1
        else:
            print"The path has no variables"

    def seq_relate_unrelate(self, currpath, i):
        relate = []
        unrelate = []
        relate_total = handle.generate_seq_graph_traversal.handle_def_use_file()
        str = relate_total[i]
        str = str.split(',')
        for t in str:
            s = 'T' + t
            relate.append(s)
        for tran in relate:
            if tran in currpath:
                currpath.remove(tran)
        unrelate = currpath
        print '所有相关迁移list: ', relate_total
        print'相关迁移: ', relate
        print'非相关迁移: ', unrelate
        return relate, unrelate

    '''def testGen(self):
        pathList0 = [['T1', 'T2', 'T2', 'T2', 'T3']]
        #  ['T3', 'T4', 'T5', 'T7', 'T11', 'T10', 'T13', 'T12']
        path_user = [['T3', 'T4', 'T5', 'T7', 'T10', 'T12', 'T13', 'T14']]
        # path_modlue = handle.generate_seq.generate_path() #产生序列
        relate = []
        unrelate = []
        for path in path_user:
            startTime = datetime.now()
            print "当前路径序列及长度", path, len(path)
            i = 0
            relate, unrelate = self.seq_relate_unrelate(path, i)
            # 对该序列分相关relate_path、不先关迁移unrelate_path
            unTvardata = self.testdate_unrelate(unrelate)  # 非相关迁移unrelate_path约束求解
            self.testdate_relate(relate, unTvardata)  # 相关迁移unrelate_path约束和GA求解
            i += 1
            endTime = datetime.now()
            print 'endTime - startTime产生该序列数据用时:\t', endTime - startTime
            print 'average time平均时间:\t', (endTime - startTime) / 100
            print '===================================================='''''
    def testGen(self):
        # path_modlue =  handle.generate_seq.generate_path() #产生序列和数据
        # seq_toscript(path_modlue) #序列转换脚本
        # self.teatdate            #GA调整测试数据
        print "===================================================="

#######################################################
def efsmFromFile(inputfile):
    from kvparser import Parser, ListParser
    SM = EFSM(inputfile)
    f = open(inputfile)
    s = f.read()
    SMBlockList = ListParser().parse(s)
    for block in SMBlockList:
        if block[0] == 'State':
            for (key, value) in block[1]:
                SM.addState(State(value))
        elif block[0] == 'Transition':
            (name, srcName, tgtName, event, cond, action) = [item[1] for item in block[1]]
            if srcName != '':  # old code is !=''
                src = SM.state(srcName)
            else:
                print 'transition src can not be null'
            if tgtName != '':
                tgt = SM.state(tgtName)
            else:
                print 'transition tgt can not be null'  #
            SM.addTransition(Transition(name, src, tgt, event, cond, action))
        else:
            pass
    f.close()
    return SM


if __name__ == '__main__':  # not execute when import as a module
    inputfile = 1
    efsmFromFile(inputfile)



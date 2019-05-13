import sclexer
import random
from datetime import datetime
import copy


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

    '''def __repr__(self):
        return self[:]
        #return "<**Path %s**>" % self[:]  #for allpath representation style----syq'''

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


######################Simple Genetic Algorithm ##########################



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

    def genome(self, vartype, genomeLen=0):
        gens = []

        for i in range(genomeLen):
            boolFlag = 0
            for key, value in vartype.iteritems():
                if key == i and value == 'Boolean':
                    gens.append(random.randint(self.min, 1))
                    boolFlag = 1
                    break
            if (boolFlag == 0):
                gens.append(random.randint(self.min, self.max))
        return gens

    def creatStartPopulation(self, varType):
        self.genomes = []

        for i in range(self.populationSize):
            self.genomes.append(self.genome(varType, self.genomeLen))
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
                for j in range(self.populationSize):
                    maxFlag = 0
                    if rank <= accumFit[j]:
                        tempGene = self.genomes[j]
                        for k in range(self.genomeLen):
                            if tempGene[k] > self.max:
                                maxFlag = 1
                                break
                        if maxFlag == 0:
                            selectedGene.append(self.genomes[j])
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
            mutation = crossGene[i]
            rank = random.uniform(0, 1)
            if rank <= self.mutationRate:
                mutationPoint = random.randint(0, self.genomeLen - 1)
                mutation[mutationPoint] = random.randint(self.min, self.max)
                for key, value in vartype.iteritems():
                    if key == mutationPoint and value == 'Boolean':
                        mutation[mutationPoint] = random.randint(0, 1)
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
        crossedGenome = self.crossAddSubGA(selectedGenome)
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


#############################################################


class EFSM:
    """Instances of this class represent a EFSM machine.
    A machine is set of states and trsitions.
    """

    def __init__(self, name, transitionList=[]):
        """       """
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

    # caculate transition ID similarity of two path-------------------syq
    def sim_leven(self, first, second):
        match = 0
        mismatch = 0
        gap = abs(len(first) - len(second))
        for i in range(min(len(first), len(second))):
            if first[i] == second[i]:
                match = match + 1
            else:
                mismatch = mismatch + 1
        sim_tran = match * 1 + mismatch * 0 + gap * 0
        # print match,mismatch,gap
        print sim_tran

    # caculate transition ID + state similarity of two path----------------------syq
    def sim_tran_state(self, first, second):
        match = 0
        mismatch = 0
        gap = abs(len(first) - len(second))

        count_BothIden = 0
        count_SourceIden = 0
        count_SourceDiff = 0
        for i in range(min(len(first), len(second))):
            if first[i] == second[i]:
                match = match + 1
            else:
                mismatch = mismatch + 1
                for item in self.transitionList:  # dimatch tran's source,target state
                    if item.name == first[i]:
                        source1 = item.src.name
                        target1 = item.tgt.name
                    if item.name == second[i]:
                        source2 = item.src.name
                        target2 = item.tgt.name
                if source1 == source2:
                    if target1 == target2:
                        count_BothIden = count_BothIden + 1
                    else:
                        count_SourceIden = count_SourceIden + 1
                else:
                    count_SourceDiff = count_SourceDiff + 1
        sim_tran = match * 1 + mismatch * 0 + gap * 0
        print count_BothIden, count_SourceIden, count_SourceDiff
        sim_state = (count_BothIden * 2.0 + count_SourceIden * 1.0 + count_SourceDiff * 0) / (
        2 ** abs(len(first) - len(second)) + 1)  # how to consider the difference between path lengths ?
        print match, mismatch, gap
        print sim_tran, sim_state

    def findAllPath(self):
        """comput all paths of esfm
        Path: list of transitions [TS1, TS2,...]
        pathList: list of paths [[TS1, TS2],[TS1,TS2],...]
        """
        for startTran in self.startTransitionList:
            tempPathList = [Path([startTran])]  # path includes startTransition
            # print tempPathList
        allPathList = []
        count = 0
        feasiblePathList = []
        endStartNo = 0
        while len(tempPathList) > 0:
            currPath = tempPathList[0]
            restPathList = tempPathList[1:]
            lastTransition = currPath[-1]
            successorList = self.succDict[lastTransition]
            if (successorList == []):
                allPathList.append(Path(currPath))
                # print 'No%s:' % (count), currPath
                # print currPath
                '''if currPath.is_feasiable_ATM():
                    print 'No%s:'%(count),currPath
                    feasiblePathList.append(currPath)
                    count=count+1'''
                count = count + 1
                if len(allPathList) > 500:
                    break
            tempPathList = restPathList + self.pathAppend(currPath, successorList)

        # print '\t number of all path is ', len(allPathList)
        # print 'all no_repeat_tran path:',allPathList
        '''print 'number of no_repeat_tran feasible path:',count
        print 'all no_repeat_tran feasible path:',feasiblePathList'''
        # self.VarNumDefOnPath(allPathList[2])

        return allPathList

    # +++++++++++++++++++++++++++++++++syq++++++++++++++++++++++++++++++++++++#

    def findPath(self, start_tran):
        tempPathList = [Path([start_tran])]
        # print tempPathList
        allPathList = []
        count = 0
        feasiblePathList = []
        endStartNo = 0
        while len(tempPathList) > 0:
            currPath = tempPathList[0]
            restPathList = tempPathList[1:]
            lastTransition = currPath[-1]
            successorList = self.succDict.get(lastTransition)  # find the last's successors
            if (successorList == []):
                allPathList.append(Path(currPath))
                # print 'No%s:' % (count), currPath
                # print currPath
                count = count + 1
                if len(allPathList) > 10000:
                    break
            tempPathList = restPathList + self.pathAppend(currPath, successorList)

        # print '\t number of all path is ', len(allPathList)
        # print 'all no_repeat_tran path:',allPathList

        return allPathList

    def pathAppendWithRepeat(self, currPath, succList, countTran):
        """return path list [path1, path2,...]

        if item in succList does not show more than two times,
        append it to rList
        [a, b] and [c, d] will return [[a,b,c],[a,b,d]]
        [a,b,c,b,c] and [b,d] will return [[a,b,c,b,c,d]]
        If there is a self loop, the self loop is considered once
        """
        newList = []
        for item in succList:
            if (currPath.count(item.name) < 6):  # old code is 4
                newList.append(Path(currPath + [item.name]))
        return newList

    def findPathWithRepeat(self):
        """comput all paths of esfm
        Path: list of transitions [TS1, TS2,...]
        pathList: list of paths [[TS1, TS2],[TS1,TS2],...] with repeat time countTrans
        """

        countTrans = 1
        allPathList = []
        pathLengthDict = {}  #### key: length of path, value: number of the path with 'key' length
        maxPathLength = 51  # old code is maxPatLength=31
        pathLength = 0
        step = 0

        for startTran in self.startTransitionList:
            tempPathList = [Path([startTran])]  # path includes startTransition
        for L in range(70):
            pathLengthDict[L] = 0
        while (len(tempPathList) > step) and (pathLength <= maxPathLength):
            currPath = tempPathList[0]
            restPathList = tempPathList[step + 1:]
            lastTransition = currPath[-1]
            successorList = self.succDict[lastTransition]
            if currPath.is_feasiable_ATM():
                tempPathList = restPathList + self.pathAppendWithRepeat(currPath, successorList, countTrans)
            else:
                tempPathList = restPathList
            if (successorList == []):
                pathLength = len(currPath)
                if pathLengthDict[pathLength] < 5:  # old code is <20
                    allPathList.append(Path(currPath))
                    pathLengthDict[pathLength] = pathLengthDict[pathLength] + 1
                    #                    print 'path',currPath,len(currPath)
                    step = 0
                else:
                    step = step + 1
                    if step > 2:
                        step = 0
                        #        print '\t number of path with repeat trans is ', len(allPathList)
        for ipath in allPathList:
            self.pathTestGen[
                len(ipath)] = 0  ### initiate self.pathTestGen, key: the length of ipath, value: test generation flag
        return allPathList



        #################for transition #####################

    def givenTransPathAppend(self, givenTrans, currPath, succList):
        """return path list [path1, path2,...]
        for a given transition computer its path
        if given item in succList, other elements in succList are not considered
        if item in succList does not show more than two times,
        append it to rList
        [a, b] and [c, d] will return [[a,b,c],[a,b,d]]
        [a,b,c,b,c] and [b,d] will return [[a,b,c,b,c,d]]
        If there is a self loop, the self loop is considered once
        """
        newList = []

        if givenTrans in succList:
            if givenTrans in currPath:
                pass
            else:
                newList.append(Path(currPath + [givenTrans]))
            return newList
        for item in succList:
            if (currPath.count(item.name) < 1):  ### loop is allowed ,at most 3
                newList.append(Path(currPath + [item.name]))
        return newList

    def findPathforGivenTrans(self, givenTrans):
        """ Find not more than 10 path at rondom
            for a given transition
        """

        for startTran in self.startTransitionList:
            tempPathList = [Path([startTran])]  # path includes startTransition

        transPathList = []
        while len(transPathList) < 10:  ## most generated path number  that covers the given transition is 10
            currPath = tempPathList[0]
            restPathList = tempPathList[1:]
            lastTransition = currPath[-1]
            if givenTrans == lastTransition:
                transPathList.append(Path(currPath))
            successorList = self.succDict[lastTransition]
            tempPathList = restPathList + self.givenTransPathAppend(givenTrans, currPath, successorList)
            if len(tempPathList) == 0 or len(tempPathList) > 5000:
                break  ## 5000 successive pathes without include given transition,
                ### namely  10 possible path covering the given transition are not generated.
        return transPathList

    ############################################################
    # Variable, function analysis on transitions
    ############################################################

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
        print "condVuse:",vlist

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
        print "actionVdef:",vdef
        print "actionVuse:",vuse

    def initTranVarFuncList(self):
        for transition in self.transitionList:
            #    print '%s variables:'%transition.name
            self.vDefUseList(transition)

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

    def identifyLeftRight(self, string):
        """ identify left and right substing for a sting
        """

        operList = ["==", "!=", "<=", ">=", "<", ">"]
        subList = []
        flag = 0
        for oper in operList:
            if oper in string:
                #    print 'oper',oper
                for right in string.split(oper):
                    for left in string.split(oper):
                        if left != right:
                            flag = 1
                            break
            if flag == 1: break
        subList.append(left)
        subList.append(right)
        return subList

    def branchDistanceCompute(self, predicate, predVarValue):
        """ computer simple predicate's fitness
        """
        K = 1
        subList = []

        predicate = predicate.strip()
        predicate = predicate.strip("(")
        predicate = predicate.strip(")")
        subList = self.identifyLeftRight(predicate)
        rightstr = subList.pop(0)
        leftstr = subList.pop(0)

        leftValue = eval(leftstr, {}, predVarValue)
        if type(leftValue) == type(leftstr):
            leftValue = ord(leftValue)

        rightValue = eval(rightstr, {}, predVarValue)
        if type(rightValue) == type(rightstr):
            rightValue = ord(rightValue)

        distance = abs(leftValue - rightValue) + K
        if "!=" in predicate:
            distance = K
            #    distance=1-1.001**(-distance)
        return distance

    def outputTestData(self, currPath, varType, noinput):
        """ print test data
        """
        eventSequence = []
        i = 0
        while (i < len(currPath)):
            currTrans = currPath[i]
            for ftran, fdict in self.currPathTranFuncDict.iteritems():
                if ftran == currTrans:
                    eventSequence.append(fdict['eventFunc'])
            i = i + 1
        if eventSequence != []:
            print 'test event squence:', eventSequence
            if noinput == 0:
                print ' test data:',
                for var in self.pathVarValue:
                    print var,
                    if var in varType:
                        if varType[var] == "chr":
                            print ':', chr(self.pathVarValue[var]),
                    else:
                        print ':', self.pathVarValue[var],
                print

    def findVarInEvent(self, var, eventFun):
        """
        find var variable in the event
        """
        renameAndVarValue = {}  #### key: rename flag, value: condVuseValueDict[var]
        for tempstr in eventFun:
            if tempstr.rfind(var) >= 1:
                for tempsubstr in tempstr.rsplit("("):
                    for tempsubsub in tempsubstr.rsplit(","):
                        tempsubsub = tempsubsub.strip()
                        tempsubsub = tempsubsub.strip(")")
                        lensub = len(tempsubsub)
                        subsub = tempsubsub[0:lensub - 1]  # recognize variable form multip input variables
                        ## for example, price0,price1,price2
                        if var == subsub:
                            renameAndVarValue[1] = self.pathVarValue[tempsubsub]
                            return renameAndVarValue
        return renameAndVarValue

    def executePath(self, currPath, noInput):
        """ execute a path
            noInput=1------ ther is no input variable on the path, used in outputTestData function
        """
        condVuseValueDict = {}  ## key: variables used in condition
        #        condVuseTypeDict={}  ## key: variables used in condition, value: type of variable
        actionVdefValueDict = {}  ## key: variables defined in action
        actionVuseValueDict = {}  ## key: variables used in action
        #        tranExec={} ## key: transition, value:executed time
        approachLevel = len(currPath) - 1
        #        for tran in currPath:
        #            tranExec[tran]=0
        #        print 'self.pathVarValue'
        #        print self.pathVarValue,'\n\n'

        i = 0
        while (i < len(currPath)):
            currTrans = currPath[i]  #
            for vtran, vdict in self.currPathTranVarDict.iteritems():
                if vtran == currTrans:  ### find currTrans transition 's tranVarDict()
                    for ftran, fdict in self.currPathTranFuncDict.iteritems():
                        if ftran == currTrans:  ### find currTrans transition 's tranFuncDict()#
                            executActFlag = 0
                            # rename=0
                            ###########deal with event variables#############################
                            if self.tranVarDict[currTrans]['eventVdef'] != []:
                                for var in self.tranVarDict[currTrans]['eventVdef']:
                                    if currPath[0:i + 1].count(currTrans) > 1:
                                        condVuseValueDict[var] = self.pathVarValue[
                                            var + '_' + currTrans + '_' + repr(currPath[0:i].count(currTrans))]
                                    elif self.originalDef.count(var) > 1:
                                        for item in vdict['eventVdef']:
                                            if var == item[0:len(var)] and len(item) == len(
                                                    var) + 1:  # may be will produce some errors, for example: accept0, accepts
                                                condVuseValueDict[var] = self.pathVarValue[item]
                                                break
                                            if var == item:
                                                condVuseValueDict[var] = self.pathVarValue[item]
                                                break
                                    else:
                                        condVuseValueDict[var] = self.pathVarValue[var]

                            ###### execute condition#########
                            if fdict['condFunc'] != [''] and fdict['condFunc'] != []:
                                condStr = fdict['condFunc'][0]
                                if eval(condStr, {}, condVuseValueDict) == False:
                                    if '&' in condStr:
                                        totalFitness = 0.0
                                        for predStr in condStr.split(" & "):
                                            predStr = predStr.strip()
                                            predStr = predStr.strip("(")
                                            predStr = predStr.strip(")")

                                            branchDis = self.branchDistanceCompute(predStr, condVuseValueDict)
                                            totalFitness = totalFitness + branchDis
                                            # fitness=totalFitness+approachLevel
                                        distance = 1 - 1.001 ** (-totalFitness)
                                    elif '||' in condStr:  # gxh add
                                        totalFitness = 0.0
                                        for predStr in condStr.split(" || "):
                                            predStr = predStr.strip()
                                            predStr = predStr.strip("(")
                                            predStr = predStr.strip(")")

                                            branchDis = self.branchDistanceCompute(predStr, condVuseValueDict)
                                            totalFitness = totalFitness + branchDis
                                            # fitness=totalFitness+approachLevel
                                        distance = 1 - 1.001 ** (-totalFitness)
                                    else:
                                        branchDis = self.branchDistanceCompute(condStr, condVuseValueDict)
                                        distance = 1 - 1.001 ** (-branchDis)
                                    fitness = approachLevel + distance
                                    return fitness

                                    #   print ' ####execute action #######'
                            approachLevel = approachLevel - 1  ####approach level fitness
                            tempActFun = []
                            tempActFun.extend(fdict['actionFunc'])
                            tempActFun.reverse()
                            while tempActFun != []:
                                actionStr = tempActFun.pop()  ## only process one assignement statement
                                oneActFlag = 0
                                for stri in actionStr.rsplit("="):
                                    stri = stri.strip()
                                    if stri in vdict['actionVdef']:
                                        for strj in actionStr.split("="):
                                            strj = strj.strip()
                                            if strj != stri:
                                                rightStr = strj
                                                rightStr = repr(rightStr)
                                                for var in vdict['actionVuse']:
                                                    if var in condVuseValueDict.keys():
                                                        actionVuseValueDict[var] = condVuseValueDict[var]
                                                    elif var in actionVdefValueDict.keys():
                                                        actionVuseValueDict[var] = actionVdefValueDict[var]
                                                actionVdefValueDict[stri] = eval(eval(rightStr), {},
                                                                                 actionVuseValueDict)
                                                condVuseValueDict[stri] = actionVdefValueDict[stri]
                                                oneActFlag = 1
                                                break  ## break strj loop
                                    if oneActFlag == 1:
                                        break  #### break stri loop
                            executActFlag = 1
                            break  ###break for ftran,fdict loop
                    if executActFlag == 1:
                        #                        tranExec[currTrans]=tranExec[currTrans]+1
                        break  ### break vtran,vdict loop

                        #            print 'condVuseValueDict={}   condVuseTypeDict={}  actionVdefValueDict={}   actionVuseValueDict={} '
                        #            print 'the value of i is ',i
                        #            print condVuseValueDict,'\n'
                        #            print condVuseTypeDict,'\n'
                        #            print actionVdefValueDict,'\n'
                        #            print actionVuseValueDict,'\n'
            i = i + 1
        # if i == 7:
        #                return 0
        #   self.outputTestData(currPath , condVuseTypeDict, noInput)
        #    for var, val in actionVdefValueDict.iteritems():
        #        print '', var,val,
        #        print ',',
        #    print
        return 0

    def obtainIndividualFitness(self, currPath, invidual, populationSize, noInput):

        invidualFit = {}  ### key :genome, value: fitness   #
        self.pathVarValue = {}  ## key: variables on the path, value: corresponding value

        for i in range(populationSize):
            for var, val in zip(self.pathDefVar, invidual[i]):
                self.pathVarValue[var] = val
            fitness = self.executePath(currPath, noInput)
            if (fitness == 0) or (fitness == 0.0):  ##  the current path is executed
                invidualFit[0] = 0
                break
            else:
                invidualFit[i] = 1 / fitness
        return invidualFit

    def copyPathInfo(self):
        """
        copy path information into current Path Dictionary
        """

        self.currPathTranVarDict = copy.deepcopy(self.tranVarDict)
        self.currPathTranFuncDict = copy.deepcopy(self.tranFuncDict)
        # transition information in Current path copying from self.tranVarDict and self.tranfUNCdICT
        #   key transition.name, value:dict
        # {eventVdef:vlist, condVuse:vlist, actionVdef:vlist, actionVuse,vlist}

    def testGenforPath(self, currPath):

        populationSize = 10
        #        maxGeneration=10000
        self.repeatTranVarDict = {}
        self.repeatTranFuncDict = {}  ####store repeat transition
        self.currPathTranVarDict = {}
        # self.currPathTranFuncDict == {}
        population = []
        invidualFitness = {}  ## key:genome, value:fitness
        noInputVar = 0
        pathVarType = {}  ## key: variable , value: type of the variable
        self.copyPathInfo()

        for tran in currPath:
            if currPath.count(tran) > 1:
                self.repeatTrans(currPath)
                break

        self.pathInputVar(currPath)  # identify input variable in events relating to the current path
        # --- stored in self.originalDef
        self.pathProProcess(currPath)  # rewrite identical variables, ---stored in self.pathDefVar
        print"pathDefVar----", self.pathDefVar
        #        print 'print success'
        #        print currPath, '\t', len(currPath)

        for num in range(len(self.pathDefVar)):
            pathVarType[num] = 'int'
            if 'garauntee' in self.pathDefVar[num] or 'accept' in self.pathDefVar[num]:
                pathVarType[num] = 'Boolean'

        if len(self.pathDefVar) > 0:  ##There exist input variables on the path
            for repeat in range(10):
                gaSample = GA(populationSize, len(self.pathDefVar))
                population = gaSample.creatStartPopulation(pathVarType)  #  initiate Population according to input variable number
                print"init population",population
                j = 1
                while 1:
                    oldInvidualFit = self.obtainIndividualFitness(currPath, population, populationSize, noInputVar)
                    if oldInvidualFit[0] == 0:
                        print 'No' + str(repeat) + '\tsuccessGeneration\t', j
                        self.outputTestData(currPath, pathVarType, 0)
                        break  # break for j loop
                    j += 1
                    population = gaSample.GeneticAlgorithm(oldInvidualFit, population, pathVarType)
                    invidualFitness = self.obtainIndividualFitness(currPath, population, populationSize, noInputVar)
                    if invidualFitness[0] == 0:
                        print 'No' + str(repeat) + '\tsuccessGeneration\t', j
                        self.outputTestData(currPath, pathVarType, 0)
                        break  # break for j loop
                    population = gaSample.basicSurvive(oldInvidualFit, invidualFitness, population)
                    if repeat == 0 and j >= 10000:
                        print 'this path is not feasible'
                        return 0
        else:
            noInputVar = 1
            self.executePath(currPath, noInputVar)








            ################### find all path for a given transition###############

    def allPathNum(self):
        """initiate and find all path
        """

        self.findStartTransition()
        self.findEndTransition()
        self.initTransitionSuccessor()
        self.initTranVarFuncList()
        self.findAllPath()


    ###################defined and used variables anaysis for a path##################


    def VarNumDefOnPath(self, currPath):
        """
        analysis the defined variables on a path 
        """

        actionDefVar = []  ### variables defined on action functions relating to a path
        eventVar = 0

        self.pathInputVar(currPath)  ### saved on self.originalDef list
        temp = 0
        while (temp < len(currPath)):
            currTrans = currPath[temp]
            for vtran, vdict in self.tranVarDict.iteritems():
                if vtran == currTrans:
                    eventVar = eventVar + len(vdict['eventVdef'])
                    if vtran != 'T1':
                        tempvdict = []
                        #####deal with action variables#######
                        tempvdict.extend(vdict['actionVdef'])
                        while tempvdict != []:
                            tempVar = tempvdict.pop(0)
                            if tempVar == 'False' or tempVar == 'True':
                                pass
                            else:
                                actionDefVar.append(tempVar)
                        break
            temp = temp + 1
        actionVar = set(actionDefVar)
        print '   ', eventVar + len(actionVar),
        print '   ', eventVar,
        print '   ', len(actionVar),

    def condNumOnPath(self, currPath):
        """
        compute the number of conditions and sub-conditions on the path
        """

        condNum = 0
        subcondNum = 0
        equalOperator = 0
        logicalEqual = 0

        temp = 0
        while (temp < len(currPath)):
            currTrans = currPath[temp]
            tempFlag = 0
            for vtran, vdict in self.tranVarDict.iteritems():
                if vtran == currTrans:
                    for ftran, fdict in self.tranFuncDict.iteritems():
                        if ftran == currTrans:
                            tempFlag = 1
                            if (fdict['condFunc'] != [''] and fdict['condFunc'] != []):
                                condNum = condNum + 1
                                subcondNum = subcondNum + 1
                                tempcond = []
                                tempcond.extend(fdict['condFunc'])
                                cond = tempcond.pop()
                                if cond.count('||') >= 1:
                                    subcondNum = subcondNum + cond.count('||')
                                if cond.count('&') >= 1:
                                    subcondNum = subcondNum + cond.count('&')
                                if cond.count('==') >= 1:
                                    equalOperator = equalOperator + cond.count('==')
                                    if cond.count('True') >= 1:
                                        logicalEqual = logicalEqual + cond.count('Ture')
                                    if cond.count('False') >= 1:
                                        logicalEqual = logicalEqual + cond.count('False')

                            break

                    if (tempFlag == 1): break
            temp = temp + 1
        print '  ', condNum,
        print '  ', subcondNum,
        print '  ', equalOperator,
        print '  ', subcondNum - equalOperator,
        print '  ', logicalEqual,
        print '  ', equalOperator - logicalEqual,

    def VarNumUseOnPath(self, currPath):
        """        
        compute the number of used variables on a path
        """
        useInCond = []
        useInAction = []

        temp = 0
        while (temp < len(currPath)):
            currTrans = currPath[temp]
            for vtran, vdict in self.tranVarDict.iteritems():
                if vtran == currTrans:
                    if vdict['condVuse'] != []:
                        useEachCond = []
                        tempvdict = []
                        #####deal with condition #######
                        tempvdict.extend(vdict['condVuse'])
                        while tempvdict != []:
                            tempVar = tempvdict.pop(0)
                            if tempVar == 'False' or tempVar == 'True':
                                pass
                            else:
                                useEachCond.append(tempVar)
                        removeRepeat = set(useEachCond)
                        for tempVar in removeRepeat:
                            if tempVar in vdict['eventVdef']:
                                useInCond.append(tempVar)
                            else:
                                if tempVar not in useInCond:
                                    useInCond.append(tempVar)
                    if vdict['actionVuse'] != []:
                        #####deal with action variables#######
                        useEachAct = []
                        tempvdict = []
                        tempvdict.extend(vdict['actionVuse'])
                        while tempvdict != []:
                            tempVar = tempvdict.pop(0)
                            if tempVar == 'False' or tempVar == 'True':
                                pass
                            else:
                                useEachAct.append(tempVar)
                        removeRepeat = set(useEachAct)
                        for tempVar in removeRepeat:
                            if tempVar in vdict['eventVdef']:
                                useInAction.append(tempVar)
                            else:
                                if tempVar not in useInAction:
                                    useInAction.append(tempVar)

                    break
            temp = temp + 1
        print '  ', len(useInCond),
        print '  ', len(useInAction),

    def VarNumDefUseOnPath(self, currPath):
        """
        compute the number of variables on a path including defined and used
        """

        defEventUseCond = []
        defActUseCond = []

        temp = 0
        while (temp < len(currPath)):
            currTrans = currPath[temp]
            for vtran, vdict in self.tranVarDict.iteritems():
                if vtran == currTrans:
                    tempvdict = []
                    tempvdict.extend(vdict['eventVdef'])
                    while tempvdict != []:
                        tempVar = tempvdict.pop(0)
                        if tempVar in vdict['condVuse']:
                            defEventUseCond.append(tempVar)
                        else:
                            nexti = temp + 1
                            if (nexti < len(currPath)):
                                nextTrans = currPath[nexti]
                                for vvtran, vvdict in self.tranVarDict.iteritems():
                                    if vvtran == nextTrans:
                                        if tempVar not in vvdict['eventVdef'] and tempVar in vvdict['condVuse']:
                                            defEventUseCond.append(tempVar)
                                        break

                                        #####deal with action variables#######
                    tempvdict = []
                    tempvdict.extend(vdict['actionVdef'])
                    while tempvdict != []:
                        tempVar = tempvdict.pop(0)
                        if tempVar == 'False' or tempVar == 'True':
                            pass
                        else:
                            nexti = temp + 1
                            while (nexti < len(currPath)):
                                nextTrans = currPath[nexti]
                                useFlag = 0
                                for vvtran, vvdict in self.tranVarDict.iteritems():
                                    if vvtran == nextTrans:
                                        if tempVar in vvdict['condVuse']:
                                            defActUseCond.append(tempVar)
                                            useFlag = 1
                                        break
                                if (useFlag == 1): break
                                nexti = nexti + 1
                    break
            temp = temp + 1
        print '  ', len(defEventUseCond),
        print '  ', len(set(defActUseCond)),

    def eventNumOnPath(self, currPath):
        """ compute the number of event on the currPath path
        """
        eventNum = 0
        eventWithVar = 0

        temp = 0
        while (temp < len(currPath)):
            currTrans = currPath[temp]
            tempFlag = 0
            for vtran, vdict in self.tranVarDict.iteritems():
                if vtran == currTrans:
                    for ftran, fdict in self.tranFuncDict.iteritems():
                        if ftran == currTrans:
                            tempFlag = 1
                            if (fdict['eventFunc'] != [''] and fdict['eventFunc'] != []):
                                #       print 'event func', fdict['eventFunc']
                                eventNum = eventNum + 1
                                if vdict['eventVdef'] != []:
                                    eventWithVar = eventWithVar + 1
                            break
                    if (tempFlag == 1): break
            temp = temp + 1
        print ' eventNum', eventNum,
        print 'eventWithVa', eventWithVar

    def duAnalysis(self):
        """
        analysis the number of variables, defined variables, used variables,
        definded and used variables, conditions, sub-condition, length according to a path
        """

        for item in self.transitionList:
            coveredTrans = item.name
            print ' transition', coveredTrans
            transPathList = self.findPathforGivenTrans(coveredTrans)
            i = 0
            while (i < len(transPathList)):
                print 'NO. path', i,
                currPath = transPathList[i]
                print '    currPath', currPath
                #  print ' lengthOfPath', len(currPath),
                print '  ', len(currPath),
                self.VarNumDefOnPath(currPath)
                self.VarNumUseOnPath(currPath)
                self.VarNumDefUseOnPath(currPath)
                self.condNumOnPath(currPath)
                i = i + 1

    def DUAnalysisForPath(self, currPath):

        print 'currPath', currPath
        print '  ', len(currPath),
        self.VarNumDefOnPath(currPath)
        self.VarNumUseOnPath(currPath)
        self.VarNumDefUseOnPath(currPath)
        self.condNumOnPath(currPath)
        self.eventNumOnPath(currPath)

    def testGenForTrans(self, givenTrans):
        """ test data generation for a given path
        """

        populationSize = 20
        maxGeneration = 5000

        #
        transPathList = self.findPathforGivenTrans(givenTrans)

        i = 0
        while (i < len(transPathList)):
            currPath = transPathList[i]
            self.DUAnalysisForPath(currPath)
            #       self.testGenforPath(currPath,populationSize,maxGeneration)
            i = i + 1



            ################# test generation for each transition########

            #    def testGen(self):
            #        """ generate test data for each transition in a EFSM
            #        """
            #
            #        for i in range(1):
            #
            #            for item in self.transitionList:
            #                if item.name in self.startTransitionList:
            #                    pass
            #                else:
            #                    coveredTrans=item.name
            #                    print ' Transition', coveredTrans
            #                    self.testGenForTrans(coveredTrans)






            ################# test generation for path that length <= 100 ########

    def testGen(self):
        pathList0 = [['T1', 'T2', 'T2', 'T2', 'T3'], ['T1', 'T4', 'T6', 'T7', 'T11', 'T16', 'T9', 'T8', 'T20', 'T22', 'T10', 'T23'],
                     ['T1', 'T4', 'T5', 'T7', 'T12', 'T15', 'T13', 'T15', 'T14', 'T15', 'T9', 'T8', 'T19', 'T21', 'T17',
                      'T21', 'T18', 'T21', 'T10', 'T23']]

        path_user = [['T3', 'T4', 'T5', 'T7'],
                     ['T1', 'T2','T20', 'T4', 'T5', 'T7', 'T8', 'T9', 'T10']]
        # for path in path_user:
        for path in pathList0:
            startTime = datetime.now()
            print path, len(path)
            self.testGenforPath(path)
            endTime = datetime.now()
            print 'endTime - startTime:\t', endTime - startTime
            print 'average time:\t', (endTime - startTime) / 100


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

            ##   format of transitionList is <Transition T1 <state START> <state S1? Card(pin, sb, cb)  write("Enter PIN"); attempts = 0;>
    f.close()
    return SM


# Generate Random String
def GenerateRandomString(len, basechars=[]):
    if (basechars == []):
        # x = range(ord('a'), ord('z') + 1)
        # x.extend(range(ord('A'), ord('Z') + 1))
        # x.extend(range(ord('0'), ord('9') + 1))
        x = range(32,126)
        basechars = [chr(i) for i in x]
        ret = ''
        for i in range(len):
            ret += random.choice(basechars)
        return ret

if __name__ == '__main__':  # not execute when import as a module
   print GenerateRandomString(9)
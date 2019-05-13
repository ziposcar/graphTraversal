#encoding:utf-8
from kvparser import ListParser
from handle_EFSM_module import EFSM
from handle_EFSM_module import State
from handle_EFSM_module import Transition
import config

def efsmFromFile(inputfile):
    SM = EFSM(inputfile)
    f = open(inputfile)
    s = f.read() # 读完所有内容
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
    # allTranEvent = SM.TEvent
    return SM

###########  处理模型信息SM 随时取其中的各种信息，调用各种函数  ######################

def obtain_efsm():
    inputfile = config.getModule()
    SM = efsmFromFile(inputfile)
    SM.allPathNum()
    print "%s has %s states and  %s transitions" % (SM.name, len(SM.stateList), len(SM.transitionList))
    print "start transition：", SM.startTransitionList
    print "end transition：", SM.endTransitionList
    return SM

#得到某efsm的全部迁移信息（name, src, tgt, event, cond, action）
def obtain_tran_info():
    SM=obtain_efsm()
    return SM.transitionList


def obtain_tran_event():
    SM = obtain_efsm()
    print SM.name
    return SM.TEvent


if __name__ == '__main__':  # not execute when import as a module
    SM = obtain_efsm()
    print "%s has %s states and  %s transitions" % (SM.name, len(SM.stateList), len(SM.transitionList))
    # print "start transition：", SM.startTransitionList
    # print "end transition：", SM.endTransitionList
    t =  obtain_tran_info()
    for i in range(len(t)):
        print t[i], "\n"

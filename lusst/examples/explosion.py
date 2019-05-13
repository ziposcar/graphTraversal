import sys
sys.path.append("..")
#from SM import *
from SMIlie import *
if len(sys.argv) > 1:
    import imp
    file, pathname, description = imp.find_module(sys.argv[1])
    try:
        sm_mod = imp.load_module(sys.argv[1], file, pathname, description)
    finally:
        if file:
            file.close()
    State_Machine = sm_mod.State_Machine





def david_example():

    s1 = State("s1", True)
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    states = [s1, s2, s3, s4]

    t1 = Transition("t1", s1, s2, True)
    t2 = Transition("t2", s1, s2, False)

    t3 = Transition("t3", s2, s3, True)
    t4 = Transition("t4", s2, s3, True)

    t5 = Transition("t5", s3, s4, True)

    transitions = [t1, t2, t3, t4, t5]

    sm = State_Machine(states, transitions)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    return



def kelly_laurie_example():

    s1 = State("s1", True)
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    states = [s1, s2, s3, s4, s5]

    t1 = Transition("t1", s1, s2, True)
    t2 = Transition("t2", s2, s2, True)

    t3 = Transition("t3", s2, s3, False)

    t4 = Transition("t4", s3, s4, True)
    t5 = Transition("t5", s4, s3, True)

    t6 = Transition("t6", s3, s5, True)
    t7 = Transition("t7", s5, s3, True)   

    transitions = [t1, t2, t3, t4, t5, t6, t7]

    sm = State_Machine(states, transitions)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    return

def our_weakness3():

    s1 = State("s1", True)
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    states = [s1, s2, s3, s4, s5]

    t1 = Transition("t1", s1, s2, True)
    t2 = Transition("t2", s2, s2, False)

    t3 = Transition("t3", s2, s3, False)

    t4 = Transition("t4", s3, s4, True)
    t5 = Transition("t5", s4, s3, True)

    t6 = Transition("t6", s3, s5, True)
    t7 = Transition("t7", s5, s3, True)
    t8 = Transition("t8", s3, s2, False)    

    transitions = [t1, t2, t3, t4, t5, t6, t7, t8]

    sm = State_Machine(states, transitions)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    sm.visualize()
    sm.slice()
    sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    return
    
def our_weakness4():

    s1 = State("s1", True)
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    states = [s1, s2, s3, s4, s5]

    t1 = Transition("t1", s1, s2, True)
    t2 = Transition("t2", s2, s2, False)

    t3 = Transition("t3", s2, s3, False)

    t4 = Transition("t4", s3, s4, True)
    t5 = Transition("t5", s4, s3, True)

    t6 = Transition("t6", s3, s5, True)
    t7 = Transition("t7", s5, s3, True)
    t8 = Transition("t8", s2, s3, False)    

    transitions = [t1, t2, t3, t4, t5, t6, t7, t8]

    sm = State_Machine(states, transitions)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    return

def our_weakness5():

    s1 = State("s1", True)
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    states = [s1, s2, s3, s4, s5]

    t1 = Transition("t1", s1, s2, True)
    t3 = Transition("t3", s2, s3, False)

    t4 = Transition("t4", s3, s4, True)
    t5 = Transition("t5", s4, s3, True)

    t6 = Transition("t6", s3, s5, True)
    t7 = Transition("t7", s5, s3, True)
    t8 = Transition("t8", s3, s2, False)    

    transitions = [t1, t3, t4, t5, t6, t7, t8]

    sm = State_Machine(states, transitions)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    return
    
def our_weakness6():

    s1 = State("s1", True)
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    states = [s1, s2, s3, s4, s5]

    t1 = Transition("t1", s1, s2, True)

    t3 = Transition("t3", s2, s3, False)

    t4 = Transition("t4", s3, s4, True)
    t5 = Transition("t5", s4, s3, True)

    t6 = Transition("t6", s3, s5, True)
    t7 = Transition("t7", s5, s3, True)   

    transitions = [t1, t3, t4, t5, t6, t7]

    sm = State_Machine(states, transitions)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    return


def kelly_laurie_not_quite_example():

    s1 = State("s1", True)
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    states = [s1, s2, s3, s4, s5]

    t1 = Transition("t1", s1, s2, True)
    t2 = Transition("t2", s2, s2, False) # <- Notice this is false

    t3 = Transition("t3", s2, s3, False)

    t4 = Transition("t4", s3, s4, True)
    t5 = Transition("t5", s4, s3, True)

    t6 = Transition("t6", s3, s5, True)
    t7 = Transition("t7", s5, s3, True)

    transitions = [t1, t2, t3, t4, t5, t6, t7]

    sm = State_Machine(states, transitions)

    print sm.nearest_marked_transitions(s2)
    print sm.nearest_marked_transitions(s3)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    return



def kelly_2_example():

    s0 = State("s0", True)
    s1 = State("s1")
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    states = [s0, s1, s2, s3, s4]

    t1 = Transition("t1", s0, s1, False)
    t2 = Transition("t2", s1, s2, True)

    t3 = Transition("t3", s1, s2, True)

    t4 = Transition("t4", s2, s3, True)
    t5 = Transition("t5", s0, s4, True)

    t6 = Transition("t6", s4, s1, False)

    transitions = [t1, t2, t3, t4, t5, t6]

    sm = State_Machine(states, transitions)

    print sm.nearest_marked_transitions(s2)
    print sm.nearest_marked_transitions(s3)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions



def kelly_3_example():

    s0 = State("s0", True)
    s1 = State("s1")
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    states = [s0, s1, s2, s3, s4, s5]

    t1 = Transition("t1", s0, s1, False)
    t2 = Transition("t2", s1, s1, True)

    t3 = Transition("t3", s1, s1, True)

    t4 = Transition("t4", s1, s2, True)
    t5 = Transition("t5", s1, s2, False)

    t6 = Transition("t6", s1, s3, False)
    t7 = Transition("t7", s2, s5, False)
    t8 = Transition("t8", s3, s4, False)
    t9 = Transition("t9", s0, s0, True)
    t10 = Transition("t10", s5, s4, True)

    transitions = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]

    sm = State_Machine(states, transitions)

    print sm.nearest_marked_transitions(s2)
    print sm.nearest_marked_transitions(s3)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions


def kelly_3_2_example():

    s0 = State("s0", True)
    s1 = State("s1")
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    states = [s0, s1, s2, s3, s4, s5]

    t1 = Transition("t1", s0, s1, False)
    t2 = Transition("t2", s1, s1, True)

    t3 = Transition("t3", s1, s1, True)

    t4 = Transition("t4", s1, s2, True)
    t5 = Transition("t5", s1, s2, False)

    t6 = Transition("t6", s1, s3, False)
    t7 = Transition("t7", s2, s4, True)
    t8 = Transition("t8", s3, s4, False)
    t9 = Transition("t9", s0, s5, True)
    t10 = Transition("t10", s5, s0, False)

    transitions = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]

    sm = State_Machine(states, transitions)

    print sm.nearest_marked_transitions(s2)
    print sm.nearest_marked_transitions(s3)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions



def kelly_4_example():

    s0 = State("s0", True)
    s1 = State("s1")
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    states = [s0, s1, s2, s3, s4]


    t1 = Transition("t1", s0, s1, False)
    t2 = Transition("t2", s1, s1, True)

    t3 = Transition("t3", s1, s1, True)

    t4 = Transition("t4", s1, s2, True)
    t5 = Transition("t5", s1, s2, False)

    t6 = Transition("t6", s1, s3, False)
    t7 = Transition("t7", s2, s4, True)
    t8 = Transition("t8", s3, s4, False)
    t9 = Transition("t9", s1, s2, True)
    t10 = Transition("t10", s1, s3, True)
    t11 = Transition("t11", s2, s2, False)


    transitions = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]

    sm = State_Machine(states, transitions)

    print sm.nearest_marked_transitions(s2)
    print sm.nearest_marked_transitions(s3)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions



def kelly_madeup_example():

    s0 = State("s0", True)
    s1 = State("s1")
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    s6 = State("s6")
    s7 = State("s7")
    s8 = State("s8")
    s9 = State("s9")
    s10 = State("s10")
    exit = State("exit")
    states = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, exit]

    t1 = Transition("t1", s0, s1, False)
    t2 = Transition("t2", s1, s4, False)

    t3 = Transition("t3", s4, s5, False)

    t4 = Transition("t4", s4, s6, False)
    t5 = Transition("t5", s5, s7, False)

    t6 = Transition("t6", s6, s7, False)
    t7 = Transition("t7", s7, s8, False)
    t8 = Transition("t8", s8, exit, False)
    t9 = Transition("t9", s1, s2, False)
    t10 = Transition("t10", s2, s3, False)
    t11 = Transition("t11", s3, exit, False)
    t12 = Transition("t12", s1, s9, True)
    t13 = Transition("t13", s9, s10, False)
    t14 = Transition("t14", s9, s10, True)
    t15 = Transition("t15", s10, s4, False)

    transitions = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15]

    sm = State_Machine(states, transitions)

    print sm.nearest_marked_transitions(s2)
    print sm.nearest_marked_transitions(s3)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

def korel_weakness1():

    s0 = State("s0", True)
    s1 = State("s1")
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    s6 = State("s6")
   
    states = [s0, s1, s2, s3, s4, s5, s6]

    t1 = Transition("t1", s0, s1, True)
    t2 = Transition("t2", s1, s2, True)
    t3 = Transition("t3", s2, s4, False)
    t4 = Transition("t4", s2, s4, False)
    t5 = Transition("t5", s2, s4, True)
    t6 = Transition("t6", s2, s4, False)
    t7 = Transition("t7", s2, s2, True)
    t8 = Transition("t8", s4, s2, True)
    t9 = Transition("t9", s4, s2, False)
    t10 = Transition("t10", s4, s6, True)
    t11 = Transition("t11", s1, s3, False)
    t12 = Transition("t12", s3, s5, False)
 
    transitions = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]

    sm = State_Machine(states, transitions)

    print sm.nearest_marked_transitions(s2)
    print sm.nearest_marked_transitions(s3)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

def our_weakness1():

    s0 = State("s0", True)
    s1 = State("s1")
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    s6 = State("s6")
   
    states = [s0, s1, s2, s3, s4, s5, s6]

    t1 = Transition("t1", s0, s1, True)
    t2 = Transition("t2", s1, s2, True)
    t3 = Transition("t3", s2, s4, False)
    t4 = Transition("t4", s2, s4, False)
    t5 = Transition("t5", s2, s4, True)
    t6 = Transition("t6", s2, s4, False)
    t7 = Transition("t7", s2, s2, True)
    t8 = Transition("t8", s4, s2, False)
    t9 = Transition("t9", s4, s2, False)
    t10 = Transition("t10", s4, s6, True)
    t11 = Transition("t11", s1, s3, False)
    t12 = Transition("t12", s3, s5, False)
 
    transitions = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]

    sm = State_Machine(states, transitions)

    print sm.nearest_marked_transitions(s2)
    print sm.nearest_marked_transitions(s3)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    sm.visualize()
    sm.slice()
    sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions
    
def our_weakness2():

    s0 = State("s0", True)
    s1 = State("s1")
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    s6 = State("s6")
   
    states = [s0, s1, s2, s3, s4, s5, s6]

    t1 = Transition("t1", s0, s1, True)
    t2 = Transition("t2", s1, s2, True)
    t3 = Transition("t3", s2, s4, False)
    t4 = Transition("t4", s2, s4, False)
    t5 = Transition("t5", s2, s4, False)
    t6 = Transition("t6", s2, s4, False)
    t7 = Transition("t7", s2, s2, True)
    t8 = Transition("t8", s4, s2, False)  #same problem in the case when t8 is true - t8 and t10 are deleted
    t9 = Transition("t9", s4, s2, False)
    t10 = Transition("t10", s4, s6, True)
    t11 = Transition("t11", s1, s3, False)
    t12 = Transition("t12", s3, s5, False)
 
    transitions = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]

    sm = State_Machine(states, transitions)

    print sm.nearest_marked_transitions(s2)
    print sm.nearest_marked_transitions(s3)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions


def atm_example():

    s0 = State("s0",True)
    s1 = State("s1")
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    s6 = State("s6")
    s7 = State("s7")
    exit = State("exit")
    states = [s0, s1, s2, s3, s4, s5, s6, s7, exit]


    t1 = Transition("t1", s0, s1, True)
    t2 = Transition("t2", s1, s1, False)

    t3 = Transition("t3", s1, exit, False)

    t4 = Transition("t4", s1, s2, True)
    t5 = Transition("t5", s2, s3, False)

    t6 = Transition("t6", s2, s3, False)
    t7 = Transition("t7", s3, s4, False)
    t8 = Transition("t8", s3, s6, True)
    t9 = Transition("t9", s4, s3, False)
    t10 = Transition("t10", s6, s3, False)
    t11 = Transition("t11", s4, s5, False)
    t12 = Transition("t12", s4, s5, False)
    t13  = Transition("t13",s4, s5, False)
    t14  = Transition("t14",s4, s5, False)
    t15  = Transition("t15",s5, s4, False)
    t16  = Transition("t16",s5, s4, False)
    t17  = Transition("t17",s6, s7, True)
    t18  = Transition("t18",s6, s7, True)
    t19  = Transition("t19",s6, s7, False)
    t20  = Transition("t20",s6, s7, False)
    t21  = Transition("t21",s7, s6, False)
    t22  = Transition("t22",s7, s6, False)
    t23  = Transition("t23",s3, exit, False)
    transitions = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23]

    sm = State_Machine(states, transitions)

    print sm.nearest_marked_transitions(s6)
    print sm.unmarked_transitions_from(s6)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    sm.visualize()
    sm.slice()
    sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions



def cashier_example():

    s0 = State("s0", True)
    s1 = State("s1")
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    s6 = State("s6")
    s7 = State("s7")
    s8 = State("s8")
    s9 = State("s9")
    s10 = State("s10")
    exit = State("exit")
    states = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, exit]

    t1 = Transition("t1", s0, s1, True)
    t2 = Transition("t2", s1, s1, True)

    t3 = Transition("t3", s1, s2, False)

    t4 = Transition("t4", s2, s3, True)
    t5 = Transition("t5", s3, s4, True)

    t6 = Transition("t6", s4, s5, True)
    t7 = Transition("t7", s5, s2, True)
    t8 = Transition("t8", s5, exit, False)
    t9 = Transition("t9", s3, s6, True)
    t10 = Transition("t10", s6, s6, True)
    t11 = Transition("t11", s6, exit, False)
    t12 = Transition("t12", s2, s7, True)
    t13  = Transition("t13",s7, s2, True)
    t14  = Transition("t14",s7, exit, False)
    t15  = Transition("t15",s6, s2, False)
    t16  = Transition("t16",s2, s8, True)
    t17  = Transition("t17",s8, s9, True)
    t18  = Transition("t18",s9, s2, True)
    t19  = Transition("t19",s9, s10, True)
    t20  = Transition("t20",s10, exit, False)
    t21  = Transition("t21",s10, s2, True)

    transitions = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21]

    sm = State_Machine(states, transitions)

    print sm.nearest_marked_transitions(s6)
    print sm.unmarked_transitions_from(s6)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    #sm.visualize()
    sm.slice()
    #sm.visualize()

    print "  After (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions




if __name__ == "__main__":
    # print "David's explosion example"
    # david_example()

    # print
    # print "Kelly and Laurie's explosion example"
    # kelly_laurie_example()

    # print
    # print "Kelly and Laurie's explosion example"
    # our_weakness3()

    # print
    # print "Kelly and Laurie's explosion example"
    # our_weakness4()

    # print
    # print "Kelly and Laurie's explosion example"
    # our_weakness5()

    # print
    # print "Kelly and Laurie's explosion example"
    # our_weakness6()

    # print
    # print "Kelly and Laurie's not quite explosion example"
    # kelly_laurie_not_quite_example()

    # print
    # print "Kelly's 2nd example"
    # kelly_2_example()

    # print
    # print "Kelly's 3nd example"
    # kelly_3_example()

    # print
    # print "Kelly's 3.5nd example"
    # kelly_3_2_example()

    # print
    # print "Kelly's 4th example"
    # kelly_4_example()

    # print
    # print "Kelly's made up example"
    # kelly_madeup_example()

    # print
    # print "An example that shows a weakness in Korel's reduction algorithm"
    # korel_weakness1()
    
    # print
    # print "Weakness 1"
    # our_weakness1()
    
    # print
    # print "Weakness 2"
    # our_weakness2()

    # print
    # print "Weakness 3"
    # our_weakness3()
    # sys.exit(0)
    
    print
    print "The ATM example"
    atm_example()

    # print
    # print "The Cashier example"
    # cashier_example()

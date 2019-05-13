import sys
sys.path.append("..")
from SMIlie import *



def test1():

    s1 = State("s1", True)
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    states = [s1, s2, s3, s4, s5]
    
    
    t1 = Transition("t1", s1, s2, True)
    t2 = Transition("t2", s1, s3, True)

    t3 = Transition("t3", s2, s4, True)
    t4 = Transition("t3", s3, s5, True)

    transitions = [t1, t2, t3, t4]

    sm = State_Machine(states, transitions)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    sm.visualize()
    # sm.merge_rightinvariant()
    sm.merge()
    sm.visualize()

def test2():

    s1 = State("s1", True)
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    s6 = State("s6")
    states = [s1, s2, s3, s4, s5, s6]
    
    
    t1 = Transition("t1", s1, s2, True)
    t2 = Transition("t2", s1, s3, True)

    t3 = Transition("t3", s2, s4, True)
    t4 = Transition("t3", s3, s5, True)

    t5 = Transition("t4", s4, s6, True)
    t6 = Transition("t4", s5, s6, True)

    transitions = [t1, t2, t3, t4, t5, t6]

    sm = State_Machine(states, transitions)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    sm.visualize()
    # sm.merge_rightinvariant()
    sm.merge()
    sm.visualize()


def test3():

    s1 = State("s1", True)
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")
    s5 = State("s5")
    s6 = State("s6")
    s7 = State("s7")
    states = [s1, s2, s3, s4, s5, s6, s7]
    
    
    t1 = Transition("t1", s1, s2, True)
    t2 = Transition("t2", s1, s3, True)

    t3 = Transition("t3", s1, s4, True)
    t4 = Transition("t4", s2, s5, True)

    t5 = Transition("t4", s3, s6, True)
    t6 = Transition("t4", s4, s7, True)

    transitions = [t1, t2, t3, t4, t5, t6]

    sm = State_Machine(states, transitions)

    print "  Before (%d states, %d transitions)" % (len(sm.states), len(sm.transitions))
    print " ", sm.states
    print " ", sm.transitions

    sm.visualize()
    # sm.merge_rightinvariant()
    sm.merge()
    sm.visualize()


if __name__ == "__main__":
    test2()

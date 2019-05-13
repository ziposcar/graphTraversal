import sys
sys.path.append("..")
from SM import *




def tutorial_stuff():

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

    # All the stuff below this line is simple examples - you can delete these if you want.
    
    print "Transitions from s1:", sm.transitions_from(s1)
    print "Marked transitions from s1:", sm.marked_transitions_from(s1)
    print "Unmarked transitions from s1:", sm.unmarked_transitions_from(s1)
    
    for t in sm.transitions_from(s2):
        print t

    print "is_path(s1, s4)?", sm.is_path(s1, s4)
    print "is_path(s4, s1)?", sm.is_path(s4, s1)
    print "is_path(s1, s1)?", sm.is_path(s1, s1)
    
    # Clone t1, changing its target node to s4; then delete the old t1 and add the new one to the
    # state machine
    
    new_t1 = Transition(t1.name, t1.source, s4, t1.is_marked)
    sm.transitions.remove(t1)
    sm.transitions.append(new_t1)
    print sm.transitions




if __name__ == "__main__":
    tutorial_stuff()
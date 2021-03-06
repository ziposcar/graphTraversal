# Korel's non-deterministic slicing algorithm
# Kelly adapted some of Laurie's original code for reduction. 



import os, platform, sys, tempfile




class State:

    def __init__(self, name, is_start=False):
    
        self.name = name
        self.is_start = is_start



    def __repr__(self):
    
        return "<State %s>" % self.name




class Transition:

    def __init__(self, name, source, target, event=None, cond=None, action=None, is_marked=True):
    
        self.name = name
        self.source = source
        self.target = target
        self.event=event
        self.cond=cond
        self.action=action
        self.is_marked = is_marked




    def __repr__(self):
    
        if self.is_marked:
            im = " marked"
        else:
            im = ""

        return "<Transition %s from %s to %s%s>" % \
          (self.name, self.source.name, self.target.name, im)


    def __eq__(self, o):

        if self.name == o.name and self.source is o.source and self.target is o.target \
          and self.event==o.event and self.cond==o.cond and self.action==o.action \
          and self.is_marked == o.is_marked:
            return True
        else:
            return False       



class State_Machine:

    def __init__(self, states, transitions):
    
        self.states = states
        self.transitions = transitions

    def transition(self, name=None):
        if name == None:
            return self.transitionList
        else:
            for transition in self.transitions:
                if transition.name == name:
                    return transition            
            print 'can not find %s in the state machine' % name


    def start_states(self):
    
        return [s for s in self.states if s.is_start]



    def transitions_from(self, state):
    
        return [t for t in self.transitions if t.source is state]



    def transitions_from_to(self, state1, state2):
    
        return [t for t in self.transitions if t.source is state1 and t.target is state2]



    def marked_transitions_from(self, state):
    
        return [t for t in self.transitions if t.source is state and t.is_marked]
        


    def unmarked_transitions_from(self, state):
    
        return [t for t in self.transitions if t.source is state and not t.is_marked]



    def unmarked_transitions_from_to(self, state1, state2):
    
        return [t for t in self.transitions if t.source is state1 and t.target is state2 and not t.is_marked]

    def unique_transitions(self):
        # return a list of transitions with unique labels(event, cond and action) in current model transitions
        allTrans=self.transitions[:]
        A=[]
        while allTrans:
            firstTran=allTrans[0]
            restTrans=allTrans[1:]
            for t in restTrans[:]:
                if t.event==firstTran.event and t.cond==firstTran.cond and t.action==firstTran.action:
                    restTrans.remove(t)
            A.append(firstTran)
            allTrans=restTrans
        return A

    def transitions_to(self, state):
    
        return [t for t in self.transitions if t.target is state]
    
    
    
    #
    # Returns True if the lists ts1 and ts2 contain the same transitions. Note that the transitions
    # in the two lists don't have to be in the same order for this to return true.
    #
    
    def transitions_are_the_same(self, ts1, ts2):
    
        if len(ts1) == len(ts2):
            return False
        
        for t in ts1:
            if t not in ts2:
                return False
        
        return True




    def marked_transitions_to(self, state):
    
        return [t for t in self.transitions if t.target is state and t.is_marked]


    #
    # Returns True if there is a path from 'from_state' to 'to_state', False otherwise.
    #
    # Note that 'is_path(x, x)' only returns True if there is a transition out of x that (ultimately)
    # leads back to it. If there isn't, then this will return False.
    #

    def is_path(self, from_state, to_state):

        seen = set()
        def helper(s):
            for t in self.transitions_from(s):
                if t.target is to_state:
                    return True
                if id(t.target) not in seen:
                    seen.add(id(t.target))
                    if helper(t.target):
                        return True
            return False

        return helper(from_state)

    # def is_transition_path(self, from_t1, to_t2):

    #     seen = set()
    #     def helper(s):
    #         if from_t1 == to_t2:
    #             return True                
    #         for t in self.transitions_from(s):
    #             if t is to_t2:                
    #                 return True
    #             if id(t) not in seen: 
    #                 seen.add(id(t))
    #                 if helper(t.target):
    #                     return True
    #         return False

        return helper(from_t1.target)

    def is_path_avoiding(self, from_state, to_state, avoiding_t):

        seen = set()
        def helper(s):
            for t in self.transitions_from(s):
                if t is avoiding_t:
                    continue

                if t.target is to_state:
                    return True

                if id(t.target) not in seen:
                    seen.add(id(t.target))
                    if helper(t.target):
                        return True
            return False

        return helper(from_state)



    def nearest_marked_transitions(self, state):
    
        old_level = [state]
        seen = set()
        i = 0 
        while len(old_level) > 0:
            new_level = []
            marked_transitions = []
            for s in old_level:
                if id(s) in seen:
                    continue

                seen.add(id(s))
                marked_transitions.extend(self.marked_transitions_from(s))
                for t in self.transitions_from(s):
                    new_level.append(t.target)
                    
            old_level = new_level
            
            if len(marked_transitions) > 0:
                return marked_transitions

        return []



    def marked_transition_in_subgraph(self, s):

        seen = set()
        stack = [s]
        while len(stack) > 0:
            c = stack.pop()
            seen.add(id(c))
            if len(self.marked_transitions_from(c)) > 0:
                return True
            for t in self.unmarked_transitions_from(c):
                if id(t.target) not in seen:
                    stack.append(t.target)

        return False
       
    def delete_unmarked_self_transitions(self):
        flag = True
        #Delete all self-transitions that are unmarked
        j = 0
        while j < len(self.transitions):
            t = self.transitions[j]
            if not t.is_marked and t.source == t.target:
                del self.transitions[j]
                flag = False
            else:
                j += 1   
         
        return flag
   
   
    def delete_transition(self, trans):
        #Delete all transitions that are in to_delete
        j = 0
        while j < len(self.transitions):
            t = self.transitions[j]
            if t == trans and not t.is_marked:
                del self.transitions[j]
            else:
                j += 1  
        

    def slice(self, criterion_name):

        criterion=self.transition(criterion_name)
       #Need to delete transitions on paths that do not include the slicing criterion 
        for i in range(len(self.states)):
            s1 = self.states[i]
            from_s1 = self.transitions_from(s1)
            for t in from_s1:
                if t.target is criterion.source:
                    flag=True
                else:
                    flag = self.is_path(t.target, criterion.source)
                if flag == False and t.name != criterion and not t.is_marked:
                    self.delete_transition(t)        
            else:
                continue
        # for t in self.transitions:
        #     print("path", self.is_transition_path(t, criterion))


        # To clean up unreachable states
        self.gc(self.start_states())

        
        no_more_to_merge = False;
        
        while no_more_to_merge == False:
             rule1 = self.mergeRule1()
             rule2 = self.mergeRule2()
             rule3 = self.delete_unmarked_self_transitions()
             no_more_to_merge = rule1 and rule2 and rule3
            
      
          


    def gc(self, roots):
    
        stack = roots[:]
        seen_states = set()
        seen_transitions = set()
        while len(stack) > 0:
            s = stack.pop()
            if id(s) in seen_states:
                continue
            seen_states.add(id(s))
            
            for t in self.transitions_from(s):
                seen_transitions.add(id(t))
                stack.append(t.target)

        i = 0
        while i < len(self.states):
            if id(self.states[i]) not in seen_states:
                del self.states[i]
            else:
                i += 1

        i = 0
        while i < len(self.transitions):
            if id(self.transitions[i]) not in seen_transitions:
                del self.transitions[i]
            else:
                i += 1


    #This is the first reduction rule by Korel- If there exists unmarked transitions from S1 to S2
    # and also from S2 to S1, then the states are merged
    def mergeRule1(self):
        
        have_merged = False
        while True:
            merged = False
            for i in range(len(self.states)):
                # We might merge more than one state together, so we collect a list starting with the
                # current state. If to_merge still only contains that element after the search then
                # this state can't be merged with anything else.

                to_merge = [self.states[i]]

                for j in range(len(self.states)):
                    if i == j:
                        continue

                    s1 = self.states[i]
                    s2 = self.states[j]

                    s1_from = self.transitions_from(s1)
                    s2_from = self.transitions_from(s2)

                    unmarked_from_s1 = []
                    unmarked_from_s2 = []                    
                   
                    for t1 in s1_from:                        
                        for t2 in s2_from:
                            if t1.target is s2 and not t1.is_marked:
                               unmarked_from_s1.append(t1)
                            if t2.target is s1 and not t2.is_marked:
                               unmarked_from_s2.append(t2)
                         
                  
                    if len(unmarked_from_s1) < 1 or len(unmarked_from_s2) < 1 :
                        continue

                    if unmarked_from_s1 > 0 and unmarked_from_s2 > 0:
                        to_merge.append(self.states[j])

                if len(to_merge) > 1:
                    # Merge the states together.
                    is_start = False
                    for s in to_merge:
                        if s.is_start:
                            is_start = True
                            break

                    name = "/".join([x.name for x in to_merge])
                    new_s = State(name, is_start)

                    for s in to_merge:
                        for t in self.transitions_from(s):
                            t.source = new_s

                        for t in self.transitions_to(s):
                            t.target = new_s

                    i = 0
                    while i < len(self.states):
                        for s in to_merge:
                            if self.states[i] is s:
                                del self.states[i]
                                break
                        else:
                            i += 1

                    self.states.append(new_s)

                    merged = True
                    have_merged = True
                    break

            if not merged:
                break

        return not have_merged


#This is the second reduction rule by Korel, i.e. it merges states where there
# is an unmarked transition from S1 to S2 and there does not exist a marked transition from S1 to S2
# and there is no outgoing transition from S1 to S3 where S2 /= S3

    def mergeRule2(self):
        
        have_merged = False
        while True:
            merged = False
            for i in range(len(self.states)):
                # We might merge more than one state together, so we collect a list starting with the
                # current state. If to_merge still only contains that element after the search then
                # this state can't be merged with anything else.

                to_merge = [self.states[i]]

                for j in range(len(self.states)):
                    if i == j:
                        continue

                    s1 = self.states[i]
                    s2 = self.states[j]

                    s1_from = self.transitions_from(s1)
                    s2_from = self.transitions_from(s2)
                                                                                 
                    unmarked_from_s1 = []
                    unmarked_only = True
                    for t1 in s1_from:
                        if not t1.target is s2: # and not t1.target is t1.source:
                            unmarked_only = False
                            break
                        elif t1.target is s2 and t1.is_marked:
                            unmarked_only = False
                            break
                        elif (t1.target is s2 and not t1.is_marked):
                           unmarked_from_s1.append(t1)
                         

                    if len(unmarked_from_s1) < 1:
                        continue

                    if not unmarked_only:
                        continue

                    if len(unmarked_from_s1) > 0:
                        to_merge.append(self.states[j])

                if len(to_merge) > 1:
                    # Merge the states together.
                    is_start = False
                    for s in to_merge:
                        if s.is_start:
                            is_start = True
                            break

                    name = "/".join([x.name for x in to_merge])
                    new_s = State(name, is_start)

                    for s in to_merge:
                        for t in self.transitions_from(s):
                            t.source = new_s

                        for t in self.transitions_to(s):
                            t.target = new_s

                    i = 0
                    while i < len(self.states):
                        for s in to_merge:
                            if self.states[i] is s:
                                del self.states[i]
                                break
                        else:
                            i += 1

                    self.states.append(new_s)

                    merged = True
                    have_merged = True
                    break

            if not merged:
                break

        return not have_merged



    def visualize(self):

        has_gv = False # ghostview
        has_open = False # Mac OS X utility
        if platform.system() in ('Windows', 'Microsoft'):
            # win32
            psviewer = 'gsview32'
            has_gv = True
        else:
            # Assume it's UNIX (either proper or Mac OS X)
            psviewer = 'gv'
    
            if os.system("which dot 2> /dev/null > /dev/null") != 0:
                sys.stderr.write("Error: You must install graphviz before trying to visualize a graph.\n")
                sys.exit(1)

            if os.system("which gv 2> /dev/null > /dev/null") == 0:
                has_gv = True

            if os.system("which open 2> /dev/null > /dev/null") == 0:
                has_open = True

            if not (has_gv or has_open):
                sys.stderr.write("Error: You must install 'gv' or 'open' before trying to visualize a graph.\n")
                sys.exit(1)
    
        o = []
        for s in self.states:
            if s.is_start:
                shape = ", shape=doublecircle"
            else:
                shape = ""
            
            o.append("""%s [label="%s"%s];""" % (id(s), s.name, shape))

        for t in self.transitions:
            if not t.is_marked:
                style = ", style=dashed"
            else:
                style = ""
            
            o.append("""%s -> %s [label="%s", arrowhead=vee%s];""" % (id(t.source), id(t.target), t.name, style))
            
        handle, dot_path = tempfile.mkstemp()
        os.write(handle, "digraph {  %s\n}" % "\n  ".join(o))
        os.close(handle)
        
        if has_open:
            handle, ps_path = tempfile.mkstemp(".pdf")
            os.close(handle)
        
            os.system("dot -T pdf -o %s %s" % (ps_path, dot_path))
            os.system("open %s&" % ps_path)
        elif has_gv:
            handle, ps_path = tempfile.mkstemp(".ps")
            os.close(handle)
        
            os.system("dot -T ps -o %s %s" % (ps_path, dot_path))
            os.system("%s %s&" % (psviewer, ps_path))

        os.remove(dot_path)

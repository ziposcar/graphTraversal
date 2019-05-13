# Adapted by Kelly in order to implement the algorithm described by Ilie et al.

# Copyright (C) 2008 Laurence Tratt http://tratt.net/laurie/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.


import os, platform, sys, tempfile




class State:

    def __init__(self, name, is_start=False):
    
        self.name = name
        self.is_start = is_start



    def __repr__(self):
    
        return "<State %s>" % self.name


    # def __eq__(self, o):

    #     if self.name == o.name and self.is_start == o.is_start:
    #         return True
    #     else:
    #         return False



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
        self.eventsList = []



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
    
        if len(ts1) != len(ts2):
            return False
        
        same = []
        for t in ts1:
            for t2 in ts2:
                if t.name == t2.name and t.target == t2.target:
                    same.append(t2)
                    break
                    
        if len(ts1) != len(same):
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
	
		stack = [state]
		seen = set()
		marked = []
		marked_seen = set()
		while len(stack) > 0:
			s = stack.pop()
			if id(s) in seen:
				continue
			seen.add(id(s))
			for t in self.marked_transitions_from(s):
				if id(t) in marked_seen:
					continue
				marked.append(t)
				marked_seen.add(id(t))
			
			for t in self.unmarked_transitions_from(s):
				stack.append(t.target)
		
		return marked



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
    
        #Delete all self-transitions that are unmarked
        j = 0
        while j < len(self.transitions):
            t = self.transitions[j]
            if not t.is_marked and t.source == t.target:
                del self.transitions[j]
            else:
                j += 1   
   
    def delete_multi_unmarked_transitions(self):
            #Delete multi  unmarked transitions with same source and target
        for t1 in self.transitions[:]:
            for t2 in self.transitions:
                if t1 is not t2 and not t1.is_marked and not t2.is_marked \
                        and t1.source==t2.source and t1.target==t2.target:
                   if t1 in self.transitions:
                       self.transitions.remove(t1)

    def applyRules(self):

        no_more_to_merge = False;
        
        while no_more_to_merge == False:

            #Apply rule for merging states with only one outgoing unmarked transition
            rule1 = self.merge3()
        
            # any cycle of epsilon transitions can be collapsed 
            # (all states merged and transitions removed)
            rule2 = self.merge2()
            no_more_to_merge = rule1 and rule2
        

    def slice(self):
        #zheng:Delete multi  unmarked transitions with same source and target
        self.delete_multi_unmarked_transitions()


        self.applyRules()
        
        #Removing epsilon transitions by copying
        stack = self.start_states()
        new_transitions = []
        
        seen = set()
        while len(stack) > 0:
            wn = stack.pop()
            if id(wn) in seen:
                continue
            seen.add(id(wn))
            
            for t in self.unmarked_transitions_from(wn):
                for mt in self.nearest_marked_transitions(t.target):
                    new_transitions.append((mt, wn))

            for t in self.transitions_from(wn):
                stack.append(t.target)

        for t, s in new_transitions:
            a = Transition(t.name, s, t.target, t.event, t.cond, t.action, t.is_marked)
            
            if a not in self.transitions:
                self.transitions.append(a)

        #Delete all unmarked transitions
        i = 0
        while i < len(self.transitions):
            t = self.transitions[i]
            if not t.is_marked:
                del self.transitions[i]
            else:
                i += 1
       
        self.gc(self.start_states())
        
        self.merge_rightinvariant()

        self.merge_leftinvariant()
        #laure's merge
        # self.merge()
        
########################################          
    def inputslice(self, eventsList):
        print('eventsList',eventsList)
        for t in self.transitions[:]:
            if t.event in eventsList:
                self.transitions.remove(t)
        # for t in self.transitions:
        #     print(t.name, t.event)
        self.gc(self.start_states())





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

    def list_in(self, list1, list2):
        """ check if all elements in list1 are also in list2
        """
        for p in list1:
            if p not in list2:
                return False
        return True

    def non_right_eqv(self, A, p, q, non_right_eqv, transitions_list):
        """ check if s1 not equivalent s2
        """
        for a in  A:
            state_from_p_by_a=[t.target for t in transitions_list if t.source==p and t.event==a.event and t.cond==a.cond and t.action==a.action]
            state_from_q_by_a=[t.target for t in transitions_list if t.source==q and t.event==a.event and t.cond==a.cond and t.action==a.action]
            for s1 in state_from_p_by_a:
                temppairlist=[(s1, s2) for s2 in state_from_q_by_a]
                if self.list_in(temppairlist, non_right_eqv): # find a non right eqv
                    return True
        return False

    def merge_rightinvariant(self):
        """ This algorithm computes the right equivalent states
        """
        s_Empty=State("EMPTY")
        all_states=self.states[:]
        all_states.append(s_Empty)
        # find a unique transition set
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
        # A=set([t.name for t in self.transitions])
        # print("A is ", A)

        all_transitions=self.transitions[:]
        for a in A:
            for s in self.states:
                all_transitions.append(Transition(a.name, s, s_Empty, a.event, a.cond, a.action, True))
            all_transitions.append(Transition(a.name, s_Empty, s_Empty, a.event, a.cond, a.action, True))

        non_right_eqv_set=set()
#        right_eqv=set()
        for s in self.states:
            non_right_eqv_set.add((s_Empty, s))
            non_right_eqv_set.add((s, s_Empty))
        
        while True:
            flag=True
            for p in all_states:
                for q in all_states:
                    if (p,q) not in non_right_eqv_set and \
                            self.non_right_eqv(A, p, q, non_right_eqv_set, all_transitions):
                        # print("bingo", (p,q))
                        non_right_eqv_set.add((p,q))
                        non_right_eqv_set.add((q,p))
                        flag=False
            if flag:
                break

        all_pairs=set()
        symm_pairs=set()
        for p in all_states:
            for q in all_states:
                all_pairs.add((p,q))
                all_pairs.add((q,p))
            symm_pairs.add((p,p))
        right_eqv_set=all_pairs - non_right_eqv_set - symm_pairs
#        right_eqv_set.remove((s_Empty, s_Empty))
        # print(right_eqv_set)

        # #find the states list to be merged
        # to_merge_list=[]
        # if right_eqv_set:
        #     to_merge_list.append(list(list(right_eqv_set)[0]))
        #     for pair in right_eqv_set:
        #         p=pair[0]
        #         q=pair[1]
        #         all_states_in_merge=[]
        #         for item in to_merge_list:
        #             for s in item:
        #                 all_states_in_merge.append(s)
        #         if p not in all_states_in_merge and q not in all_states_in_merge:
        #             to_merge_list.append([p,q])
        #         for item in to_merge_list:
        #             if p in item and q not in item:
        #                 item.append(q)
        #             elif p not in item and q in item:
        #                 item.append(p)

        to_merge_list=[]
        if right_eqv_set:
            to_merge_set=set()
            for pair in right_eqv_set:
                for s in pair:
                    to_merge_set.add(s)
            to_merge_list=[[s] for s in to_merge_set]
            for pair in right_eqv_set:
                p=pair[0]
                q=pair[1]
                for l in to_merge_list:
                    if p in l:
                        p_merge=l
                    if q in l:
                        q_merge=l
                if p_merge is not q_merge:
                    to_merge_list.remove(p_merge)
                    to_merge_list.remove(q_merge)
                    to_merge_list.append(p_merge+q_merge)
                        

        #merge states
        print("to merge list", to_merge_list)
        while to_merge_list:
            first_merge=to_merge_list[0]
            rest_merge=to_merge_list[1:]

            for s in first_merge:
                is_start = False
                if s.is_start:
                    is_start = True
                    break
            name = "/".join([x.name for x in first_merge])
            new_s = State(name, is_start)
            self.states.append(new_s)

            for s in first_merge:
                # print(self.states)
                # print("remove", s)
                self.states.remove(s)
                # if s in self.states:
                #     self.states.remove(s)
                for t in self.transitions_from(s):
                    t.source = new_s
                for t in self.transitions_to(s):
                    t.target = new_s
            to_merge_list=rest_merge
        # print("merged state", self.states)

        # this code will merge all transitions with the same source, same target state and same label
        old_tran_list=self.transitions[:]
        new_tran_list=[]
        while old_tran_list:
            first_tran=old_tran_list[0]
            rest_trans=old_tran_list[1:]
            for t in rest_trans[:]:
                if first_tran.source is t.source and first_tran.target is t.target \
                        and first_tran.event==t.event and first_tran.cond==t.cond \
                        and first_tran.action==t.action:
                    if first_tran.name == t.name:
                        rest_trans.remove(t)
                    else:
                        first_tran.name="/".join([first_tran.name, t.name ])
                        rest_trans.remove(t)
            new_tran_list.append(first_tran)
            old_tran_list=rest_trans
        self.transitions=new_tran_list
        # print("merged transitions", self.transitions)


        # #remove duplicated transitions
        # old_tran_list=self.transitions[:]
        # new_tran_list=[]
        # while old_tran_list:
        #     first_tran=old_tran_list[0]
        #     rest_trans=old_tran_list[1:]
        #     if first_tran not in rest_trans:
        #         new_tran_list.append(first_tran)
        #     old_tran_list=rest_trans
        # self.transitions=new_tran_list
        # # print("merged transitions", self.transitions)

########################################          
    def merge_leftinvariant(self):
        """ This algorithm computes the left equivalent states
        """
        for s in self.states:
            s.is_start= not s.is_start
        for t in self.transitions:
            temp=t.source
            t.source=t.target
            t.target=temp

        self.merge_rightinvariant()
        
        for s in self.states:
            s.is_start= not s.is_start
        for t in self.transitions:
            temp=t.source
            t.source=t.target
            t.target=temp





    def merge(self):
    
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
                    
                    from_s1_to_s2 = self.transitions_from_to(s1, s2)
                    from_s2_to_s1 = self.transitions_from_to(s2, s1)
                    if len(from_s1_to_s2) == len(from_s2_to_s1):
                        if len(from_s1_to_s2) > 0 and self.transitions_are_the_same(from_s1_to_s2, from_s2_to_s1):
                            to_merge.append(self.states[j])
                            continue
                    
                    
                    s1_from = self.transitions_from(s1)
                    s2_from = self.transitions_from(s2)
                    if len(s1_from) > 0 and self.transitions_are_the_same(s1_from, s2_from):
                        to_merge.append(self.states[j])
                        continue

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
                    break
            
            for s in self.states:
                k = 0
                while k < len(self.transitions):
                    l = k + 1
                    while l < len(self.transitions):
                        if self.transitions[k] == self.transitions[l]:
                            del self.transitions[l]
                        else:
                            l += 1
                    k += 1
            
            if not merged:
                break


    def merge2(self):
    
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
                    unmarked_only = True
                    for t1 in s1_from:
                        for t2 in s2_from:
                            if t1.target is s2 and not t1.is_marked:
                               unmarked_from_s1.append(t1)
                            elif t2.target is s1 and not t2.is_marked:
                               unmarked_from_s2.append(t2)
                            elif t1.target is s2 and t1.is_marked:
                                unmarked_only = False
                                break
                            elif t2.target is s1 and t2.is_marked:
                                unmarked_only = False
                                break

                    if len(unmarked_from_s1) < 1 or len(unmarked_from_s2) < 1 :
                        continue

                    if not unmarked_only:
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

        self.delete_unmarked_self_transitions()
        return not have_merged


# It merges states where there
# is an unmarked transition from S1 to S2 and the outdegree of S1 is 1.

    def merge3(self):
    
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
                    #s2_from = self.transitions_from(s2)
                    
                    
                    if (len(s1_from) > 1):
                        continue
                                          
                    unmarked_from_s1 = []
                    unmarked_only = True
                    for t1 in s1_from:
                        if not t1.target is s2 and not t1.target is t1.source:
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

                    if unmarked_from_s1 > 0:
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

        self.delete_unmarked_self_transitions()
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

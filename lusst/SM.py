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




class Transition:

    def __init__(self, name, source, target):
    
        self.name = name
        self.source = source
        self.target = target
        #self.isz_marked = is_marked



    def __repr__(self):
    
        '''if self.is_marked:
            im = " marked"
        else:
            im = "" '''

        return "<Transition %s from %s to %s>" % \
          (self.name, self.source.name, self.target.name)



    def __eq__(self, o):

        if self.name == o.name and self.source is o.source and self.target is o.target:
            return True
        else:
            return False
        



class State_Machine:

    def __init__(self, states, transitions):
    
        self.states = states
        self.transitions = transitions



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
                    


    def slice(self):

        stack = self.start_states()
        new_transitions = []
        
        seen = set()
        transitions_to_keep = set()
        while len(stack) > 0:
            wn = stack.pop()
            if id(wn) in seen:
                continue
            seen.add(id(wn))
            
            for t in self.unmarked_transitions_from(wn):
                if not self.marked_transition_in_subgraph(t.target):
                    continue

                # Do we want to keep t as is?
                has_marked_path = False
                for mt in self.marked_transitions_from(t.source):
                    if mt.source is mt.target:
                        continue
                    if self.is_path_avoiding(mt.target, t.target, t):
                        has_marked_path = True
                        break

                if has_marked_path:
                    continue

                if len(self.nearest_marked_transitions(t.target)) > len(self.unmarked_transitions_from_to(t.source, t.target)):
                    transitions_to_keep.add(id(t))
                    continue

                # Try and avoid explosion.
                for mt in self.nearest_marked_transitions(t.target):
                    new_transitions.append((mt, wn))

            for t in self.transitions_from(wn):
                stack.append(t.target)

        for t, s in new_transitions:
            a = Transition(t.name, s, t.target, t.is_marked)
            
            if a not in self.transitions:
                self.transitions.append(a)

        i = 0
        while i < len(self.transitions):
            t = self.transitions[i]
            if not (t.is_marked or id(t) in transitions_to_keep):
                del self.transitions[i]
            else:
                i += 1

        self.gc(self.start_states())
        
        self.merge()



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
                        print "from", s1.name, "to", s2.name, from_s1_to_s2, from_s2_to_s1
                    if len(from_s1_to_s2) > 0 and self.transitions_are_the_same(from_s1_to_s2, from_s2_to_s1):
                        print "from", s1.name, "to", s2.name, "are the same"
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



    def visualize(self, criterionTran=None):

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

            if criterionTran:
                criterionName=criterionTran.name
            else:
                criterionName=None
            if  t.name==criterionName:
                o.append("""%s -> %s [color=blue, fontcolor=blue, fontsize=18, label="%s", arrowhead=vee%s];""" % (id(t.source), id(t.target), t.name, style))
            else:
                o.append("""%s -> %s [label="%s", arrowhead=vee%s];""" % (id(t.source), id(t.target), t.name, style))

        handle, dot_path = tempfile.mkstemp()
#        os.write(handle, "digraph {\n size=\"7.2, 10.5\"; ratio=fill;\n  %s\n}" % "\n  ".join(o))
#        os.write(handle, "digraph {\n size=\"10.5, 7.2\"; ratio=fill;\n  %s\n}" % "\n  ".join(o))
        os.write(handle, "digraph {\n %s\n}" % "\n  ".join(o))
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

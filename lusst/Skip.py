import SM




class State_Machine(SM.State_Machine):

    def skip_transitions_from(self, state):

        return [t for t in self.transitions if t.source is state and t.name == "skip"]



    def is_sibling_to(self, fromSt, toSt):

        for t in self.marked_transitions_from(fromSt):
            if id(t.target) == id(toSt):
                print "t.target = ", id(t.target)
                print "toSt = ", id(toSt)
                return True

        return False



    def is_marked_to(self, toSt):

        for t in self.marked_transitions_to(toSt):
            #if id(t.target) == id(fromSt):
            if t.source != t.target:
                print "t.target = ", id(t.target)
                #print "toSt = ", id(toSt)
                return True

        return False



    def is_reachable(self, from_s, to_s):
    
        seen = set()
        def helper(s):
            for t in self.transitions_from(s):
                if t.target is to_s and t.is_marked:
                    return True
                if id(t.target) not in seen and t.is_marked:
                    seen.add(id(t.target))
                    if helper(t.target):
                        return True
            return False

        return helper(from_s)



    def slice(self):

        #Delete all self-transitions that are unmarked
        j = 0
        while j < len(self.transitions):
            t = self.transitions[j]
            if not t.is_marked and t.source == t.target:
                del self.transitions[j]
            else:
                j += 1

        stack = self.start_states()
        new_transitions = []

        seen = set()
        while len(stack) > 0:
            wn = stack.pop()
            if id(wn) in seen:
                continue
            seen.add(id(wn))

            for t in self.unmarked_transitions_from(wn):
                print "unmarked transition =", t
                if self.is_sibling_to(wn, t.target) or self.is_reachable(wn, t.target): # or self.is_path_avoiding(wn, t.target, t):
                #if self.is_reachable(wn, t.target):
                    print "there is a sibling marked transition to t.target "
                    print "or there is a marked incomming transition"
                    break
                else:
                    for mt in self.nearest_marked_transitions(t.target):
		                new_transitions.append((wn, t.target))


            for t in self.transitions_from(wn):
                stack.append(t.target)


        for s, t in new_transitions:
            a = SM.Transition("skip", s, t, True)

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
        #self.merge() #Looks like we might not need this
        self.merge2()
        #self.merge3()
        self.merge4()
        self.slice2()
        self.merge5()


    #This is a second pass to delete any skips that are double
    def slice2(self):

        stack = self.start_states()
        skip_to_delete = []

        seen = set()
        while len(stack) > 0:
            wn = stack.pop()
            if id(wn) in seen:
                continue
            seen.add(id(wn))

            for t in self.skip_transitions_from(wn):
                if self.is_path_avoiding(wn, t.target, t):
                    skip_to_delete.append(t)
                    break


            for t in self.transitions_from(wn):
                stack.append(t.target)


        #Delete all skip transitions that have been collected in skip_to_delete
        i = 0
        if len(skip_to_delete) > 0:
            while i < len(self.transitions):
                t = self.transitions[i]
                for k in skip_to_delete:
                    if t == k:
                        del self.transitions[i]
                        break;
                i += 1



    #This is the first reduction rule by Korel
    def merge2(self):

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

                    skip_from_s1 = []
                    skip_from_s2 = []
                    skip_only = True
                    for t1 in s1_from:
                        for t2 in s2_from:
                            if t1.target is s2 and t1.name == "skip":
                               skip_from_s1.append(t1)
                            elif t2.target is s1 and t2.name == "skip":
                               skip_from_s2.append(t2)
                            elif t1.target is s2 and t1.name != "skip":
                                skip_only = False
                                break
                            elif t2.target is s1 and t2.name != "skip":
                                skip_only = False
                                break

                    print "skip_from_s1 = ", skip_from_s1
                    print "skip_from_s2 =", skip_from_s2

                    if len(skip_from_s1) < 1 or len(skip_from_s2) < 1 :
                        continue

                    if not skip_only:
                        continue

                    if skip_from_s1 > 0 and skip_from_s2 > 0:
                        to_merge.append(self.states[j])

                if len(to_merge) > 1:
                    # Merge the states together.
                    is_start = False
                    for s in to_merge:
                        if s.is_start:
                            is_start = True
                            break

                    name = "/".join([x.name for x in to_merge])
                    new_s = SM.State(name, is_start)

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

            if not merged:
                break

        self.delete_skip_self_trans()



    #This is the second reduction rule by Korel
    def merge3(self):

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

                    skip_from_s1 = []
                    skip_only = True
                    for t1 in s1_from:
                        if not t1.target is s2 and not t1.target is t1.source:
                            skip_only = False
                            break
                        elif t1.target is s2 and t1.name != "skip":
                            skip_only = False
                            break
                        elif (t1.target is s2 and t1.name == "skip"):
                           skip_from_s1.append(t1)

                    if len(skip_from_s1) < 1:
                        continue

                    if not skip_only:
                        continue

                    if skip_from_s1 > 0:
                        to_merge.append(self.states[j])

                if len(to_merge) > 1:
                    # Merge the states together.
                    is_start = False
                    for s in to_merge:
                        if s.is_start:
                            is_start = True
                            break

                    name = "/".join([x.name for x in to_merge])
                    new_s = SM.State(name, is_start)

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

            if not merged:
                break

        self.delete_skip_self_trans()



 #This is similar to the second reduction rule by Korel - it merges states that have non-contributing
 #transitions and no other transitions to other states and no self-loops
    def merge4(self):

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

                    skip_from_s1 = []
                    skip_only = True
                    for t1 in s1_from:
                        if not t1.target is s2:
                            skip_only = False
                            break
                        elif t1.target is s2 and t1.name != "skip":
                            skip_only = False
                            break
                        elif (t1.target is s2 and t1.name == "skip"):
                           skip_from_s1.append(t1)

                    if len(skip_from_s1) < 1:
                        continue

                    if not skip_only:
                        continue

                    if skip_from_s1 > 0:
                        to_merge.append(self.states[j])

                if len(to_merge) > 1:
                    # Merge the states together.
                    is_start = False
                    for s in to_merge:
                        if s.is_start:
                            is_start = True
                            break

                    name = "/".join([x.name for x in to_merge])
                    new_s = SM.State(name, is_start)

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

            if not merged:
                break

        self.delete_skip_self_trans()



    #This merges states that have non-contributing in one direction and no transitions in another
    def merge5(self):

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

                    skip_from_s1 = []
                    t_from_s2 = []
                    skip_only = True
                    for t1 in s1_from:
                        for t2 in s2_from:
                            if t2.target is s1:
                                skip_only = False
                                break
                            elif t1.target is s2 and t1.name != "skip":
                                skip_only = False
                                break
                            elif (t1.target is s2 and t1.name == "skip"):
                                skip_from_s1.append(t1)

                    if len(skip_from_s1) < 1:
                        continue

                    if not skip_only:
                        continue

                    if skip_from_s1 > 0:
                        to_merge.append(self.states[j])

                if len(to_merge) > 1:
                    # Merge the states together.
                    is_start = False
                    for s in to_merge:
                        if s.is_start:
                            is_start = True
                            break

                    name = "/".join([x.name for x in to_merge])
                    new_s = SM.State(name, is_start)

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

            if not merged:
                break

        self.delete_skip_self_trans()



    def delete_skip_self_trans(self):

        #Delete skip self-transitions
        m = 0
        while m < len(self.transitions):
            t = self.transitions[m]
            if t.name == "skip" and t.source == t.target:
                del self.transitions[m]
            else:
                m += 1
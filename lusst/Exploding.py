import SM




class State_Machine(SM.State_Machine):

    def slice(self):

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
            a = SM.Transition(t.name, s, t.target, t.is_marked)
            
            if a not in self.transitions:
                self.transitions.append(a)

        i = 0
        while i < len(self.transitions):
            t = self.transitions[i]
            if not t.is_marked:
                del self.transitions[i]
            else:
                i += 1

        self.gc(self.start_states())
        
        self.merge()
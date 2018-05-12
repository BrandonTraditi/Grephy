
def learn_alphabet(input_file):
    ''' 
  Scans for alphabet
    '''
    alphabet = set()
    file = open(input_file,"r")
    line = file.readlines()
    for a in line:
        a = a.replace("\n", "")
        a = a.replace("\r", "")
        for i in a:
            alphabet.add(i)
    file.close()
    return alphabet


def reg_post(expression, alphabet):

    #Converting Regex to PostFix Expression
    
    charStack = []
    char_ato = 0

    alt = 0
    result = []
    for char in expression:
        if char == '*': 
            result.append(char)
        elif char == '+':
            if char_ato == 2: 
                result.append('.')
            char_ato = 0
            alt = alt + 1
        elif char == '(':
            if char_ato == 2:
                result.append('.')
                char_ato = 1
            charStack.append((char_ato, alt))
            char_ato = 0
            alt = 0
        elif char == ')':
            if char_ato == 2: 
                result.append('.')
            if alt: 
                result.append('+'*alt)
            char_ato,alt = charStack.pop()
            char_ato = char_ato + 1

        else:
            if char_ato == 2: 
                result.append('.')
                char_ato = char_ato - 1
            result.append(char)
            char_ato = char_ato + 1

    return result

def post_NFA(post_fix):
    '''
    Converts postfix -> NFA
    Utilizes Thompson's Construction/Algorithim
    
    '''
    class state():
        def __init__(self, state):
            self.state = state
            self.out = None
            self.out1 = None

    class nfa_fragment():
        def __init__(self, start, incomplete):
            self.start = start
            self.out = incomplete

        def incomplete(incomplete_transitions, out):
        # Incomplete to out
        for state in incomplete_transitions:
            if state.state == -1:
                state.out1 = out
            else:
                state.out = out

    def catenation(nfa_frags):
        # based off "." char, combine two NFA Fragments
        frag1 = nfa_frags.pop()
        frag = nfa_frags.pop()
        incomplete(frag.out, frag1.start)
        frag.out = frag1.out
        nfa_frags.append(frag)

    def alt(nfa_frags):
        # incomplete transitions
        frag1 = nfa_frags.pop()
        frag = nfa_frags.pop()
        state = state(-1)
        state.out = frag1.start
        state.out1 = frag.start
        frag.start = state
        frag.out = frag.out + frag1.out
        nfa_frags.append(frag)
    
    def zero_or_more(nfa_frags):
        #loops and splits with incomplete
        frag = nfa_frags.pop()
        state = state(-1)
        state.out = frag.start
        incomplete(frag.out, state)
        frag.out = [state]
        frag.start = state
        nfa_frags.append(frag)
    
    nfa_frags = []

    for char in post_fix:
        if char == '.':
            catenation(nfa_frags)
        elif char == '*':
            zero_or_more(nfa_frags)
        elif char == '+':
            alt(nfa_frags)
        else:
            incomplete(char, nfa_frags)
    if nfa_frags:
        frag = nfa_frags.pop()
        incomplete(frag.out, state(-2))
        return frag.start
    return state(-2)


def NFA_DFA(nfa, alphabet):
    ''' 
    Converts NFA to DFA
    '''
    class dfa_state():
        def __init__(self, states, accept=False):
            #States of DFA from NFA and transitions 
            self.states = states  
            self.transitions = {}  
            self.accept = accept    

    class dfa():
        def __init__(self):
            #Start state + other states
            self.multiState = set() 
            self.startState = None 

        def move(self, char, states):
            ''' 
            Returns NfA states reachable from DFA
            '''
            oneTrans = set()
            for state in states:
                if state.a == char:
                    oneTrans.add(state.out)
            return oneTrans

        def get_state(self, nfa):
            ''' 
            Return DFA state reachable with e
            '''
            nextState = set()
            accept = False
            for state in nfa.copy():
                if state.a is -1:
                    nextState.add(state.out)
                    nextState.add(state.out1)
                    nfa.add(state)
                while nextState:
                    current = nextState.pop()
                    if current.c is -1:
                        nextState.add(current.out)
                        nextState.add(current.out1)
                    else:
                        nfa.add(current)
            # Accepting states
            for state in nfa:
                if state.a == -2:
                    accept = True
            end = dfa_state(nfa,accept)
            return end
        
    dfa = dfa()
    #Finding the start state
    dfa_startState = dfa.get_state(set([nfa]))
    queue.append(dfa_startState)
    dfa.Q.add(dfa_startState)
    dfa.start = dfa_startState
    return dfa



def get_DFA(dfa, infile):
    op = open(infile,"r")
    lines = op.read().splitlines()
    op.close()
    for line in lines:
        state = dfa.start
        for char in line:
            if char in state.transitions:
                state = state.transitions[char]
            else:
                state = None
                break
        if state and state.accept == True:
            print(line)
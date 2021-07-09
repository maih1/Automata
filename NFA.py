class nfa:
    def __init__(self, startState, finalStates, states, alphabet, transitions) -> None:
        """
        Input:
        -startState: start state (s_0)
        -finalStartes: a list final state (F)
        -states: a lists containing the states (S)
        -alphabet: a lists alphabet (sigma)
        -transitions: state transition function (detal)
        """
        self.startState = startState
        self.finalStates = finalStates
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions

def opendFileInput(filename):
    file = open(filename)
    rd = file.readline()
    print(rd,'3')
    startState = ''
    finalStartes = []
    states = []
    alphabet = []
    transitions = dict()

    count = 0

    for i in file:
        data = i.rstrip().split()
        
        if i == 0:
            startState = str(i)
        elif i == 1:
            finalStartes = data
        else:
            states.append(data[0])
            # alphabet.append(data[1])
            transitions.update({'detal ' + str(count): data})
            count += 1
    
    dictData = {
        'startState': startState,
        'finalStartes': finalStartes,
        'states': set(states),
        'alphabet': set(alphabet),
        'transition': transitions
    }

    file.close()
    
    return dictData
print(opendFileInput('t1.txt')) 

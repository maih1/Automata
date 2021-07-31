import InputNFA as dt


class Automaton:
    def __init__(self, startState=None, finalStates=None, states=None, alphabet=None, transitions=None):
        """
        Input:
        -startState: start state (s_0) ''
        -finalStartes: a list final state (F) []
        -states: a lists containing the states (S) []
        -alphabet: a lists alphabet (sigma) []
        -transitions: state transition function (delta) {}
        """
        self.startState = startState
        self.finalStates = finalStates
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions

    # automation data frame
    def automatonForm(self):
        automaton = {
            'startState': self.startState,
            'finalStates': self.finalStates,
            'states': self.states,
            'alphabet': self.alphabet,
            'transitions': self.transitions
        }

        return automaton

    # print data automation
    def printAutomation(self):
        automaton = self.automatonForm()

        # print
        for i in automaton:
            if i == 'transitions':
                print('+ transitions (delta):')
                for j in range(len(automaton[i])):
                    print('\tdelta {}: {}'.format(j, automaton[i][j]))
            else:
                print('+ {}: {}'.format(i, automaton[i]))

# Input data in otomat
def automatonData(filename):
    fileData = dt.opendFileInput(filename)
    ndftData = dt.ndfInput(fileData)

    automaton = Automaton()

    for i in ndftData:
        if i == 'startState':
            automaton.startState = ndftData[i]
        elif i == 'finalStates':
            automaton.finalStates = ndftData[i]
        elif i == 'states':
            automaton.states = ndftData[i]
        elif i == 'alphabet':
            automaton.alphabet = ndftData[i]
        elif i == 'transitions':
            automaton.transitions = ndftData[i]

    return automaton

# find transition of state x
# Tìm hàm chuyển của trạng thái x
def findTransitions(x, transitions, alphabet):
    listFind = []
    check = True
    length = 0
    t = 0
    
    while check == True and length < len(transitions):
        i = transitions[length]
        dataFind = []
        
        if x == i[0]:
            for j in range(1, len(i)):
                dataFind.append(i[j])
            listFind.append(tuple(dataFind))
            t += 1
        
        if t == len(alphabet):
            check = False
        else: length += 1
             
    return listFind
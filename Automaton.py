import Data as dt


class Automaton:
    def __init__(self, startState=None, finalStates=None, states=None, alphabet=None, transitions=None):
        """
        Input:
        -startState: start state (s0) ''
        -finalStartes: a list final state (F) []
        -states: a lists containing the states (S) []
        -alphabet: a lists alphabet (Σ - sigma) []
        -transitions: state transition function (δ -delta) []
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

    def printTran(self):
        print('\t{:{width}}'.format('S\\Σ', width=20), end='')

        for i in self.alphabet:
            print('{:{width}}'.format(i, width=20,), end='')
        
        print()
        s_states = getStartTranStates(self.transitions)
        for i in s_states:
            print('\t{:{width}}'.format('{}'.format(i), width=20), end='')

            for al in self.alphabet:
                j = 0
                check_tran = True
                while check_tran == True and j < len(self.transitions):
            # for j in self.transitions:
                    if i == self.transitions[j][0] and al == self.transitions[j][1]:
                        if len(self.transitions[j]) == 2:
                            print('{:{width}}'.format('-', width=20,), end='')
                        elif len(self.transitions[j]) > 3:
                            p = []
                            for k in range(2, len(self.transitions[j])):
                                p.append(self.transitions[j][k])
                            print('{:{width}}'.format('{}'.format(p), width=20,), end='')
                        else:
                            print('{:{width}}'.format('{}'.format(self.transitions[j][2]), width=20,), end='')

                        check_tran = False
                    else: j += 1
            print()


    # print data automation
    def printAutomation(self):
        automaton = self.automatonForm()

        # print
        for i in automaton:
            if i == 'startState' and isinstance(automaton[i], list):
                print('+ {}: {}'.format(i, automaton[i][0]))
            elif i == 'transitions':
                print('+ transitions (delta):')
                # In dạng bảng
                self.printTran()

                # In dạng hàm
                # for j in range(len(automaton[i])):
                #     print('\tdelta {}: {}'.format(j, automaton[i][j]))
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

# Lay trang thai bat dau
def getStartTranStates(trans):
    start_state_trans = []

    for i in trans:
        if i[0] not in start_state_trans:
            start_state_trans.append(i[0])
    
    return start_state_trans

# Lay trạng thái chuyển tiếp
def getNextTransStates(trans):
    next_states_trans = []

    for i in trans:
        if len(i) <= 2:
            pass
        elif len(i) == 3:
            next_states_trans.append[[i[2]]]
        else:
            states = []
            
            for j in range(2, len(i)):
                states.append(i[j])
            
            if states not in next_states_trans:
                next_states_trans.append(states)
    
    return next_states_trans
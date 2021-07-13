import math
import Input as ip


class Automaton:
    def __init__(self, startState=None, finalStates=None, states=None, alphabet=None, transitions=None):
        """
        Input:
        -startState: start state (s_0) ''
        -finalStartes: a list final state (F) []
        -states: a lists containing the states (S) []
        -alphabet: a lists alphabet (sigma) []
        -transitions: state transition function (detal) {}
        """
        self.startState = startState
        self.finalStates = finalStates
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions


# Input data in otomat
def automatonData(filename):
    fileData = ip.opendFileInput(filename)
    ndftData = ip.ndfInput(fileData)

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


# find Unreachable State
def findUnreachableState(states, startState, transitions):
    state_unreachable = []

    states = [i for i in states if i != startState]

    for i in states:
        check = False
        for j in range(len(transitions)):
            nextStates = transitions[j][2]
            if i == nextStates and check == False:
                check = True
        if check == False:
            state_unreachable.append(i)

    return state_unreachable


# find non-loop transition of state x
def findTransitions(x, transitions):
    listFind = []

    for i in transitions:
        dataFind = []
        if x == i[0]:
            dataFind.append(i[1])
            dataFind.append(i[2])
            listFind.append(tuple(dataFind))

    return listFind


# Get the next state over a number of transition
def getNextstate(state, transitions, alphabet):
    listNextState = []
    listNextTran = []

    # generate 2 transition with alphabet
    for i in range(len(alphabet)):
        nextTran = [alphabet[i], alphabet[i]]
        listNextTran.append(nextTran)

    # get next state
    for i in listNextTran:
        nextState = state
        while len(i) > 0:
            check = True
            for j in transitions:
                if check == True and nextState == j[0] and i[0] == j[1]:
                    nextState = j[2]
                    i.pop()
                    check = False

        listNextState.append(nextState)

    return listNextState


# Get equivalence states
def getEquivalenceStates(states, startState, finalStates, transitions, alphabet):
    # unreachable state
    state_unreachable = findUnreachableState(states, startState, transitions)
    count = 1

    # list equivalence states
    listEquivalenceStates = []

    # remove unreachable state in states
    for i in state_unreachable:
        states.remove(i)

    # find equivalence states
    for i in states:
        # get transition of i
        tran_i = findTransitions(i, transitions)

        for j in range(count, len(states)):
            # get transition of j
            tran_j = findTransitions(states[j], transitions)
            check = True

            # state i is final state and state j is not final state, contra
            if (i in finalStates and states[j] not in finalStates) or (i not in finalStates and states[j] in finalStates):
                pass

            # state i, j is final state
            # elif (i in finalStates and states[j] in finalStates):
            #     equivalenceStates = []
            #     equi_state = []
            #     equi_state.append(i)
            #     equi_state.append(states[j])
            #     equivalenceStates.append(equi_state)
            #     equivalenceStates.append(k)
            #     listEquivalenceStates.append(equivalenceStates)

            # state i, j is not final state
            else:
                nextTran_p = getNextstate(i, transitions, alphabet)
                nextTran_q = getNextstate(states[j], transitions, alphabet)
                for k in tran_i:
                    # next state of state i equal next state of state j
                    if k in tran_j and check == True and nextTran_p == nextTran_q:
                        equivalenceStates = []
                        equi_state = []
                        equi_state.append(i)
                        equi_state.append(states[j])
                        equivalenceStates.append(equi_state)
                        equivalenceStates.append(k)
                        listEquivalenceStates.append(equivalenceStates)
                        check = False
        count += 1

    return listEquivalenceStates


# merge states together to a destination
def mergeState(listStateEqui):
    newListStateEqui = []
    j = 0

    # browse in this list equivalence states
    while len(listStateEqui) != 0:
        i = 0
        check = True
        start = listStateEqui[0]
        # create new list equivalence states
        newListStateEqui.append(listStateEqui[i])

        while check == True:
            equivalenceStates = []

            # check next status is same
            if i <= len(listStateEqui)-1 and start[1] == listStateEqui[i][1]:
                # union of two states
                union_state = list(set(start[0]) | set(listStateEqui[i][0]))
                equivalenceStates.append(sorted(union_state))
                equivalenceStates.append(start[1])
                newListStateEqui[j] = equivalenceStates
                start = newListStateEqui[j]
                listStateEqui.pop(i)
            elif i < len(listStateEqui)-1:
                i += 1
            else:
                check = False

        j += 1

    return newListStateEqui


# list equivalence states
def dfaMinimization(states, startState, finalStates, transitions, alphabet):
    getListEquivalenceStates = getEquivalenceStates(
        states, startState, finalStates, transitions, alphabet)
    print(getListEquivalenceStates)
    list_equi = mergeState(getListEquivalenceStates)
    print(list_equi)
    dfa = Automaton()

    # new start state
    check = True
    start_index = 0
    while check == True and start_index <= len(list_equi):
        if start_index < len(list_equi) and startState in list_equi[start_index][0] and check == True:
            dfa.startState = list_equi[start_index][0]
            check = False
        elif start_index == len(list_equi) - 1 or len(list_equi) == 0:
            dfa.startState = startState
            check = False
        else:
            start_index += 1

    # new final states
    dfa.finalStates = []

    for i in finalStates:
        check_final = True
        final_index = 0

        while check_final == True and final_index <= len(list_equi):
            if final_index < len(list_equi) and i in list_equi[final_index][0]:
                dfa.finalStates.append(list_equi[final_index][0])
                check_final = False
            elif final_index == len(list_equi) - 1 or len(list_equi) == 0:
                dfa.finalStates.append(i)
                check_final = False
            else:
                final_index += 1

    

    return dfa


a = automatonData('t1.txt')
# print(a.alphabet)
f = findTransitions('a', a.transitions)
# print(f)

m = getEquivalenceStates(a.states, a.startState,
                         a.finalStates, a.transitions, a.alphabet)
# print(m)

u = mergeState(m)
# print(u)

# getNextstate('b', a.states, a.transitions, a.alphabet)

m = dfaMinimization(a.states, a.startState, a.finalStates,
                    a.transitions, a.alphabet)
print(m.startState)
print(m.finalStates)

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


def automatonData(filename):
    # Input data in otomat
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


def findUnreachableState(states, startState, transitions):
    # find Unreachable State
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


def findTransitions(x, transitions):
    # find non-loop transition of state x
    listFind = []

    for i in transitions:
        dataFind = []
        if x == i[0] and x != i[2]:
            dataFind.append(i[1])
            dataFind.append(i[2])
            listFind.append(tuple(dataFind))

    return listFind


def mergeState(listStateEqui):
    # merge states together to a destination
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

        # else:
        #     j += 1
        #     # newListStateEqui[j] = listState[i]
        #     newListStateEqui.append(listState[i])
        #     start = newListStateEqui[j]
        #     listState.pop(i)

    return newListStateEqui


def getEquivalenceStates(states, startState, finalStates, transitions):
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
            elif (i in finalStates and states[j] in finalStates):
                equivalenceStates = []
                equi_state = []
                equi_state.append(i)
                equi_state.append(states[j])
                equivalenceStates.append(equi_state)
                equivalenceStates.append(k)
                listEquivalenceStates.append(equivalenceStates)

            # state i, j is not final state
            else:
                for k in tran_i:
                    # next state of state i equal next state of state j
                    if k in tran_j and check == True:
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


# def dfaMinimization(states, startState, finalStates, transitions):
#     # list equivalence states
#     listEquivalenceStates = getEquivalenceStates(
#         states, startState, finalStates, transitions)
#     dfa = Automaton()

#     # new start state
#     check = True
#     for i in listEquivalenceStates:
#         print(i)
#         if startState in i and check == True:
#             dfa.startState = i
#             check = False
#         else:
#             dfa.startState = startState

#     return dfa


a = automatonData('t1.txt')
# print(a.finalStates)
f = findTransitions('a', a.transitions)
# print(f)

m = getEquivalenceStates(a.states, a.startState, a.finalStates, a.transitions)
# print(m)

u = mergeState(m)
print(u)

# m = dfaMinimization(a.states, a.startState, a.finalStates, a.transitions)
# print(m.startState)

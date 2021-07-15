import math
import Data as dt


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


# find transition of state x
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
# bug to to tototototo
def getNextstate(trans, state, transitions, alphabet):
    listNextState = []
    listNextTran = []

    # generate 2 transition with alphabet
    for i in range(len(alphabet)):
        nextTran = [trans, alphabet[i], alphabet[i]]
        # nextTran = [alphabet[i], alphabet[i]]

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
    temp_states = states.copy()
    for i in state_unreachable:
        temp_states.remove(i)

    # find equivalence states
    for i in temp_states:
        # get transition of i
        tran_i = findTransitions(i, transitions)

        for j in range(count, len(temp_states)):
            # get transition of j
            tran_j = findTransitions(temp_states[j], transitions)
            check = True

            # state i is final state and state j is not final state, contra
            if (i in finalStates and temp_states[j] not in finalStates) or \
            (i not in finalStates and temp_states[j] in finalStates):
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
                for k in tran_i:
                    # next state of state i equal next state of state j
                    if k in tran_j and check == True:
                        trans = [k]
                        intersection_trans = list(set(trans) & set(tran_j))
                        
                        # check the next state over a number of transition
                        nextTran_p = getNextstate(intersection_trans[0][0], i, transitions, alphabet)
                        nextTran_q = getNextstate(intersection_trans[0][0], temp_states[j], transitions, alphabet)

                        if nextTran_p == nextTran_q:
                            equivalenceStates = []
                            equi_state = []
                            equi_state.append(i)
                            equi_state.append(temp_states[j])
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
def dfaMinimization( startState, finalStates, states, alphabet, transitions):
    # Get equivalence states
    getListEquivalenceStates = getEquivalenceStates(
        states, startState, finalStates, transitions, alphabet)

    # list states together to a destination
    list_equi = mergeState(getListEquivalenceStates)

    # unreachable state
    state_unreachable = findUnreachableState(states, startState, transitions)

    # create new automat/dfa
    dfa = Automaton()

    # new start state
    if len(list_equi) == 0:
        dfa.startState = startState
    else:
        check_start = True
        start_index = 0
        while check_start == True and start_index <= len(list_equi):
            if start_index < len(list_equi) and startState in list_equi[start_index][0] and check_start == True:
                dfa.startState = tuple(list_equi[start_index][0])
                check_start = False
            elif start_index < len(list_equi) - 1:
                start_index += 1
            else:
                check_start = False

    # new final states
    if len(list_equi) == 0:
        dfa.finalStates = finalStates
    else:
        dfa_final = []

        for i in finalStates:
            check_final = True
            final_index = 0

            while check_final == True and final_index <= len(list_equi):
                if final_index < len(list_equi) and i in list_equi[final_index][0]:
                    dfa_final.append(tuple(list_equi[final_index][0]))
                    check_final = False
                else:
                    if final_index == len(list_equi) - 1 or len(list_equi) == 0:
                        dfa_final.append(i)
                        check_final = False
                    else:
                        final_index += 1
            
        dfa.finalStates = list(set(dfa_final))
    
    # new dfa states
    temp_states = states.copy()
    for i in state_unreachable:
        temp_states.remove(i)

    dfa.states = temp_states

    # new dfa alphabet
    dfa.alphabet = alphabet

    # new transitions
    dfa.transitions = []

    # if the list is empty dfa transition equals input automat transition
    if len(list_equi) == 0:
        dfa.transitions = transitions.copy()
    else:
        # add to transition equivalence states dfa transition 
        temp_trandfa = []
        for i in list_equi:
            new_tran = [tuple(i[0]), i[1][0], i[1][1]]
            temp_trandfa.append(new_tran)

        temp_dfa_tran = temp_trandfa.copy()
        temp_tran = transitions.copy()
        check_tran = True

        # remove unreachable state transitions
        for i in state_unreachable:
            k = 0
            while check_tran == True:
                if k < len(temp_tran) and i == temp_tran[k][0]:
                    temp_tran.pop(k)
                else:
                    if k < len(temp_tran) - 1:
                        k += 1
                    else:
                        check_tran = False

        # convert final state and delete transition in states together to a destination
        for i in range(len(temp_dfa_tran)):
            # if dfa.transitions[i][2] in temp_dfa_tran[i][0]:
            #     dfa.transitions[i][2] = temp_dfa_tran[i][0]

            k = 0
            check_tran = True
            while check_tran == True:
                if k < len(temp_tran) and \
                temp_tran[k][0] in temp_dfa_tran[i][0] and \
                temp_tran[k][1] == temp_dfa_tran[i][1] and \
                temp_tran[k][2] == temp_dfa_tran[i][2]:
                    temp_tran.pop(k)
                else:
                    if k < len(temp_tran) and temp_tran[k][2] in temp_dfa_tran[i][0]:
                        temp_tran[k][2] = temp_dfa_tran[i][0]
                    if k < len(temp_tran) and temp_tran[k][0] in temp_dfa_tran[i][0]:
                        temp_tran[k][0] = temp_dfa_tran[i][0]
                    if k < len(temp_tran) - 1:
                        k += 1
                    else:
                        check_tran = False

        # remove transition loop
        count = 1
        for i in temp_tran:
            lenght = len(temp_tran) - 1
            for j in range(count, lenght):
                if i == temp_tran[j]:
                    temp_tran.pop(j)
                lenght = len(temp_tran) - 1
            count += 1

        for i in range(len(temp_dfa_tran)):
            for j in range(len(temp_dfa_tran)):
                if temp_trandfa[j][2] in temp_dfa_tran[i][0]:
                    temp_trandfa[j][2] = temp_dfa_tran[i][0]
            dfa.transitions.append(temp_dfa_tran[i])

        # add to transition in dfa transition
        for i in temp_tran:
            dfa.transitions.append(i)

    return dfa

# if __name__ == '__main__':
print( "Automation input: " )
# automaton = automatonData('test1.txt')
# automaton = automatonData('test2.txt')
# automaton = automatonData('test3.txt')
automaton = automatonData('test4.txt')
# automaton.printAutomation()

print('----------------------------------------------')

print( "Deterministic Finite Automaton Minimization" )
dfa = dfaMinimization(automaton.startState, automaton.finalStates, automaton.states, automaton.alphabet, automaton.transitions)
dfa.printAutomation()
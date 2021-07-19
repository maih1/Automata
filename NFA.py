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

# remove unreachable state in states
def removeUnreachableState(states, state_unreachable):
    temp_states = states.copy()
    for i in state_unreachable:
        temp_states.remove(i)

    return temp_states

# remove unreachable state transitions
def removeUnreachableTransition(state_unreachable, transitions):
    temp_tran = transitions.copy()
    check_tran = True
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
    return temp_tran

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
    temp_states = removeUnreachableState(states, state_unreachable)

    # temp_states = states.copy()
    # for i in state_unreachable:
    #     temp_states.remove(i)

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

                        # if nextTran_p == nextTran_q:
                        equivalenceStates = []
                        equi_state = []
                        equi_state.append(i)
                        equi_state.append(temp_states[j])
                        equivalenceStates.append(equi_state)
                        equivalenceStates.append(k)
                        listEquivalenceStates.append(equivalenceStates)
                        check = False
        count += 1
    
    print(listEquivalenceStates)

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
        # for i in state_unreachable:
        #     k = 0
        #     while check_tran == True:
        #         if k < len(temp_tran) and i == temp_tran[k][0]:
        #             temp_tran.pop(k)
        #         else:
        #             if k < len(temp_tran) - 1:
        #                 k += 1
        #             else:
        #                 check_tran = False
        temp_tran = removeUnreachableTransition(state_unreachable, transitions)

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
            length = len(temp_tran) - 1
            for j in range(count, length):
                if i == temp_tran[j]:
                    temp_tran.pop(j)
                length = len(temp_tran) - 1
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


# check if 2 arrays are equal
def checkListEqual(ls1, ls2):
    count = 0

    while True:
        if count < len(ls1) and ls1[count] in ls2:
            count += 1
        elif count == len(ls1):
            return True
        else:
            return False

def stateSamePartition(ls_temp):
# find state with the same partition
    ls_same_partition = []
    count = 1
    for i in ls_temp:
        temp_list = []
        for j in range(count, len(ls_temp)):
            print(ls_temp[j])
            for k in i[1]:
                if k in ls_temp[j][1]:
                    temp_list.append(i[0])
                    temp_list.append(ls_temp[j][0])

        if len(temp_list) == 0:
            check_same = ls_same_partition.copy()
            for k in check_same:
                if len(k) != 1 and i[0] not in k:
                    ls_same_partition.append([i[0]])
        elif len(temp_list) != 0:
            ls_same_partition.append(list(set(temp_list)))
        count += 1

    return ls_same_partition

# merge states together to a destination
def mergeState2(listState):
    # new_listState = []
    # count = 1

    # for i in listState:
    #     for j in range(count, len(listState)):
    #             union_state = list(set(i) | set(j))

    newListStateEqui = []
    j = 0

    # browse in this list equivalence states
    # while len(listState) != 0:
    i = 0
    check = True
    start = listState[0]
    # create new list equivalence states
    newListStateEqui.append(listState[i])

    while len(listState) != 0:
        # equivalenceStates = []

        # check next status is same
        if i <= len(listState)-1:
            
            # equivalenceStates.append(sorted(union_state))
            check_union = list(set(start) & set(listState[i]))
            if len(check_union) == 0:
                j += 1
                newListStateEqui.append(listState[i])
            else:
                # union of two states
                union_state = list(set(start) | set(listState[i]))
                newListStateEqui[j] = sorted(union_state)
                
            start = newListStateEqui[j]
            listState.pop(i)
        elif i < len(listState)-1:
            i += 1
        # else:
        #     check = False

    # j += 1
    # lỗi ở đây
    return newListStateEqui

def sortKey(tuple):
  return tuple[0]

def stateSame(ls_temp, ls_temp2, ls_state):
# find state with the same partition
    ls_same_partition = []
    count = 1
    
    # for i in ls_temp:
    #     temp_list = []
    #     for j in range(count, len(ls_temp)):
    #         i_j = ls_temp[j]
    #         i[1].sort(key=sortKey)
    #         i_j[1].sort(key=sortKey)
    #         count_ls_state = 0
    #         check_ls = True
    #         temp_check_list1 = 0
           
    #         while check_ls == True and count_ls_state < len(ls_state):
    #             # print(k)
    #             temp_check_list2 = 0

    #             for k in range(len(i[1])):
    #                 a = i[1][k][1]
    #                 b = i_j[1][k][1]
    #                 c = ls_state[count_ls_state]
    #                 if i[1][k][1] in ls_state[count_ls_state] and i_j[1][k][1] in ls_state[count_ls_state]:
    #                     # temp_list.append(i[0])
    #                     # temp_list.append(i_j[0])
    #                 # else 
    #                     temp_check_list1 += 1
    #                     temp_check_list2 += 1
    #             if temp_check_list2 == len(i[1]):
    #                 temp_list.append(i[0])
    #                 temp_list.append(i_j[0])
    #                 ls_same_partition.append([i[0], i_j[0]])
    #                 check_ls = False
    #             elif temp_check_list1 == len(i[1]):
    #                 check_ls = False
    #             else:
    #                 count_ls_state += 1
    #         if temp_check_list1 == len(i[1]) and temp_check_list1 != temp_check_list2:
    #             temp_list.append(i[0])
    #             temp_list.append(i_j[0])
    #             ls_same_partition.append(temp_list)
    #         # elif temp_check_list1 < len(i[1]):
    #         #     if len(ls_same_partition) == 0:
    #         #         ls_same_partition.append([i[0]])
    #         #     elif j == len(ls_temp) - 1:
    #         #         ls_same_partition.append([i_j[0]])
    #         #     else:
    #         #         check_same = ls_same_partition.copy()
                    
    #         #         for k in check_same:
    #         #             print(k)
    #         #             print(i[0])
    #         #             print(i_j[0] not in k)
    #         #             if i[0] not in k:
    #         #                 ls_same_partition.append([i[0]])
    #     check_same = ls_same_partition.copy()
    #     if i[0] not in temp_list:
    #         ls_same_partition.append([i[0]])
                    
    #     # for k in check_same:
    #     #     print(k)
    #     #     print(i[0])
    #     #     print(i_j[0] not in [k for k in check_same] )
    #     #     if i[0] not in k:
    #     #         ls_same_partition.append([i[0]])

    #     # for k in ls_same_partition:
    #     #     print(k)
    #     #     print(i[0])
    #     #     if i[0] not in k:
    #     #         ls_same_partition.append(list(i[0]))  
    #     count += 1
        
    # print(ls_same_partition)
    # new = mergeState2(ls_same_partition)
    # print(new)

    # lỗi hợp hai list
    # Định dùng pop
    ls_temp2_copy = ls_temp2.copy()
    i = 0
    while len(ls_temp2_copy) > 0:
    # for i in ls_temp2:
        ii = ls_temp2_copy[i]
        temp_list = [ii[0]]
        j = 1
        while j < len(ls_temp2_copy): 
        # for j in range(count, len(ls_temp2)):
            jj = ls_temp2_copy[j]
            ii[1].sort(key=sortKey)
            jj[1].sort(key=sortKey)
            count_ls_state = 0
            check_ls = True
            temp_check_list1 = 0
           
            while check_ls == True and count_ls_state < len(ls_state):
                # print(k)
                temp_check_list2 = 0

                for k in range(len(ii[1])):
                    a = ii[1][k][1]
                    b = jj[1][k][1]
                    c = ls_state[count_ls_state]
                    if ii[1][k][1] in ls_state[count_ls_state] and jj[1][k][1] in ls_state[count_ls_state]:
                        # temp_list.append(i[0])
                        # temp_list.append(i_j[0])
                    # else 
                        temp_check_list1 += 1
                        temp_check_list2 += 1
                if temp_check_list2 == len(ii[1]):
                    # temp_list.append(ii[0])
                    temp_list.append(jj[0])
                    ls_temp2_copy.pop(j)
                    # ls_same_partition.append([i[0], i_j[0]])
                    check_ls = False
                elif temp_check_list1 == len(ii[1]):
                    check_ls = False
                else:
                    count_ls_state += 1
            
            if temp_check_list1 == len(ii[1]) and temp_check_list1 != temp_check_list2:
                # temp_list.append(i[0])
                temp_list.append(jj[0])
                ls_temp2_copy.pop(j)
                # ls_same_partition.append(temp_list)
            elif temp_check_list1 != len(ii[1]):
                j += 1

        if len(temp_list) == 1:
            ls_same_partition.append([ii[0]])           
        elif len(temp_list) != 1:
            ls_same_partition.append(sorted(list(set(temp_list))))
        count += 1
        # i += 1
        ls_temp2_copy.pop(i)
                
    # print(ls_same_partition)
    # new = mergeState2(ls_same_partition)
    # print(new)
    return ls_same_partition

# bug to tot oooooooooooooooooooooooooooo
def nextTrans(startState, finalStates, states, alphabet, transitions):
    # unreachable state
    state_unreachable = findUnreachableState(states, startState, transitions)
    temp_states = removeUnreachableState(states, state_unreachable)
    
    count = 0
    liststate = []
    ls_00 = finalStates
    ls_01 = [i for i in temp_states if i not in  finalStates]
    ls_0 = [ls_00, ls_01]
    
    liststate.append(ls_0)

    temp_liststate = liststate.copy()
    
    ls_not_final = []
    ls_full_final = [] 
    ls_temp = []
    ls_temp2 = []

    for i in temp_liststate[0][1]:
        list_next_state = []
        list_next_trans = []
        
        for j in transitions:
            if i == j[0]:
                list_next_state.append(j[2])
                list_next_trans.append((j[1], j[2]))
        
        list_check_state = [k for k in list_next_state if k in finalStates]
        
        if len(list_check_state) == 0:
            ls_not_final.append(i)
        elif len(list_check_state) == len(list_next_state):
            ls_full_final.append(i)
        else: 
            ls_temp.append(i)   
            ls_temp2.append((i, list_next_trans))      
    # count = 1
    # ls_temp_lists_final = []
    # # find state with the same partition
    # for i in ls_temp2:
    #     temp_list = []
    #     temp_i = ''
    #     for j in range(count, len(ls_temp2)):
    #         print(ls_temp2[j])
    #         for k in i[1]:
    #             if k in ls_temp2[j][1]:
    #                 temp_list.append(i[0])
    #                 temp_list.append(ls_temp2[j][0])
    #         temp_i = ls_temp2[j][0]
    #     if len(temp_list) == 0:
    #         for k in ls_temp_lists_final:
    #             if i[0] not in k:
    #                 ls_temp_lists_final.append(list(i[0]))
    #     elif len(temp_list) != 0:
    #         ls_temp_lists_final.append(list(set(temp_list)))
    #     count += 1
    ls_temp_lists_final = stateSamePartition(ls_temp2)

    ls_temp_lists_final.append(ls_00)
    ls_temp_lists_final.append(ls_full_final)
    ls_temp_lists_final.append(ls_not_final)

    ls_1 = ls_temp_lists_final.copy()
    # remove empty list 
    if [] in ls_1:
        ls_1.remove([])
    liststate.append(ls_1)
    
    if checkListEqual(liststate[0], liststate[1]) == True:
        return liststate[0]
    else:
        check = True
        while check:
            new_temp_list = []
            length = len(liststate) - 1
            print(liststate[length])

            for i in liststate[length]:
                temp_i = []
                temp_tran_i = []
                if len(i) > 2:                                      
                    for j in i:
                        temp_i.append(j)
                        temp_tran_i.append((j, findTransitions(j, transitions)))
                
                if len(temp_tran_i) == 0:
                    new_temp_list.append(i)
                # xu ly tempa_tran_i
                else: 
                    # a = stateSamePartition(tempa_tran_i)
                    for j in stateSame(temp_i, temp_tran_i, liststate[length]):
                        new_temp_list.append(j)
            
            # check if 2 arrays are equal
            if checkListEqual(liststate[length], new_temp_list) == True:
                return liststate[length]
            else:
                liststate.append(new_temp_list)

            #  viet laij ham mergeState

    
#     return ls_same_partition
# if __name__ == '__main__':
print( "Automation input: " )
# automaton = automatonData('test1.txt')
# automaton = automatonData('test2.txt')
automaton = automatonData('test3.txt')
# automaton = automatonData('test4.txt')
# automaton.printAutomation()

nt = nextTrans(automaton.startState, automaton.finalStates, automaton.states, automaton.alphabet, automaton.transitions)

print('----------------------------------------------')

print( "Deterministic Finite Automaton Minimization" )
dfa = dfaMinimization(automaton.startState, automaton.finalStates, automaton.states, automaton.alphabet, automaton.transitions)
dfa.printAutomation()
# bug
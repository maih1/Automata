import math
import Data as dt
import Automaton as at


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


# check if two arrays are equal
def checkListEqual(ls1, ls2):
    count = 0

    while True:
        if count < len(ls1) and ls1[count] in ls2:
            count += 1
        elif count == len(ls1):
            return True
        else:
            return False


# find state with the same partition
def stateSamePartition(ls_temp_copy):
    # new list same partition
    ls_same_partition = []
    ls_temp_copy = ls_temp_copy.copy()
    i = 0

    # check first place with the rest
    while len(ls_temp_copy) > 0:
        ii = ls_temp_copy[i]
        temp_list = [ii[0]]
        j = 1

        while j < len(ls_temp_copy):
            jj = ls_temp_copy[j]
            count = 0

            for k in ii[1]:
                if k in jj[1]:
                    count += 1

            if count != 0:
                temp_list.append(jj[0])
                ls_temp_copy.pop(j)
            else:
                j += 1

        if len(temp_list) == 1:
            ls_same_partition.append([ii[0]])
        elif len(temp_list) != 1:
            ls_same_partition.append(sorted(list(set(temp_list))))

        ls_temp_copy.pop(i)

    return ls_same_partition

# Sort key
def sortKey(tuple):
    return tuple[0]


# find state with same partition nth time
def stateSame(ls_temp, ls_temp2, ls_state):
    ls_same_partition = []
    ls_temp2_copy = ls_temp2.copy()
    i = 0

    # check first place with the rest
    while len(ls_temp2_copy) > 0:
        ii = ls_temp2_copy[i]
        temp_list = [ii[0]]
        j = 1

        while j < len(ls_temp2_copy):
            jj = ls_temp2_copy[j]
            ii[1].sort(key=sortKey)
            jj[1].sort(key=sortKey)
            count_ls_state = 0
            check_ls = True
            temp_check_list1 = 0

            # check 2 state in list state
            while check_ls == True and count_ls_state < len(ls_state):
                temp_check_list2 = 0

                for k in range(len(ii[1])):
                    
                    # test transition function with classes of subclass
                    if ii[1][k][1] in ls_state[count_ls_state] and jj[1][k][1] in ls_state[count_ls_state]:
                        temp_check_list1 += 1
                        temp_check_list2 += 1

                # all transfer functions (alphabets) of 2 states belong to the same class of partition, 
                # the 2 states create a new class in the new partition
                if temp_check_list2 == len(ii[1]):
                    temp_list.append(jj[0])
                    ls_temp2_copy.pop(j)
                    check_ls = False
                # check next partition
                elif temp_check_list1 == len(ii[1]):
                    check_ls = False
                else:
                    count_ls_state += 1

            # each transfer function (alphabet) of 2 states belonging to the same class in the partition,
            # the 2 states create a new class in the new partition        
            if temp_check_list1 == len(ii[1]) and temp_check_list1 != temp_check_list2:
                temp_list.append(jj[0])
                ls_temp2_copy.pop(j)
            elif temp_check_list1 != len(ii[1]):
                j += 1
        # add new class to partition
        if len(temp_list) == 1:
            ls_same_partition.append([ii[0]])
        elif len(temp_list) != 1:
            ls_same_partition.append(sorted(list(set(temp_list))))

        ls_temp2_copy.pop(i)

    return ls_same_partition


# Get equivalence states 
def getPartition(startState, finalStates, states, alphabet, transitions):
    # unreachable state
    # remove unreachable state in states
    state_unreachable = findUnreachableState(states, startState, transitions)
    temp_states = removeUnreachableState(states, state_unreachable)

    # create partition
    liststate = []
    ls_00 = finalStates
    ls_01 = [i for i in temp_states if i not in finalStates]
    ls_0 = [ls_00, ls_01]

    # add first partition
    liststate.append(ls_0)

    temp_liststate = liststate.copy()

    # class does not reach the end state
    ls_not_final = []

    # class only to end state
    ls_full_final = []

    # class includes both finished and unterminated
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
        
        # add does not reach the end state
        if len(list_check_state) == 0:
            ls_not_final.append(i)
        # add class only to end state
        elif len(list_check_state) == len(list_next_state):
            ls_full_final.append(i)
        # add class includes both finished and unterminated
        else:
            ls_temp.append(i)
            ls_temp2.append((i, list_next_trans))

    # new subclasses including completed and unfinished classes
    # add subclasses for 2nd partition 
    ls_temp_lists_final = stateSamePartition(ls_temp2)
    ls_temp_lists_final.append(ls_00)
    ls_temp_lists_final.append(ls_full_final)
    ls_temp_lists_final.append(ls_not_final)

    # create second  partition
    ls_1 = ls_temp_lists_final.copy()
    
    # remove empty list
    if [] in ls_1:
        ls_1.remove([])
    
    # add second  partition
    liststate.append(ls_1)

    # check and find the next partitions
    if checkListEqual(liststate[0], liststate[1]) == True:
        return liststate[0]
    else:
        check = True
        while check:
            new_temp_list = []
            length = len(liststate) - 1

            # find the new partition from the previous partition
            for i in liststate[length]:
                temp_i = []
                temp_tran_i = []

                # find new subclasses for classes with more than 2 states
                if len(i) > 2:
                    for j in i:
                        temp_i.append(j)
                        temp_tran_i.append(
                            (j, at.findTransitions(j, transitions, alphabet)))

                # For subclasses less than 2 states, 
                # new partitions can be added
                if len(temp_tran_i) == 0:
                    new_temp_list.append(i)
                
                # handle finding new subclasses for classes with more than 2 states
                else:
                    # a = stateSamePartition(tempa_tran_i)
                    for j in stateSame(temp_i, temp_tran_i, liststate[length]):
                        new_temp_list.append(j)

            # check if 2 arrays are equal
            # If 2 consecutive partitions are equal, return that partition
            # if not, repeat find the new partition from the previous partition
            if checkListEqual(liststate[length], new_temp_list) == True:
                return liststate[length]
            else:
                liststate.append(new_temp_list)


# Get equivalence states
def getListEquivalenceStates(listState):
    listEqui = []
    for i in listState:
        if len(i) > 1:
            listEqui.append(tuple(i))

    return listEqui


# list equivalence states
def dfaMinimization(startState, finalStates, states, alphabet, transitions):
    # Get equivalence states
    listState = getPartition(startState, finalStates,
                          states, alphabet, transitions)

    # list states together to a destination
    list_equi = getListEquivalenceStates(listState)

    # unreachable state
    state_unreachable = findUnreachableState(states, startState, transitions)

    # create new automat/dfa
    dfa_min = at.Automaton()

    # new start state
    if len(list_equi) == 0:
        dfa_min.startState = startState
    else:
        check_start = True
        start_index = 0
        
        while check_start == True and start_index <= len(list_equi):
            if start_index < len(list_equi) and startState in list_equi[start_index] and check_start == True:
                dfa_min.startState = tuple(list_equi[start_index])
                check_start = False
            elif start_index < len(list_equi) - 1:
                start_index += 1
            else:
                check_start = False
        if dfa_min.startState == None:
            dfa_min.startState = startState

    # new final states
    if len(list_equi) == 0:
        dfa_min.finalStates = finalStates
    else:
        dfa_final = []

        for i in finalStates:
            check_final = True
            final_index = 0

            while check_final == True and final_index <= len(list_equi):
                if final_index < len(list_equi) and i in list_equi[final_index]:
                    dfa_final.append(tuple(list_equi[final_index]))
                    check_final = False
                else:
                    if final_index == len(list_equi) - 1 or len(list_equi) == 0:
                        dfa_final.append(i)
                        check_final = False
                    else:
                        final_index += 1

        dfa_min.finalStates = list(set(dfa_final))

    # new dfa states
    temp_states = states.copy()
    for i in state_unreachable:
        temp_states.remove(i)

    dfa_min.states = temp_states

    # new dfa alphabet
    dfa_min.alphabet = alphabet

    # new transitions
    dfa_min.transitions = []

    # if the list is empty dfa transition equals input automat transition
    if len(list_equi) == 0:
        dfa_min.transitions = transitions.copy()
    else:
        temp_list_equi = list_equi.copy()
        temp_tran = removeUnreachableTransition(state_unreachable, transitions)

        # convert final state and delete transition in states together to a destination
        for i in temp_list_equi:
            for j in temp_tran:
                if j[0] in i:
                    j[0] = i
                if j[2] in i:
                    j[2] = i

        # remove transition loop
        i = 0
        while i < len(temp_tran) - 1:
            ii = temp_tran[i]
            j = i + 1
            while j < len(temp_tran):
                jj = temp_tran[j]

                if ii == jj:
                    temp_tran.pop(j)
                else: j += 1
            i += 1

        # add to transition in dfa transition
        for i in temp_tran:
            dfa_min.transitions.append(i)

    return dfa_min


if __name__ == '__main__':
    print("Automation input: ")
    # automaton = at.automatonData('test1.txt')

    automaton = at.automatonData('./Data/testdfamin1.txt')
    # automaton = at.automatonData('./Data/testdfamin2.txt')
    # automaton = at.automatonData('./Data/testdfamin3.txt')
    # automaton = at.automatonData('./Data/testdfamin4.txt')
    automaton.printAutomation()

    print('----------------------------------------------')

    print("Deterministic Finite Automaton Minimization")
    dfa = dfaMinimization(automaton.startState, automaton.finalStates,
                        automaton.states, automaton.alphabet, automaton.transitions)
    dfa.printAutomation()
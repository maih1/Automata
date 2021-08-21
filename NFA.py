"""
Epsilon NFA to NFA
"""

import Data as dt
import Automaton as at
import copy as cp


# find a transition function whose destination is many states
# Tìm một hàm chuyển tiếp la epsilon
def findTransEp(transitions):
    des_many_states = []

    for i in transitions:
        if i[1] == 'epsilon':
            des_many_states.append(i)

    return des_many_states

# find transition not save alphabet
# Tìm hàm chuyển cho một trạng thái và một ký tự trong bảng chữ cái
def findTransNotAlpha(x, alphabet, transitions):
    listFind = []
    check = True
    length = 0
    t = 0
    
    while check == True and length < len(transitions):
        i = transitions[length]
        
        if x == i[0] and alphabet == i[1]:
            if len(i) < 3:
                pass
            else:
                for j in range(2, len(i)):
                    listFind.append(i[j])
            t += 1
        length += 1
             
    return listFind

# Get next state
# Lấy trạng thái chuyển tiếp
def getNextState(trans_i):
    next_state = []

    for i in range(2, len(trans_i)):
        next_state.append(trans_i[i])
    
    return next_state

# Lay trang thai bat dau
def getStartTranStates(trans):
    start_state_trans = []

    for i in trans:
        start_state_trans.append(i[0])
    
    start_state_trans.sort()
    return start_state_trans

# tim cac ε-closure(q_i)
def find_eq(states, transitions):
    ls_eq = dict()
    eps_trans = findTransEp(transitions)
    _get_start_trans = getStartTranStates(eps_trans)
    for i in states:
        if i not in _get_start_trans:
            ls_eq.update({i: [i]})
        else:
            res_eq = []
            next_state = [i]
            new_next = []
            j = 0
            while len(next_state) > 0:
                k = 0
                check_k = True

                if next_state[j] in _get_start_trans:
                    while check_k == True and k < len(eps_trans):
                        if next_state[j] == eps_trans[k][0]:
                            new_next = getNextState(eps_trans[k])
                            for gn in new_next:
                                if gn not in res_eq and gn not in next_state:
                                    res_eq.append(gn)
                                    next_state.append(gn)
                            check_k = False
                        else: k += 1
                next_state.pop(j)
                
            res_eq.append(i)
            res_eq.sort()
            ls_eq.update({i: res_eq})

    return ls_eq

# lay ra eq(i)
def get_eq(state, ls_eq):
    # _get_eq = []

    for i in ls_eq:
        if state == i:
            # _get_eq.append(ls_eq[i])
            return ls_eq[i]
    # return _get_eq


# union of transition next states
# hợp các trạng thái tiếp theo của quá trình chuyển đổi
def unionTransState(list_states):
    list_union = []

    for i in list_states:
        list_union = list(set(list_union) | set(i))
    list_union.sort()
    return list_union


# Xây dựng lại hàm chuyển
def updateTrans(states, alphabet, transitions, ls_eq):
    # ls_eq = find_eq(states, transitions)
    new_ls_trans = []
    
    # Viet lai ham chuyen
    for i in states:
        
        # Lay ham eq cua trang thai i
        # eq(q0) = [q0, q1, q2]
        _eq = get_eq(i, ls_eq)
        new_tran = []

        # tim trang thai chuyen tiep voi moi ky hieu trong bang chu cai
        # i = q0, j = 0 tim q0 0 = ?
        for j in alphabet:
            next_tran_ij = []
            
            # trang thai tiep theo la ket qua cua cac ham chuyen toi epsilon cua trang thai dau
            # q0 j ? + q1 j ? + q2 j ?
            for k in _eq:
                # Tim trang thai chuyen tiep cho trang thai bat dau la k thuoc eq(i) va j thuoc bang chu cai
                _find_next_state_tran = findTransNotAlpha(k, j, transitions)
                next_tran_ij.append(_find_next_state_tran)
            
            # Hop cac trang thai chuyen tiep
            union_trans = unionTransState(next_tran_ij)
            union_eq = []

            # trang thai chuyen tiep cua ham chuyen i thuoc tap trang thai, j thuoc bang chu cai
            # la ham hop cua cac trang thai den epsilon
            # q0 0 = eq(eq(0), a) = eq([ket qua cua eq(0)], a) = eq(P)
            # eq(P) = ∪nion_q∈P eq(q) 
            if len(union_trans) == 0:
                union_eq = union_trans
            else:
                _temp_union_trans = []
                for k in union_trans:
                    _get_eq_k = get_eq(k, ls_eq)
                    _temp_union_trans.append(_get_eq_k)
                union_eq = unionTransState(_temp_union_trans)



            # Them ham chuyen [i, j, res] vao bo ham chuyen moi
            if len(union_eq) == 0:
                new_ls_trans.append([i, j])
            else:
                _new_tran_ij = [i, j]
                for k in union_eq:
                    _new_tran_ij.append(k)
                
                new_ls_trans.append(_new_tran_ij)

    return new_ls_trans

# chuyen epsilon nfa sang nfa
def nfa(startState, finalStates, states, alphabet, transitions):
    # create nfa
    _nfa = at.Automaton()

    # list epsilon 
    ls_eq = find_eq(states, transitions)


    # new alphabet
    alphabet = [ i for i in alphabet if i != 'epsilon']
    _nfa.alphabet = alphabet

    # new state 
    states = cp.deepcopy(states)
    _nfa.states = states

    # new trans
    transitions = cp.deepcopy(transitions)
    new_trans = updateTrans(states, alphabet, transitions, ls_eq)
    _nfa.transitions = new_trans

    # new start state
    startState = cp.deepcopy(startState)
    _nfa.startState = startState

    # new final state
    finalStates = cp.deepcopy(finalStates)
    new_final_state = finalStates
    
    for i in finalStates:
        for j in ls_eq:
            if i in ls_eq[j] and j in startState and j not in new_final_state:
                new_final_state.append(j)
    
    new_final_state = list(set(new_final_state))
    new_final_state.sort()
    _nfa.finalStates = new_final_state

    return _nfa


def main(filename):
    automation = at.automatonData(filename)
    _nfa = nfa(automation.startState, automation.finalStates, automation.states, automation.alphabet, automation.transitions)
    return _nfa

# au = at.automatonData('./Data/NFA/testnfa1.txt')
# au = at.automatonData('./Data/NFA/testnfa4.txt')
# au = at.automatonData('./Data/NFA/testnfa2.txt')
# au = at.automatonData('./Data/NFA/testnfa5.txt')
# au = at.automatonData('./Data/NFA/testinputdfa.txt')
# au = at.automatonData('./Data/NFA/testinputdfa2.txt')
# au = at.automatonData('./Data/DFA/testdfa1.txt')
# au.printAutomation()

# c = nfa(au.startState, au.finalStates, au.states, au.alphabet, au.transitions)
# c.printAutomation()
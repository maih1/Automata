import Automaton as at
import NFA
import copy as cp

"""
DFA:
+ Constructing a function of two variables
    - find a transition function whose destination is many states
+ Define a new set of states
    -Add transition and state so that automat M is full automat.
+ Define the transfer function
--------------------------------------------------------------------
+ Xây dựng hàm hai biến
     - tìm một hàm chuyển tiếp có đích là nhiều trạng thái
+ Xác định một tập hợp các trạng thái mới
     -Thêm chuyển tiếp và trạng thái để automat M là automat đầy đủ.
+ Xác định chức năng chuyển

"""

# find a transition function whose destination is many states
# Tìm một hàm chuyển tiếp có đích là nhiều trạng thái
def findTransMany(transitions):
    des_many_states = []

    for i in transitions:
        if len(i) > 3:
            des_many_states.append(i)

    return des_many_states


# union of transition next states
# hợp các trạng thái tiếp theo của quá trình chuyển đổi
def unionTransState(list_states):
    list_union = []

    for i in list_states:
        list_union = list(set(list_union) | set(i))
    
    return sorted(list_union)

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


# Constructing function of two variables
# Construct the transition function for the dual states
# xây dựng hàm của hai biến
# Xây dựng hàm chuyển đổi cho các trạng thái kép
# T({p1, p2}, a) = T(p1,a) ∪ T(p2,a) = {p2} ∪{p1} = {p1, p2}
def constructTransitionDual(alphabet, temp_trans, des_many_states):
    # new_trans = findTransMany(transitions)
    union_trans = []
    temp_trans = temp_trans.copy()
    ls_next_state_des = at.getNextTransStates(des_many_states) 

    for i in ls_next_state_des:     
        # nextState = at.findTransitions(i[0], des_many_states, alphabet)
        # nextState = list(nextState[0])
        # nextState.pop(0)
        nextState = i

        for j in alphabet:
            nextstate_k = []
           
            for k in nextState:
                # find next state
                nextstate_k.append(findTransNotAlpha(k, j, temp_trans))
            
            # union of transition states and add transiton in new list
            # hợp các trạng thái chuyển đổi và thêm chuyển đổi trong danh sách mới
            _add =[nextState, j, unionTransState(nextstate_k)]
            if _add not in union_trans:
                union_trans.append([nextState, j, unionTransState(nextstate_k)])

    return union_trans

# Get next state
# Lấy trạng thái chuyển tiếp
def getNextState(trans_i):
    next_state = []

    for i in range(2, len(trans_i)):
        next_state.append(trans_i[i])
    
    return next_state

# Define a new set of states
# Xác định một tập hợp các trạng thái mới
def newStates(states, des_many_states, union_trans):
    # create new states
    temp_new_states = states.copy()

    for i in des_many_states:
        _add = getNextState(i)
        if _add not in temp_new_states:
            temp_new_states.append(_add)
    
    for i in union_trans:
        _add = i[2]
        if len(_add) > 1 and _add not in temp_new_states:
            temp_new_states.append(_add)

    # # remove loop state
    temp_new_states2 = temp_new_states.copy()
    # for i in range(len(temp_new_states)):
    #     for j in range(i+1, len(temp_new_states)):
    #         if temp_new_states[i] == temp_new_states[j]:
    #             temp_new_states2.pop(j)
    
    count = 0
    new_states = dict()

    for i in temp_new_states2:
        new_states.update({'s'+str(count): i})
        count += 1

    return new_states

# update trans
# Cập nhật lại hàm chuyển
def updateTrans(des_many_states, union_trans, transitions):
    # create new trans
    new_trans = transitions.copy()

    # update type next many state
    for i in des_many_states:
        update = []
        for j in range(2, len(i)):
            update.append(i[j])
        temp_update = [i[0], i[1], update]

        check = True
        id_trans = 0
        while check == True and id_trans < len(new_trans):
            trans_i = new_trans[id_trans]
            if i == trans_i:
                new_trans[id_trans] = temp_update
                check = False
            else: id_trans += 1

    # add transition function for the dual states to transitions
    for i in union_trans:
        if i not in new_trans:
            new_trans.append(i)

    return new_trans

# Deterministic Finite Automaton
# Create dfa
# set dfa
def dfa(startState, finalStates, states, alphabet, transitions):
    trans = cp.deepcopy(transitions)

    # transition function whose destination is many states
    # hàm chuyển tiếp có đích là nhiều trạng thái
    des_many_states = findTransMany(trans)

    # transition function for the dual states
    # hàm chuyển tiếp cho các trạng thái kép
    union_trans = constructTransitionDual(alphabet, trans, des_many_states)

    # create new automat/dfa
    # Tạo otomat mới
    dfa = at.Automaton()

    # New states
    # Tạo danh sách trạng thái mới
    # temp_states = newStates(states, des_many_states, union_trans)
    # temp_states2 = temp_states.copy()
    
    # add transition function for the dual states to transitions
    # thêm chức năng chuyển tiếp cho các trạng thái kép để chuyển tiếp
    temp_trans = updateTrans(des_many_states, union_trans, trans)
    new_trans = cp.deepcopy(temp_trans)

    # New states
    # Tạo danh sách trạng thái mới
    temp_states = newStates(states, des_many_states, union_trans)
    temp_states2 = temp_states.copy()
    
    # set trans 
    # Thay đổi trạng thái của hàm chuyển đổi 
    for i in temp_states:
        id_trans = 0

        while id_trans < len(temp_trans):
            trans_i = new_trans[id_trans]
            
            # change the new entry state 
            # Thay đổi trạng thái bắt đầu trong hàm chuyển sang loại trạng thái mới
            # p0 a p1 thành s0 a p1
            if temp_states[i] == trans_i[0] or [temp_states[i]] == trans_i[0]:
                trans_i[0] = i

            # incomplete automation supplement
            # Bổ sung thêm trạng thái để automat là hoàn chỉnh
            # p1 a null thành p0 a s1
            if len(trans_i) < 3 or len(trans_i[2]) == 0:
                # add new state
                # Thêm vào trạng thái mới
                count = len(temp_states)
                add_state = 's'+ str(count)
                temp_states2.update({add_state: None})

                # update trans
                # Cập nhật lại hàm chuyển
                if len(trans_i) < 3:
                    trans_i.append(add_state)
                else:
                    trans_i[2] = add_state

                # add new trans of new state
                # Thêm vào hàm chuyển mới của trạng thái mới
                # Ứng với từng phần tử trong bảng chữ cái
                # alphabet = a, b, c
                # thêm s1 a s1, s1 b s1, s1 c s1
                for k in alphabet:
                    _new = [add_state, k, add_state]
                    if _new not in new_trans:
                        new_trans.append([add_state, k, add_state])

            # change the new end state 
            # Thay đổi trạng thái chuyển tiếp trong hàm chuyển sang loại trạng thái mới
            # p0 a p1 thành p0 a s1
            elif temp_states[i] == trans_i[2] or [temp_states[i]] == trans_i[2]:
                trans_i[2] = i
            
            id_trans += 1

    # remove transition loop
    # Xóa những hàm chuyển giống nhau lặp lại
    i = 0
    while i < len(new_trans) - 1:
        ii = new_trans[i]
        j = i + 1
        while j < len(new_trans):
            jj = new_trans[j]

            if ii == jj:
                new_trans.pop(j)
            else: j += 1
        i += 1

    # add new trans dfa
    # thêm tập hàm chuyển mới cho dfa
    dfa.transitions = new_trans

    # create new states dfa
    # Tạo bộ trạng thái mới của dfa
    new_states = []

    for i in temp_states2:
        new_states.append(i)
    
    dfa.states = new_states

    # create new start state dfa
    # Trạng thái bắt đầu mới của dfa
    new_start_state = []

    for i in temp_states2:
        if temp_states2[i] in startState:
            new_start_state.append(i)
    
    dfa.startState = new_start_state

    # create new final state dfa
    # Trạng thái kết thúc mới của dfa
    new_final_state = []
    
    for i in finalStates:
        for j in temp_states:
            if i in temp_states[j] and j not in new_final_state:
                new_final_state.append(j)
    
    dfa.finalStates = sorted(new_final_state)

    # create new alalphabet dfa
    # Bảng chữ cái của dfa
    dfa.alphabet = alphabet.copy()

    return dfa

def main(filename):
    automation = at.automatonData(filename)
    _dfa = dfa(automation.startState, automation.finalStates, automation.states, automation.alphabet, automation.transitions)
    return _dfa


def inputData(filename):
    automaton = at.automatonData(filename)

    # kiem tra ham chuyen co dang epsilon khong
    check_epsilon = NFA.findTransEp(automaton.transitions)

    # neu khong co dang epsition khong can bien doi nfa
    if len(check_epsilon) == 0:
        return automaton
    
    # neu co dang epsition thi can chuyen dang epsition nfa sang nfa
    else:
        _nfa = NFA.main(filename)
        return _nfa


if __name__ == '__main__':
    print("Automation input: ")
    automaton = inputData('./Data/DFA/testdfa1.txt')
    # automaton = inputData('./Data/DFA/testdfa2.txt')
    
    # automaton = inputData('./Data/NFA/testnfa4.txt')
    # automaton = inputData('./Data/NFA/testinputdfa2.txt')
    automaton.printAutomation()
    
    print('----------------------------------------------')

    print("Deterministic Finite Automaton")
    _dfa = dfa(automaton.startState, automaton.finalStates,
                            automaton.states, automaton.alphabet, automaton.transitions)
    _dfa.printAutomation()
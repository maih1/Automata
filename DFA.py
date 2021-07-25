import Automaton as at
import Data as dt
import copy as cp


# find a transition function whose destination is many states
def findTransMany(transitions):
    des_many_states = []

    for i in transitions:
        if len(i) > 3:
            des_many_states.append(i)

    return des_many_states


# union of transition next states
def unionTransState(list_states):
    list_union = []

    for i in list_states:
        list_union = list(set(list_union) | set(i))
    
    return sorted(list_union)

# find transition not save alphabet
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
def constructTransitionDual(alphabet, temp_trans, des_many_states):
    # new_trans = findTransMany(transitions)
    union_trans = []
    temp_trans = temp_trans.copy()

    for i in des_many_states:     
        nextState = at.findTransitions(i[0], des_many_states, alphabet)
        nextState = list(nextState[0])
        nextState.pop(0)

        for j in alphabet:
            nextstate_k = []
           
            for k in nextState:
                # find next state
                nextstate_k.append(findTransNotAlpha(k, j, temp_trans))
            
            # union of transition states and add transiton in new list
            union_trans.append([nextState, j, unionTransState(nextstate_k)])

    return union_trans

# Get next state
def getNextState(trans_i):
    next_state = []

    for i in range(2, len(trans_i)):
        next_state.append(trans_i[i])
    
    return next_state

# Define a new set of states
def newStates(states, des_many_states, union_trans):
    # create new states
    temp_new_states = states.copy()

    for i in des_many_states:
        temp_new_states.append(getNextState(i))
    
    # remove loop state
    temp_new_states2 = temp_new_states.copy()
    for i in range(len(temp_new_states)):
        for j in range(i+1, len(temp_new_states)):
            if temp_new_states[i] == temp_new_states[j]:
                temp_new_states2.pop(j)
    
    count = 0
    new_states = dict()

    for i in temp_new_states2:
        new_states.update({'s'+str(count): i})
        count += 1

    return new_states

# update trans
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
        new_trans.append(i)

    return new_trans


# Create dfa
# set dfa
def dfa(startState, finalStates, states, alphabet, transitions):
    trans = cp.deepcopy(transitions)

    # transition function whose destination is many states
    des_many_states = findTransMany(trans)

    # transition function for the dual states
    union_trans = constructTransitionDual(alphabet, trans, des_many_states)

    # create new automat/dfa
    dfa = at.Automaton()

    # New states
    temp_states = newStates(states, des_many_states, union_trans)
    temp_states2 = temp_states.copy()
    
    # add transition function for the dual states to transitions
    temp_trans = updateTrans(des_many_states, union_trans, trans)
    new_trans = cp.deepcopy(temp_trans)
    
    # set trans      
    for i in temp_states:
        id_trans = 0

        while id_trans < len(temp_trans):
            trans_i = new_trans[id_trans]
            
            # change the new entry state 
            if temp_states[i] == trans_i[0] or [temp_states[i]] == trans_i[0]:
                trans_i[0] = i

            # incomplete automation supplement
            if len(trans_i) < 3:
                # add new state
                count = len(temp_states)
                add_state = 's'+ str(count)
                temp_states2.update({add_state: None})

                # update trans
                trans_i.append(add_state)

                # add new trans of new state
                for k in alphabet:

                    new_trans.append([add_state, k, add_state])

            # change the new end state 
            elif temp_states[i] == trans_i[2] or [temp_states[i]] == trans_i[2]:
                trans_i[2] = i
            
            id_trans += 1

    # remove transition loop
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

    # create new trans dfa
    dfa.transitions = new_trans

    # create new states
    new_states = []

    for i in temp_states2:
        new_states.append(i)
    
    dfa.states = new_states

    # create new start state
    new_start_state = None

    for i in temp_states2:
        if temp_states2[i] == startState:
            new_start_state = i
    
    dfa.startState = new_start_state

    # create new final state 
    new_final_state = []
    
    for i in finalStates:
        for j in temp_states:
            if i in temp_states[j]:
                new_final_state.append(j)
    
    dfa.finalStates = sorted(new_final_state)

    # create new alalphabet
    dfa.alphabet = alphabet.copy()

    return dfa

if __name__ == '__main__':
    print("Automation input: ")
    automaton = at.automatonData('./Data/Dfa/testdfa1.txt')
    # automaton = at.automatonData('./Data/Dfa/testdfa2.txt')
    automaton.printAutomation()
    
    print('----------------------------------------------')

    print("Deterministic Finite Automaton")
    _dfa = dfa(automaton.startState, automaton.finalStates,
                            automaton.states, automaton.alphabet, automaton.transitions)
    _dfa.printAutomation()
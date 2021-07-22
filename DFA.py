from typing import NoReturn
import Data
import Automaton as at
import Data as dt


# find a transfer function whose destination is many states
def findTransMany(transitions):
    new_trans = []

    for i in transitions:
        if len(i) > 3:
            new_trans.append(i)

    return new_trans


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
def constructTransitionDual(alphabet, transitions, new_trans):
    # new_trans = findTransMany(transitions)
    union_trans = []

    for i in new_trans:     
        nextState = at.findTransitions(i[0], new_trans, alphabet)
        nextState = list(nextState[0])
        nextState.pop(0)

        for j in alphabet:
            nextstate_k = []
           
            for k in nextState:
                # find next state
                nextstate_k.append(findTransNotAlpha(k, j, transitions))
            
            # union of transition states and add transiton in new list
            union_trans.append([nextState, j, unionTransState(nextstate_k)])

    return union_trans


# Define a new set of states
def newStates(states, new_trans):
    # create new states
    new_states = dict()
    count = 0

    for i in states:
        new_states.update({'s'+str(count): i})
        count += 1

    # bug
    for i in new_trans:
        new_states.update({'s'+str(count): i})
        count += 1
    
    return new_states

automaton = at.automatonData('test1.txt')
# automaton.printAutomation()

a = at.findTransitions('p0', automaton.transitions, automaton.alphabet)
# print(a)
b = findTransMany(automaton.transitions)
# print(b)
c = constructTransitionDual(automaton.alphabet, automaton.transitions, b)
# print(c)
d =newStates(automaton.states, b)
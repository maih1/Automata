import math
import Input as ip

class Automaton:
    def __init__(self, startState, finalStates, states, alphabet, transitions) -> None:
        """
        Input:
        -startState: start state (s_0)
        -finalStartes: a list final state (F)
        -states: a lists containing the states (S)
        -alphabet: a lists alphabet (sigma)
        -transitions: state transition function (detal)
        """
        self.startState = startState
        self.finalStates = finalStates
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions

def findUnreachableState(startState, states, transitions):
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

def getEquivalenceStates(automaton):
    # unreachable state
    state_unreachable = []

a = ip.opendFileInput('t1.txt')
c = ip.ndfInput(a)
for x in c:
    print(x, c[x])

d =findUnreachableState(c['startState'], c['states'], c['transitions'])
print(d)
import math
import Input as ip

class nfa:
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

# a = ip.opendFileInput('t1.txt')
# c = ip.ndfInput(a)
# for x in c:
#     print(x, c[x])
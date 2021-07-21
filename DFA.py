import Data
import Automaton as at
import Data as dt

def dfa(startState, finalStates, states, alphabet, transitions):
    pass
automaton = at.automatonData('test1.txt')
automaton.printAutomation()

a = at.findTransitions('p0', automaton.transitions, automaton.alphabet)

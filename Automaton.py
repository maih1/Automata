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
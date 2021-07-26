import Data as dt

# Chomsky Normal Form
class CNF:
    pass

class CKY:
    def __init__(self, sentence=None, startSymbol=None, grammar=None) -> None:
        """
        Input:
        -sentence: the sentence must analyzed
        -startSymbol: start symbol (S)
        -grammar:The Structure of the rules in a Chomsky Normal Form grammar (P)
        """
        self.sentence = sentence
        self.startSymbol = startSymbol
        self.grammar = grammar

# Input data into cky
def ckyData1(filename):
    fileData = dt.opendFileInput(filename)
    ckyData = dt.ckyInput(fileData)

    cky = CKY()

    for i in ckyData:
        if i == 'sentence':
            cky.sentence = ckyData[i]
        elif i == 'startSymbol':
            cky.startSymbol = ckyData[i]
        elif i == 'grammar':
            cky.grammar = ckyData[i]

    return cky
import Data as dt

# Chomsky Normal Form
class CNF:
    def __init__(self, mainAlphabet=None, subAlphabet=None, startSymbol=None, rules=None) -> None:
        """
        Input: 
        -mainAlphabet: main alphabet/end symbols set (sigma)
        -subAlphabet: sub-alphabet/the symbol set doesn't end or variable set (V)
        -startSymbol: start symbol (S)/ký tự xuất phát/tiên đề
        -rules: finite set of rules/set of birth rules (P)
        """
        self.mainAlphabet = mainAlphabet
        self.subAlphabet = subAlphabet
        self.startSymbol = startSymbol
        self.rules = rules

    def cnfForm(self):
        cky = {
            'mainAlphabet': self.mainAlphabet,
            'subAlphabet': self.subAlphabet,
            'startSymbol': self.startSymbol,
            'rules': self.rules,
        }

        return cky
    
    # print data cnf
    def printCNF(self):
        cnf = self.cnfForm()

        # print
        for i in cnf:
            if i == 'rules':
                print('+ rules (P):')
                for j in range(len(cnf[i])):
                    print('\tP{}: {} -> {}'.format(j, cnf[i][j][0], cnf[i][j][1]))
            else:
                print('+ {}: {}'.format(i, cnf[i]))

# Cocke Kasami Younger
class CKY:
    def __init__(self, sentence=None, startSymbol=None, grammar=None) -> None:
        """
        Input:
        -sentence: the sentence must analyzed/Câu cần phân tích
        -startSymbol: start symbol (S)/ký tự xuất phát/tiên đề
        -grammar: grammar (G) or set of birth rules (P) in grammar/văn phạm hay tập các quy tắc sinh trong văn phạm
        """
        self.sentence = sentence
        self.startSymbol = startSymbol
        self.grammar = grammar

    # rewrite the sentence
    def rewriteSentence(self):
        new_sentence = ''

        for i in range(len(self.sentence)):
            if i == len(self.sentence) - 1:
                new_sentence = new_sentence + str(self.sentence[i])
            else: new_sentence = new_sentence + str(self.sentence[i]) + ' '

        return new_sentence

def cnfData(filename):
    fileData = dt.opendFileInput(filename)
    cnfData = dt.cnfInput(fileData)

    cnf = CNF()

    for i in cnfData:
        if i == 'mainAlphabet':
            cnf.mainAlphabet = cnfData[i]
        elif i == 'subAlphabet':
            cnf.subAlphabet = cnfData[i]
        elif i == 'startSymbol':
            cnf.startSymbol = cnfData[i]
        elif i == 'rules':
            cnf.rules = cnfData[i]
    
    return cnf

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

# Input data into cky from cnf
def ckyData2(filename, cnf):
    fileData = dt.opendFileInput(filename)
    cky = CKY()

    cky.sentence = fileData[0]
    cky.startSymbol = cnf.startSymbol
    cky.grammar = cnf.rules

    return cky

# set type grammar/rules
def setType(rules):
    new_grammar = []

    for i in rules:
        set_list = []
        for j in range(1, len(i)):
            set_list.append(i[j])
        new_grammar.append([i[0], set_list])
    
    return new_grammar
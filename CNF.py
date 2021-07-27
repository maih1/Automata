import Data as dt

# Chomsky Normal Form
class CNF:
    pass

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
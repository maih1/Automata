def opendFileInput(filename):
    file = open(filename)

    fileData = []

    for i in file:
        data = i.rstrip().split()
        
        fileData.append(data)

    file.close()
    
    return fileData

def ndfInput(filedata):
    startState = ''
    finalStartes = []
    states = []
    alphabet = []
    transitions = []

    for i in range(len(filedata)):
        if i == 0:
            startState = filedata[i]
            # states.append(filedata[i][0])
        elif i == 1:
            finalStartes = filedata[i]
            # for j in filedata[i]:
            #     states.append(j)
        else:            
            states.append(filedata[i][0])
            alphabet.append(filedata[i][1])
            transitions.append(filedata[i])
        
    ndftData = {
        'startState': startState,
        'finalStates': finalStartes,
        'states': sorted(set(states)),
        'alphabet': sorted(set(alphabet)),
        'transitions': transitions
    }

    return ndftData

def ckyInput(filedata): 
    sentence = []
    startSymbol = []
    grammar = []

    for i in range(len(filedata)):
        if i == 0:
            sentence = filedata[i]
        elif i == 1:
            startSymbol = filedata[i][0]
        else:
            grammar.append(filedata[i])

    cky_data = {
        'sentence': sentence,
        'startSymbol': startSymbol,
        'grammar': grammar,
    }

    return cky_data

def cnfInput(filedata):
    # main alphabet/end symbols set
    # bảng chữ cái chính/bộ ký hiệu kết thúc
    mainAlphabet = []

    # sub-alphabet/the symbol set doesn't end or variable set
    # bảng chữ cái phụ/tập ký hiệu không kết hay tập biến
    subAlphabet = []

    # start symbol
    # Ký tự suất phát/tiên đề
    startSymbol = ''

    # finite set of rules
    # Tập quy tắc hữu hạn/quy tắc sinh
    rules = []

    for i in range(len(filedata)):
        if i == 0:
            mainAlphabet = filedata[i]
        elif i == 1:
            subAlphabet = filedata[i]
        elif i == 2:
            startSymbol = filedata[i][0]
        else:
            rules.append(filedata[i])

    cnf_data = {
        'mainAlphabet': mainAlphabet,
        'subAlphabet': subAlphabet,
        'startSymbol': startSymbol,
        'rules': rules,
    }

    return cnf_data
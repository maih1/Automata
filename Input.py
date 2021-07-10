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

    count = 0

    for i in range(len(filedata)):
        if i == 0:
            startState = filedata[i][0]
            states.append(filedata[i][0])
        elif i == 1:
            finalStartes = filedata[i]
            for j in filedata[i]:
                states.append(j)
        else:
            
            states.append(filedata[i][0])
            alphabet.append(filedata[i][1])
            transitions.append(filedata[i])

            count += 1
        
    ndftData = {
        'startState': startState,
        'finalStartes': finalStartes,
        'states': sorted(set(states)),
        'alphabet': sorted(set(alphabet)),
        'transitions': transitions
    }

    return ndftData
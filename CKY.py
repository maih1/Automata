import CNF 

# set type grammar/rules
def setType(grammar):
    new_grammar = []

    for i in grammar:
        set_list = []
        for j in range(1, len(i)):
            set_list.append(i[j])
        new_grammar.append([i[0], set_list])
    
    return new_grammar

# Create table/list cky
# Tạo bảng cky
def listCheckCky(length):
    ls_cky = [[[]]*length for _ in range(length)]
    
    return ls_cky

# Multiply two symbols sets
# Nhân phần tử của 2 bộ ký tự
def mulSym(s1, s2):
    ls_mul = []

    for i in s1:
        for j in s2:
            ls_mul.append(str(i) + str(j))
    
    return ls_mul

# Check if sym/from sym is on the right side of the rule set
# Kiểm tra ký tự hợp sym/từ sym có thuộc vế phải trong bộ quy tắc không 
def checkSymbols(ls_sym, grammar):
    ls_check_sym = []

    for i in ls_sym:
        for j in grammar:
            if i in j[1]:
                # If it is on the right hand side of the rule p_j 
                # Returns the result on the left side of p_j
                # Nếu nằm thuộc vế phải trong quy tắc p_j
                # Trả về kết quả là vế trái của p_j
                ls_check_sym.append(j[0])
    
    return ls_check_sym


# Find the left side of the characters in the sentence to be analyzed 
# In the set of rules
# Tìm vế trái của các ký tự trong câu cần phân tích
# Trong bộ quy tắc
def set_ii(grammar, sen_i):
    ls = []
    
    # check sentence in grammar
    for j in grammar:
        if sen_i in j[1]:
            ls.append(j[0])

    return ls

# union values from the values in the table cky
# Hợp các giá trị từ các giá trị trong bảng cky
def unionTransState(ls):
    list_union = []

    for i in ls:
        list_union = list(set(list_union) | set(i))
    
    return sorted(list_union)

# Set values for the cells in the table cky 
# Đặt giá trị cho các ô trong bảng cky
def cky(sentence, grammar):
    
    # lenght table cky - length sentence - n
    length = len(sentence)

    # create table/list cky
    ls_cky = listCheckCky(length)
    
    # change type set of rules
    grammar = setType(grammar)

    # loop diagonally in the table cky
    # lặp theo đường chéo trong bảng cky

    # Find the left side of the characters in the sentence to be analyzed in the set of rules
    # Tìm vế trái của các ký tự trong câu cần phân tích trong bộ quy tắc
    # set list check cky index i, i
    # Giá trị vế trái tìm được lưu vào vị trí i, i trong bảng cky
    for i in range(length):
        ls = set_ii(grammar, sentence[i])
        ls_cky[i][i] = ls

    # Find the left-hand side from the values of the left-hand side of the characters in the sentence to be analyzed
    # Tìm vế trái từ các giá trị vế trái của các ký tự trong câu cần phân tích

    # Tìm từ vị trí ký tự thứ 2 đến vị trí ký tự thứ n
    # Tương ứng từ vị trí i = 0 đến i = n-1 trong bảng cky

    # Lặp từ phần tử thứ 2 đến n
    # Tương ứng với đặt giá trị từ vị trí thứ i = 1 đến i = n-1 trong bảng cky
    # Lặp theo đường chéo (01, 12, 23, 34 ... n-2n-1) trong bảng cky
    for i in range(1, length):

        # Tạo vị trí/tọa độ i trong bảng cho giá trị vế trái tìm được
        index1 = i

        # lặp phần tìm n - i giá trị vế trái trong bộ quy tắc suy diễn
        for j in range(length - i):
            temp_ls = []
            index2 = j

            # Lặp tìm giá trị vế trái từ k lần giá trị trước 
            for k in range(i):
                # Giá trị vế trái tìm từ 2 giá trị vế trái trước

                # ký tự ở vị trí j, index2 theo đường chéo
                sym1 = ls_cky[j][index2]

                # ký tự ở vị trí index2 + 1, index1 theo đường chéo
                sym2 = ls_cky[index2+1][index1]

                # Nhân phần tử của 2 bộ ký tự/giá trị vế trái theo vị trí đường chéo trong bảng tương ứng
                ls_sym = mulSym(sym1, sym2)

                # Tìm giá trị vế trái từ ký tự hợp sym/từ sym trong tập quy tắc
                res_check = checkSymbols(ls_sym, grammar)
                temp_ls.append(res_check)

                # chuyển vị trí/tọa độ j
                index2 += 1
            
            # hợp của k giá trị vế trái tìm được cho ô thứ j, index1 trong bảng cky
            ls_ij = unionTransState(temp_ls)

            # Đặt lại giá trị cho ô thứ j, index1
            ls_cky[j][index1] = ls_ij

            # chuyển vị trí/tọa đô ô đặt giá trị i
            index1 += 1
        
    return ls_cky

# Check sentence derived from grammar
# Kiểm tra xem câu có sinh được từ văn phạm không
def checkCky(sentence, grammar, startSymbol):
    ls_cky = cky(sentence, grammar)
    
    # If the starting character is in cell 0, n (n is the number of symbols (letters) in the sentence)
    # in the cky table (list cky) Then the sentence is born from grammar
    # Nếu ký tự bắt đầu (ký tự xuất phát/tiên đề) có nẳm tại ô 0, n (n là số ký hiệu (chữ cái) trong câu)
    # trong bảng cky (list cky) thì câu sinh được ra từ văn phạm
    if startSymbol in ls_cky[0][len(sentence) - 1]:
        return True
    else: return False

def _p(length):
    p = ''
    for i in range(length):
        p += '-'
    return p


# Print table cky
# In bảng cky
def printCky(ls_cky):
    for i in range(len(ls_cky)):
        for j in range(len(ls_cky)):
            if j < i:
                print('{:{width}}'.format('', width=10),end='\t')
            else: print('{:{width}}'.format('{}'.format(ls_cky[i][j]), width=10),end='\t')
        print()

# Print the analysis sentence that can be derived from grammar G?
# In câu phân tích có sinh được từ văn phạm G không
def printMainCky(sentence, new_sentence, grammar, startSymbol):
    _checkCky = checkCky(sentence, grammar, startSymbol)
    
    if _checkCky == True:
        print("Sentence \"{}\" is derived from the G grammar".format(new_sentence))
    else:
        print("Sentence \"{}\" is not derived from the G grammar".format(new_sentence))


# main
if __name__ == "__main__":
    cky_data = CNF.ckyData1('test1.txt')
    # cky_data = CNF.ckyData1('test2.txt')

    # rewrite the sentence
    new_sentence = cky_data.rewriteSentence()

    # Table/list cky
    _cky = cky(cky_data.sentence, cky_data.grammar)

    # Print main
    printMainCky(cky_data.sentence, new_sentence, cky_data.grammar, cky_data.startSymbol)
    
    # Print table cky
    print('Table CKY:')
    printCky(_cky)
import numpy as np
import CNF 

# set type grammar
def setType(grammar):
    new_grammar = []

    for i in grammar:
        set_list = []
        for j in range(1, len(i)):
            set_list.append(i[j])
        new_grammar.append([i[0], set_list])
    
    return new_grammar

def listCheckCky(length):
    ls_cky = [[[]]*5 for _ in range(5)]
    
    return ls_cky

# multiply 2 symbols
def mulSym(s1, s2):
    ls_mul = []

    for i in s1:
        for j in s2:
            ls_mul.append(str(i) + str(j))
    
    return ls_mul

def checkSymbols(ls_sym, grammar):
    ls_check_sym = []

    for i in ls_sym:
        for j in grammar:
            if i in j[1]:
                ls_check_sym.append(j[0])
    
    return ls_check_sym

def set_ii(grammar, sen_i):
    ls = []
    
    # check sentence in grammar
    for j in grammar:
        if sen_i in j[1]:
            ls.append(j[0])

        
    return ls

# union of 
def unionTransState(ls):
    list_union = []

    for i in ls:
        list_union = list(set(list_union) | set(i))
    
    return sorted(list_union)

def cky(sentence, grammar):
    length = len(sentence)
    ls_cky = listCheckCky(length)

    grammar = setType(grammar)

    # set list check cky index i, i
    # lặp theo đường chéo
    for i in range(length):
        ls = set_ii(grammar, sentence[i])
        ls_cky[i][i] = ls

    # lặp từ phần tử thứ 2 đến n
    for i in range(1, length):
        # Tạo vị trí i trong list
        index1 = i

        # lặp phần tìm n - i giá trị quy tắc suy diễn
        for j in range(length - i):
            temp_ls = []
            index2 = j

            # Lặp k lần số quy tắc để điển giá trị cho ls_cky thứ j, index1
            for k in range(i):
                # ký tự ở vị trí j, index2 theo đường chéo
                sym1 = ls_cky[j][index2]

                # ký tự ở vị trí index2 + 1, index1 theo đường chéo
                sym2 = ls_cky[index2+1][index1]

                # tích của hai nhóm ký hiệu
                ls_sym = mulSym(sym1, sym2)

                # Tìm giá trị của các tích ký hiệu trong tập quy tăc
                res_check = checkSymbols(ls_sym, grammar)
                temp_ls.append(res_check)

                # chuyển vị trí lấy ký tự
                index2 += 1
            
            # hợp của k giá trị cho ô thứ j, index1
            ls_ij = unionTransState(temp_ls)

            # thay đổi giá trị cho ô thứ j, index1
            ls_cky[j][index1] = ls_ij

            # chuyển vị trí ô tìm giá trị
            index1 += 1
        
    return ls_cky


def cky1(sentence, grammar):
    # create 
    ls_cky = [[] for i in range(len(sentence))]
    length = len(sentence)
    ls_cky1 = listCheckCky(length)

    # set grammar
    grammar = setType(grammar)

    # set ls_cky[i][j] of sentence[i]
    for i in range(length):
        ls = []
        for j in range(len(grammar)):
            if sentence[i] in grammar[j][1]:
                ls.append(grammar[j][0])
        ls_cky[0].append(ls)

    for i in range(2, length):
        n = length - i + 1
        o = i - 1
        for j in range(1, length - i + 2):
            for k in range(1, i):
                # loi ham hop
                sym1 = ls_cky[k - 1][j - 1]
                a = i - k - 1
                b = j + k - 1
                sym2 = ls_cky[i - k - 1][j + k - 1]
                ls_sym = mulSym(sym1, sym2)
                res_check = checkSymbols(ls_sym, grammar)
                ls_cky[i - 1].append(res_check)
    print(ls_cky)

    return ls_cky

cky_data = CNF.ckyData1('test1.txt')
# print(cky.grammar, cky.sentence, cky.startSymbol)
_cky = cky(cky_data.sentence, cky_data.grammar)
for i in _cky:
    print(i)
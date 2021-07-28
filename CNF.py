import InputCNF as ICNF

# tach chuoi
def splitString(string):
    ls = []

    for i in string:
        ls.append(i)
    
    return ls

# hop chuoi
def megString(ls_string):
    _string = ''

    for i in ls_string:
        _string += i
    
    return _string

# Xoa ky tu epsilon trong chuoi
def delSym(split_string, sym_eps):
    new_ls_left = []

    for i in range(len(split_string)):
        temp_split = split_string.copy()
        if split_string[i] == sym_eps:
            temp_split.pop(i)
            new_ls_left.append(megString(temp_split))
    
    # Thêm phần vế trái không chứa ký tự rỗng nào
    temp_split = split_string.copy()
    for i in range(len(split_string)):
        if split_string[i] == sym_eps:
            temp_split.remove(sym_eps)
    
    if len(temp_split) != len(split_string):
        new_ls_left.append(megString(temp_split))
    
    new_ls_left = list(set(new_ls_left))

    # remove ''
    temp_split = list(set(new_ls_left))
    for i in temp_split:
        if i == '':
            new_ls_left.remove(i)
    
    return new_ls_left

# Xóa quy tắc rỗng
def delEmptyRule(rules):
    new_rules = []
    rules = ICNF.setType(rules)
    # left side
    left_side_eps = []

    # find left side of right side is epsilon
    # tìm vế trái của vế phải là rỗng
    for i in rules:
        if 'epsilon' in i[1]:
            left_side_eps.append(i[0])
            i[1].remove('epsilon')
    # tim cac phan tu khac cua tap rong
    temp_ε = left_side_eps.copy()
    for i in temp_ε:
        for j in rules:
            if i in j[1]:
                left_side_eps.append(j[0])

    if len(left_side_eps) > 0:
        for i in left_side_eps:
            for j in rules:
                # Vế phải mới sau khi xóa phần tử rỗng
                temp_right_rules = []

                for k in j[1]:
                    # tach cac phan ky tu cua ve phai
                    slipt_right = splitString(k)
                    new_left_side = delSym(slipt_right, i)
                    if len(new_left_side) > 0:
                        for l in new_left_side:
                            temp_right_rules.append(l)

                for k in range(len(j[1])):    
                    temp_right_rules.insert(k, j[1][k])

                # Thay vế phải mới vào quy tắc
                j[1] = temp_right_rules

    return rules

# delete single rule
# Xóa quy tắc đơn
def delSingleRule(rules, subAlphabet):
    new_rules = rules.copy()

    for i in range(len(rules)):
        if len(rules[i][1]) < 2 and rules[i][1] in subAlphabet:
            new_rules.pop(i)
    
    return new_rules

# Lấy ra quy tắc dạng A -> a, A -> BC
def getRulesStandard(mainAlphabet, subAlphabet, rules):
    for i in rules:
        if i[0] in subAlphabet:
            # kiểm tra vế phải là nhỏ hơn 2 ký tự và chỉ thuộc bảng ký hiệu phụ
            lenght_sym = len(i[1])
            check_sub = lenght_sym <= 2 & i[1]
            # Kiểm tra vế phải chỉ là 1 ký tự và thuộc bảng chữ cái chính



# cnf_data = ICNF.cnfData('test1.txt')
cnf_data = ICNF.cnfData('test2.txt')
# cnf_data.printCNF()
a = delEmptyRule(cnf_data.rules)
print(a)
# delEmptyRule(cnf_data.rules)
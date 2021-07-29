import copy as cp
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

# Removal of Null Productions
# Xóa quy tắc rỗng
def rmNullRules(rules):
    new_rules = []
    # rules = ICNF.setType(rules)
    # left side
    left_side_eps = []

    # find left side of right side is epsilon
    # tìm vế trái của vế phải là rỗng
    for i in rules:
        if 'epsilon' in i[1]:
            left_side_eps.append(i[0])
            i[1].remove('epsilon')
        elif len(i[1]) == 0 and i[0] not in left_side_eps:
            left_side_eps.append(i[0])

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

# Removal of Unit Productions
# Xóa quy tắc đơn

# Lấy ra vế phải của một quy tắc cần tìm
def getRightSide(rules, sym):
    ls = []
    
    # check sentence in grammar
    for j in rules:
        if sym in j[0]:
            ls = (j[1])

    return ls

# Lấy ra vế trái của các quy tắc đơn
def getLeftUnit(rules, subAlphabet):
    # Lấy ra vế trái của các quy tắc đơn
    ls_left_sig = []
    for i in rules:
        temp_right = []
        for j in i[1]:
            if len(j) < 2 and j in subAlphabet and i[0] in subAlphabet :
                temp_right.append(j)
        
        if len(temp_right) > 0:
            ls_left_sig.append([i[0], temp_right])

    return ls_left_sig

# Removal of Unit Productions
# Xóa quy tắc đơn
# Quy tắc đơn có dạng A -> B, AB không thuộc bảng ký hiệu phụ
def rmUnitRules(new_rules, subAlphabet, ls_left_sig):
    # Kiểm tra có tồn tại quy tắc đơn không
    # Nếu không có quy tắc đơn nào thì trả về bộ quy tăc
    if len(ls_left_sig) == 0:
        return new_rules

    # Nếu còn quy tắc đơn thì xóa và cập nhật lại bộ quy tắc
    else: 
        # Xoa tung quy tac don
        i = 0
        while i < len(ls_left_sig):
        # for i in ls_left_sig:
            for j in ls_left_sig[i][1]:
                # Lấy ra vế phải từ vế trái của quy tắc đơn
                get_right = getRightSide(new_rules, j)

                # Thay thế vế phải của quy tắc đơn
                k = 0
                check = True
                while check and k < len(new_rules):
                    if ls_left_sig[i][0] == new_rules[k][0]:
                        # Xóa phần vế phải của quy tắc đơn
                        id_l = 0
                        c_l = True
                        while c_l == True and id_l < len(new_rules[k][1]):
                            if new_rules[k][1][id_l] == j:
                                new_rules[k][1].pop(id_l)
                                c_l = False
                            else: id_l += 1

                        for gr in get_right:
                            new_rules[k][1].append(gr)
                        
                        check = False
                    else: k += 1
            ls_left_sig.pop(i)

        # Cập nhật lại các quy tắc đơn trong bộ quy tắc
        ls_left_sig = getLeftUnit(new_rules, subAlphabet)

        # Đệ quy
        return rmUnitRules(new_rules, subAlphabet, ls_left_sig)


# Removal of Useless rule
# loại bỏ các qui tắc dư thừa

# Loại bỏ quy tắc/biến vô sinh
# Những biến không dẫn ra được xâu kết thúc được gọi là biến vô sinh
def varNotTer(mainAlphabet, subAlphabet, rules, cnf):
    new_sub = []
    new_rules = cp.deepcopy(rules)
    ls_ter = []

    # add rules in main alphabet
    # thêm vào quy tắc có vế phải thuộc trong bảng chữ cái chính 
    for i in mainAlphabet:
        for j in rules:
            if i in j[1]:
                ls_ter.append(j[0])
    
    ls_ter = sorted(list(set(ls_ter)))

    # Thêm vào quy tắc mà vế phải có ký tự nằm trong bảng chữ cái chính và ls ter
    for i in rules:
        for j in i[1]:
            ls_split_left_rules = splitString(j)
            check_ter = True
            for k in ls_split_left_rules:
                if k in mainAlphabet or k in ls_ter:
                    pass
                else: check_ter = False
            if check_ter == True and i[0] not in ls_ter:
                ls_ter.append(i[0])

    # update new_rules
    i = 0
    while i < len(new_rules):

        # Nếu bắt đầu/vế trái quy tắc là ký tự không thuộc ls_ter thì xóa khỏi bộ quy tắc
        if new_rules[i][0] not in ls_ter:
            new_rules.pop(i)
        else:
            # Kiểm tra vế phải của quy tắc
            j = 0
            while j < len(new_rules[i][1]):
            # for j in range(len(new_rules[i][1])):
                s =new_rules[i][1][j]
                ls_split_left_rules = splitString(new_rules[i][1][j])
                check_ter = True
                for k in range(len(ls_split_left_rules)):
                    if ls_split_left_rules[k] in mainAlphabet or ls_split_left_rules[k] in ls_ter:
                        pass
                    else: check_ter = False
                # Nếu trong vế phải tồn tại ký tự không có trong ls_ter thì xóa bỏ
                if check_ter == False:
                    new_rules[i][1].pop(j)
                    # new_rules.append(rules[i])
                else: j += 1
            i += 1

    # Xóa bỏ các quy tắc rỗng mới
    new_rules = rmNullRules(new_rules)

    # Bảng ký hiệu phụ mới
    new_sub = ls_ter.copy()

    # update cnf
    # Cập nhật lại cnf
    cnf.subAlphabet = ls_ter
    cnf.rules = new_rules

    return cnf

# Loại bỏ nhứng biến không dẫn đến được
# Những biến không dẫn xuất ra được từ S được gọi là không dẫn đến được
def nonDerivable(mainAlphabet, subAlphabet, startSymbol, rules, cnf):
    new_sub = []
    new_main = []
    new_rules = []

    _der = [startSymbol]
    union_sub_main = list(set(mainAlphabet) | set(subAlphabet))

    check = True
    _der_loop = _der.copy()
    while check:
        temp_der = _der.copy()
        new_der = []

        for i in rules:
            if i[0] in _der_loop:
                for j in i[1]:
                    ls_split = splitString(j)
                    for k in ls_split:
                        new_der.append(k)

                        if k not in temp_der:
                            temp_der.append(k)
        if _der == temp_der:
            check = False
        else:
            _der = temp_der
            _der_loop = new_der
                    
    new_sub = list(set(subAlphabet) & set(_der))
    new_main = list(set(mainAlphabet) & set(_der))

    for i in rules:
        if i[0] in _der:
            new_rules.append(i)

    cnf.mainAlphabet = new_main
    cnf.subAlphabet = new_sub
    cnf.rules = new_rules

    return cnf


# Lấy ra quy tắc dạng A -> a, A -> BC
def getRulesStandard(mainAlphabet, subAlphabet, rules):
    new_rules = []
    up_rules = []

    for i in rules:
        # if i[0] in subAlphabet:
        new_ls_right = []
        for j in i[1]:
            # Kiểm tra vế phải chỉ là 1 ký tự và thuộc bảng chữ cái chính
            if len(j) == 1 and j in mainAlphabet:
                new_ls_right.append(j)

            # kiểm tra vế phải là 2 ký tự và chỉ thuộc bảng ký hiệu phụ
            elif len(j) == 2:
                ls_split = splitString(j)
                
                if ls_split[0] in subAlphabet and ls_split[1] in subAlphabet:
                    new_ls_right.append(j)
        # add new rules
        if len(new_ls_right) > 0:
            # Các quy tắc chuẩn
            new_rules.append([i[0], new_ls_right])

            # Các quy tắc chưa chuẩn
            dis = list(set(i[1]) -set(new_ls_right))
            if len(dis) > 0:
                up_rules.append([i[0], dis])
        else:
            up_rules.append(i)

    # Trả về một bộ 2 tập quy tắc
    # Tập quy tắc đầu đax thuộc dạng chuẩn
    # Tập quy tắc cuối chưa đạt chuẩn
    return new_rules, up_rules

# The right-hand rule transform contains both major and minor symbols
# Biến đổi quy tắc vế phải có chứa cả ký hiệu chính và ký hiệu phụ A -> bC
def transRightMainSub(tup_rules, mainAlphabet, subAlphabet):
    temp_tup_rules = cp.deepcopy(tup_rules)
    new_ls_rules = temp_tup_rules[0]
    new_ls_up = []
    new_sub = subAlphabet.copy()

    # kiểm tra các quy tắc gồm cả ký tự chính và phụ
    for i in temp_tup_rules[1]:
        left_new_ls_up = []
        temp_new_ls_rules = []

        for rg in i[1]:
            ls_split = splitString(rg)
            
            # Tìm những quy tắc gồm cả chính và phụ
            j = 0
            _ms = True
            check_ms = True

            while check_ms == True and j < len(ls_split):
                if ls_split[j] in mainAlphabet:
                    _ms = True
                    check_ms = False
                elif ls_split[j] in subAlphabet:
                    _ms = False
                    j += 1

            if _ms == False:
                # add right side of tules not standar
                # Thêm vế phải của tập quy tắc chưa đạt chuẩn (dạng: ABC)
                left_new_ls_up.append(rg)
            else:
                update_rules = ''

                for sp in range(len(ls_split)):
                    if ls_split[sp] in mainAlphabet:
                        # Thêm ký hiệu phụ mới C_i
                        sub_i = 'C_(' + ls_split[sp] + ')'
                        new_sub.append(sub_i)

                        # Thêm quy tắc mới
                        new_rules_i = [sub_i, [ls_split[sp]]]
                        if new_rules_i not in new_ls_rules:
                            new_ls_rules.append(new_rules_i)

                        # Cập nhật lại quy tắc cũ
                        ls_split[sp] = sub_i
                        meg = megString(ls_split)
                        update_rules = meg
                
                temp_new_ls_rules.append(update_rules)
        # Thêm vào quy tắc chưa đạt chuẩn
        if len(left_new_ls_up) > 0:
            new_ls_up.append([i[0], left_new_ls_up])

        # Thêm vào quy tắc đã đạt chuẩn
        if len(temp_new_ls_rules) > 0:
            for nr in new_ls_rules:
                if i[0] == nr[0]:
                    for rgn in temp_new_ls_rules:
                        nr[1].append(rgn)
    
    # Cập nhật lại bảng ký hiệu phụ
    new_sub = list(set(new_sub))

    # Trả về giá trị một bộ mới gồm 
    # 0-Quy tắc đạt chuẩn
    # 1-Quy tắc chưa đạt chuẩn
    # 2-Bảng ký hiệu phụ mới
    new_tup = (new_ls_rules, new_ls_up, new_sub)

    return new_tup
    

# Transform the rules where the right side has length greater than 2
# Biến đổi các quy tắc mà vế phải có độ dài lớn hơn 2
def transRightGeater2(tup_rules):
    temp_tup = cp.deepcopy(tup_rules)
    new_ls_rules = temp_tup[0]
    new_sub = temp_tup[2]

    # Biến đổi quy tắc mà vế phải có số ký tự lớn hơn 2
    temp_new_ls_rules = []
    for i in temp_tup[1]:

        temp_right_rules = []

        for j in i[1]:

            ls_split = splitString(j)
    
            # Thêm vào m - 2 ký tự phụ
            k = 0
            length = len(ls_split) - 1
            while k < length:
                # Thêm vào ký tự phụ thứ k đến m - 2, m = độ dài vế phải
                sub_i = 'C_(' + str(k) + ')'
                if sub_i not in new_sub and (k + length) != len(ls_split):
                    new_sub.append(sub_i)
                # Thêm vào quy tắc tương ứng với ký tự phụ mới
                if k == 0:
                    meg = megString([ls_split[k], sub_i])
                    # new_rulse_i = [i[0], [meg]]

                    if meg not in temp_right_rules:
                        temp_right_rules.append(meg)
            
                elif (k + length) == len(ls_split):
                    sub_i = 'C_(' + str(k - 1) + ')'
                    meg = megString([ls_split[k],ls_split[k+1]])
                    new_rulse_i = [sub_i, [meg]]

                    if new_rulse_i not in temp_new_ls_rules:
                        temp_new_ls_rules.append(new_rulse_i)
                    # else:
                else:
                    sub_next_i = 'C_(' + str(k+1) + ')'
                    meg = megString([ls_split[k],sub_next_i])
                    new_rulse_i = [sub_i, [meg]]
                    
                    if new_rulse_i not in temp_new_ls_rules:
                        temp_new_ls_rules.append(new_rulse_i)

                k += 1
        # Cập nhật lại vế phải quy tắc i
        if len(temp_right_rules) > 0:
            temp_right_rules = list(set(temp_right_rules))
            for nr in new_ls_rules:
                if nr[0] == i[0]:
                    for gr in temp_right_rules:
                        nr[1].append(gr)

    # Cập nhật thêm các quy tắc mới cho bộ quy tắc
    copy_ls_rules = cp.deepcopy(temp_new_ls_rules)
    i = 0
    while i < len(temp_new_ls_rules):
        new_rigt_rules = [temp_new_ls_rules[i][1][0]]
        j = i+1
        
        while j < len(temp_new_ls_rules):
            if temp_new_ls_rules[i][0] == temp_new_ls_rules[j][0]:
                new_rigt_rules.append(temp_new_ls_rules[j][1][0])
                temp_new_ls_rules.pop(j)
            else: j += 1
        
        new_ls_rules.append([temp_new_ls_rules[i][0], new_rigt_rules])
        temp_new_ls_rules.pop(i)
        
    # Trả về giá trị một bộ gồm
    # 0-Các quy tắc đạt chuẩn
    # 1-Bảng ký hiệu phụ mới

    return (new_ls_rules, new_sub)

# Chomsky Normal Form
# Văn phạm theo dạng chuẩn Chomsky
def updateRules(mainAlphabet, subAlphabet, startSymbol, rules):
    rules = cp.deepcopy(rules)
    new_rules = rmNullRules(rules)

cnf_data = ICNF.cnfData('test1.txt')
# cnf_data = ICNF.cnfData('test2.txt')
# cnf_data = ICNF.cnfData('test3.txt')
# cnf_data = ICNF.cnfData('test4.txt')
# cnf_data = ICNF.cnfData('test5.txt')
# cnf_data.printCNF()
rules = ICNF.setType(cnf_data.rules)

a = rmNullRules(rules)
# print(a)

b_1 = getLeftUnit(a, cnf_data.subAlphabet)
b = rmUnitRules(a, cnf_data.subAlphabet, b_1)
# print(b)
c = varNotTer(cnf_data.mainAlphabet, cnf_data.subAlphabet, b, cnf_data)
# print(c)
d = nonDerivable(c.mainAlphabet, c.subAlphabet, c.startSymbol, c.rules, c)
d.printCNF()

e = getRulesStandard(d.mainAlphabet, d.subAlphabet, d.rules)
f = transRightMainSub(e, d.mainAlphabet, d.subAlphabet)
g = transRightGeater2(f, d.mainAlphabet)
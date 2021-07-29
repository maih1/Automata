import copy as cp
import InputCNF as ICNF


def upForm(form, mainAlphabet):
    for i in mainAlphabet:
        new_form = 'C_(' + str(i) + ')'
        # new_form = 'C_(' + str(i) + ')'
        form.append(new_form)
    return form

# Split string
# Tách chuỗi 'C_(a)AC_(b)B'
def splitString(form, string):
    ls = []
    new_ls = []

    for i in string:
        ls.append(i)

    i = 0
    while i < len(ls):
        mg = ls[i]
        j = i + 1
        check = True
        while check == True and j < len(ls):
            if ls[j] not in form and mg not in form:
                check = False
            elif len(mg) == 5:
                check = False
            else:
                mg += ls[j]
                ls.pop(j)
        new_ls.append(mg)
        ls.pop(i)
    
    # i = 0
    # while i < len(ls):
    # # for i in rals:
    #     if ls[i] in form:
    #         ls.pop(i)
    #     else: i +=1

    return new_ls


# merger string
# Hợp chuỗi
def megString(ls_string):
    _string = ''

    for i in ls_string:
        _string += i
    
    return _string


# Remove null characters in string (epsilon)
# Xóa ký tự rỗng trong chuỗi
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


# Removal of Null Productions (epsilon)
# Xóa quy tắc rỗng
def rmNullRules(rules, form):
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
                    slipt_right = splitString(form, k)
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

# Get the right hand side of a rule to find
# Lấy ra vế phải của một quy tắc cần tìm
def getRightSide(rules, sym):
    ls = []
    
    for j in rules:
        if sym in j[0]:
            ls = (j[1])

    return ls


# Get the left hand side of unit rules
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
    # Check if single rule exists
    # If no unit rule is rule set is returned
    # Kiểm tra có tồn tại quy tắc đơn không
    # Nếu không có quy tắc đơn nào thì trả về bộ quy tăc
    if len(ls_left_sig) == 0:
        return new_rules

    # If there is a single rule, delete and update the rule set again
    # Nếu còn quy tắc đơn thì xóa và cập nhật lại bộ quy tắc
    else: 
        # Delete unit rule
        # Xóa từng quy tắc đơn
        i = 0
        while i < len(ls_left_sig):
        # for i in ls_left_sig:
            for j in ls_left_sig[i][1]:
                # Get the right side of a rule to find
                # Lấy ra vế phải từ vế trái của quy tắc đơn
                get_right = getRightSide(new_rules, j)

                # Substitute the right side of the unit rule
                # Thay thế vế phải của quy tắc đơn
                k = 0
                check = True
                while check and k < len(new_rules):
                    if ls_left_sig[i][0] == new_rules[k][0]:
                        # Remove right of unit rule
                        # Xóa phần vế phải của quy tắc đơn
                        id_l = 0
                        c_l = True
                        while c_l == True and id_l < len(new_rules[k][1]):
                            if new_rules[k][1][id_l] == j:
                                new_rules[k][1].pop(id_l)
                                c_l = False
                            else: id_l += 1

                        for gr in get_right:
                            if gr not in new_rules[k][1]:
                                new_rules[k][1].append(gr)
                        # for gr in get_right:
                        #     new_rules[k][1].append(gr)
                        
                        check = False
                    else: k += 1
            ls_left_sig.pop(i)

        # Update unit rules in the rule set
        # Cập nhật lại các quy tắc đơn trong bộ quy tắc
        ls_left_sig = getLeftUnit(new_rules, subAlphabet)

        # Recursive
        # Đệ quy
        return rmUnitRules(new_rules, subAlphabet, ls_left_sig)


# Removal of Useless rule
# loại bỏ các qui tắc dư thừa

# Remove inanimate rules/variables
# Step 1 − Include all symbols, W1, that derive some terminal and initialize i=1.
# Step 2 − Include all symbols, Wi+1, that derive Wi.
# Step 3 − Increment i and repeat Step 2, until Wi+1 = Wi.
# Step 4 − Include all production rules that have Wi in it.

# Loại bỏ quy tắc/biến vô sinh
# Những biến không dẫn ra được xâu kết thúc được gọi là biến vô sinh
def varNotTer(mainAlphabet, subAlphabet, rules, cnf, form):
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

    # Added the rule that the right side has a main alphabet character and ls_ter
    # Thêm vào quy tắc mà vế phải có ký tự nằm trong bảng chữ cái chính và ls ter
    for i in rules:
        for j in i[1]:
            ls_split_left_rules = splitString(form, j)
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

        # If the start / left side rules are not part ls_ter characters are removed from the set of rules
        # Nếu bắt đầu/vế trái quy tắc là ký tự không thuộc ls_ter thì xóa khỏi bộ quy tắc
        if new_rules[i][0] not in ls_ter:
            new_rules.pop(i)
        else:
            # Check left rules
            # Kiểm tra vế phải của quy tắc
            j = 0
            while j < len(new_rules[i][1]):
            # for j in range(len(new_rules[i][1])):
                s =new_rules[i][1][j]
                ls_split_left_rules = splitString(form, new_rules[i][1][j])
                check_ter = True
                for k in range(len(ls_split_left_rules)):
                    if ls_split_left_rules[k] in mainAlphabet or ls_split_left_rules[k] in ls_ter:
                        pass
                    else: check_ter = False

                # If there is a character in the right side that is not in ls_ter, delete it
                # Nếu trong vế phải tồn tại ký tự không có trong ls_ter thì xóa bỏ
                if check_ter == False:
                    new_rules[i][1].pop(j)
                    # new_rules.append(rules[i])
                else: j += 1
            i += 1

    # Remove new null rules
    # Xóa bỏ các quy tắc rỗng mới
    new_rules = rmNullRules(new_rules, form)

    # New sub-character
    # Bảng ký hiệu phụ mới
    new_sub = ls_ter.copy()

    # update cnf
    # Cập nhật lại cnf
    cnf.subAlphabet = ls_ter
    cnf.rules = new_rules

    return cnf

# Eliminate variables that do not lead to
# Step 1 − Include the start symbol in Y1 and initialize i = 1.
# Step 2 − Include all symbols, Yi+1, that can be derived from Yi and include all production rules that have been applied.
# Step 3 − Increment i and repeat Step 2, until Yi+1 = Yi.

# Loại bỏ nhứng biến không dẫn đến được
# Những biến không dẫn xuất ra được từ S được gọi là không dẫn đến được
def nonDerivable(mainAlphabet, subAlphabet, startSymbol, rules, cnf, form):
    new_sub = []
    new_main = []
    new_rules = []

    # The beginning of the rule is the start symbol
    # Bắt đầu quy tắc là tiên đề
    _der = [startSymbol]

    # Check the word axiomatic variable
    # Add rules derived from axioms
    # Kiểm tra từ biến tiên đề
    # Thêm vào những quy tắc dẫn ra từ tiên đề
    check = True
    _der_loop = _der.copy()

    # Iterate in addition to rules derived from axioms and from derived rules
    # Lặp những quy tắc dẫn ra được từ tiên đề và từ những quy tắc dẫn xuất
    while check:
        temp_der = _der.copy()
        new_der = []

        # Find the derived rules from the derived set
        # Add _der to the left side of the lead rule
        # Tìm những quy tắc dẫn được ra từ tập dẫn xuất
        # Thêm vào _der vế trái của quy tắc dẫn được
        for i in rules:
            if i[0] in _der_loop:
                for j in i[1]:
                    ls_split = splitString(form, j)
                    for k in ls_split:
                        new_der.append(k)

                        if k not in temp_der:
                            temp_der.append(k)

        # If the found rule set is the same as the previous rule set, the loop ends
        # Nếu tập quy tắc tìm được giống tập quy tắc trước đó thì kết thúc vòng lặp
        if _der == temp_der:
            check = False

        # If not update the loop again and continue
        # Nếu không cập nhật lại vòng lặp và tiếp tục
        else:
            _der = temp_der
            _der_loop = new_der

    # Update the main, minor alphabet and the set of birth rules
    # after removing the rules that don't lead        #    
    # Cập nhật lại bảng chữ cái chính, phụ và tập quy tắc sinh 
    # sau khi loại những quy tắc không dẫn đến được
    new_sub = list(set(subAlphabet) & set(_der))
    new_main = list(set(mainAlphabet) & set(_der))
    new_main = sorted(new_main)

    for i in rules:
        if i[0] in _der:
            new_rules.append(i)

    # update cnf
    # Cập nhật lại cnf
    cnf.mainAlphabet = new_main
    cnf.subAlphabet = new_sub
    cnf.rules = new_rules

    return cnf


# Get a rule of the form A -> a, A -> BC
# Lấy ra quy tắc dạng A -> a, A -> BC
def getRulesStandard(mainAlphabet, subAlphabet, rules, form):
    new_rules = []
    up_rules = []

    for i in rules:
        # if i[0] in subAlphabet:
        new_ls_right = []
        for j in i[1]:

            # Check that the right side is only 1 character and belongs to the main alphabet 
            # Kiểm tra vế phải chỉ là 1 ký tự và thuộc bảng chữ cái chính
            if len(j) == 1 and j in mainAlphabet:
                new_ls_right.append(j)

            # check the right hand side is 2 characters and belongs only to the secondary symbol table
            # kiểm tra vế phải là 2 ký tự và chỉ thuộc bảng ký hiệu phụ
            elif len(j) == 2:
                ls_split = splitString(form, j)
                
                if ls_split[0] in subAlphabet and ls_split[1] in subAlphabet:
                    new_ls_right.append(j)
        
        # add new rules
        if len(new_ls_right) > 0:
            # Standard rules
            # Các quy tắc chuẩn
            new_rules.append([i[0], new_ls_right])

            # Unstandardized rules
            # Các quy tắc chưa chuẩn
            dis = list(set(i[1]) -set(new_ls_right))
            if len(dis) > 0:
                up_rules.append([i[0], dis])
        else:
            up_rules.append(i)

    # Returns a set of 2 rule sets tập
    # 0-The rule set is already in standard form
    # 1-Unqualified set of rules
    # Trả về một bộ 2 tập quy tắc
    # 0-Tập quy tắc đã thuộc dạng chuẩn
    # 1-Tập quy tắc chưa đạt chuẩn
    
    return new_rules, up_rules

# get Left Rules
def getLeftRules(rules):
    left_rules = []

    for i in rules:
        left_rules.append(i[0])
    
    return left_rules

# The right-hand rule transform contains both major and minor symbols
# Biến đổi quy tắc vế phải có chứa cả ký hiệu chính và ký hiệu phụ A -> bC
def transRightMainSub(tup_rules, mainAlphabet, subAlphabet, form):
    temp_tup_rules = cp.deepcopy(tup_rules)
    new_ls_rules = temp_tup_rules[0]
    new_ls_up = []
    new_sub = subAlphabet.copy()

    # check the rules for both primary and secondary characters
    # kiểm tra các quy tắc gồm cả ký tự chính và phụ
    for i in temp_tup_rules[1]:
        left_new_ls_up = []
        temp_new_ls_rules = []

        for rg in i[1]:
            ls_split = splitString(form, rg)
            
            # Find rules that include both primary and secondary
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
                        # Add new sub-symbol C_i
                        # Thêm ký hiệu phụ mới C_i
                        sub_i = 'C_(' + ls_split[sp] + ')'
                        new_sub.append(sub_i)

                        # Add new rule
                        # Thêm quy tắc mới
                        new_rules_i = [sub_i, [ls_split[sp]]]
                        if new_rules_i not in new_ls_rules:
                            new_ls_rules.append(new_rules_i)

                        # Update old rules
                        # Cập nhật lại quy tắc cũ
                        ls_split[sp] = sub_i
                        meg = megString(ls_split)
                        update_rules = meg
                if len(ls_split) == 2:
                    temp_new_ls_rules.append(update_rules)
                else:
                    left_new_ls_up.append(update_rules)
        
        # Add non-standard rules
        # Thêm vào quy tắc chưa đạt chuẩn
        if len(left_new_ls_up) > 0:
            new_ls_up.append([i[0], left_new_ls_up])

        # Add the standard rule
        # Thêm vào quy tắc đã đạt chuẩn
        if len(temp_new_ls_rules) > 0:
            for nr in new_ls_rules:
                if i[0] == nr[0]:
                    for rgn in temp_new_ls_rules:
                        nr[1].append(rgn)
    
    # Update the sub-symbol
    # Cập nhật lại bảng ký hiệu phụ
    new_sub = list(set(new_sub))
    new_sub = sorted(new_sub)
    
    # Returns a new tuple of
    # 0-Qualifying Rule
    #1-The rule is not up to standard
    #2-New sub-symbol table
    # Trả về giá trị một bộ mới gồm 
    # 0-Quy tắc đạt chuẩn
    # 1-Quy tắc chưa đạt chuẩn
    # 2-Bảng ký hiệu phụ mới
    new_tup = (new_ls_rules, new_ls_up, new_sub)

    return new_tup
    

# Transform the rules where the right side has length greater than 2
# Biến đổi các quy tắc mà vế phải có độ dài lớn hơn 2
def transRightGeater2(tup_rules, form):
    temp_tup = cp.deepcopy(tup_rules)
    new_ls_rules = temp_tup[0]
    new_sub = temp_tup[2]

    # Transform the rules where the right side has length greater than 2
    # Biến đổi quy tắc mà vế phải có số ký tự lớn hơn 2
    temp_new_ls_rules = []
    for i in temp_tup[1]:

        temp_right_rules = []

        for j in i[1]:

            ls_split = splitString(form, j)

            # Add m - 2 sub characters
            # Thêm vào m - 2 ký tự phụ
            k = 0
            length = len(ls_split) - 1
            
            while k < length:
                # Add the kth extra character to m - 2, m = length on the right side
                # Thêm vào ký tự phụ thứ k đến m - 2, m = độ dài vế phải
                sub_i = 'C_(' + str(k) + ')'
                if sub_i not in new_sub and (k + 2) != len(ls_split):
                    new_sub.append(sub_i)

                # Added new subscript corresponding rule
                # Thêm vào quy tắc tương ứng với ký tự phụ mới
                if k == 0:
                    meg = megString([ls_split[k], sub_i])
                    # new_rulse_i = [i[0], [meg]]

                    if meg not in temp_right_rules:
                        temp_right_rules.append(meg)
            
                elif (k + 2) == len(ls_split):
                    sub_i = 'C_(' + str(k - 1) + ')'
                    meg = megString([ls_split[k],ls_split[k+1]])
                    new_rulse_i = [sub_i, [meg]]

                    if new_rulse_i not in temp_new_ls_rules:
                        temp_new_ls_rules.append(new_rulse_i)
                else:
                    sub_back_i = 'C_(' + str(k-1) + ')'
                    meg = megString([ls_split[k],sub_i])
                    new_rulse_i = [sub_back_i, [meg]]
                    
                    if new_rulse_i not in temp_new_ls_rules:
                        temp_new_ls_rules.append(new_rulse_i)

                k += 1
        
        # Update the right side of rule i
        # Cập nhật lại vế phải quy tắc i
        if len(temp_right_rules) > 0:
            temp_right_rules = list(set(temp_right_rules))
            getleft = getLeftRules(new_ls_rules)

            if i[0] in getleft:
                for nr in new_ls_rules:
                    if nr[0] == i[0]:
                        for gr in temp_right_rules:
                            nr[1].append(gr)
            else:
                new_ls_rules.append([i[0], temp_right_rules])

    # Update new rules for the rule set
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
      
    new_sub.sort()
    new_ls_rules.sort()
    # Returns a tuple of
    # 0-Qualified Rules
    #1-New sub-symbol table
    # Trả về giá trị một bộ gồm
    # 0-Các quy tắc đạt chuẩn
    # 1-Bảng ký hiệu phụ mới
    new_tup = (new_ls_rules, new_sub)

    return new_tup

# Chomsky Normal Form
# Văn phạm theo dạng chuẩn Chomsky
def cnf(_cnf):
    _cnf = cp.deepcopy(_cnf)
    form = ['(', ')', '_', 'C_(', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    form = upForm(form, _cnf.mainAlphabet)
    # Reset style for rule set
    # Thiết lập lại kiểu cho bộ quy tắc
    rules = ICNF.setType(_cnf.rules)

    # Delete null rules
    # Xóa các quy tắc rỗng
    rmNull = rmNullRules(rules, form)

    # Find single rules
    # Tìm các quy tắc đơn

    # Get the left side of a list of unit rules
    # Lấy ra vế trái của một danh sách các quy tắc đơn
    getLeft = getLeftUnit(rmNull, _cnf.subAlphabet)

    # Remove unit rules
    # Xóa quy tắc đơn
    rmUnit = rmUnitRules(rmNull, _cnf.subAlphabet, getLeft)

    # Remove inanimate rules/variables
    # Loại bỏ quy tắc/biến vô sinh
    _cnf = varNotTer(_cnf.mainAlphabet, _cnf.subAlphabet, rmUnit, _cnf, form)

    # Remove rules / variables that do not lead to the final
    # Loại bỏ nhứng quy tắc/biến không dẫn đến được
    _cnf = nonDerivable(_cnf.mainAlphabet, _cnf.subAlphabet, _cnf.startSymbol, _cnf.rules, _cnf, form)

    # Get rules of normal form
    # Lấy ra các quy tắc thuộc dạng chuẩn
    getRules = getRulesStandard(_cnf.mainAlphabet, _cnf.subAlphabet, _cnf.rules, form)
    
    # Transform the right rule that contains both major and minor symbols
    # Biến đổi quy tắc vế phải có chứa cả ký hiệu chính và ký hiệu phụ
    _transRightMainSub = transRightMainSub(getRules, _cnf.mainAlphabet, _cnf.subAlphabet, form)
    
    # Transform the rules where the right hand side has length greater than 2
    # Biến đổi các quy tắc mà vế phải có độ dài lớn hơn 2
    _transRightGeater2 = transRightGeater2(_transRightMainSub, form)

    # Update cnf
    # Cập nhật lại cnf

    # Update rules
    # Cập nhật lại tập quy tắc sinh
    _cnf.rules = _transRightGeater2[0]

    # Update the sub-Alphabet
    # Cập nhật lại bảng ký hiệu phụ
    _cnf.subAlphabet = _transRightGeater2[1]

    # The result is a Chomsky standard-form grammar
    # Kết quả là văn phạm dạng chuẩn Chomsky
    return _cnf


if __name__ == '__main__':
    # input data
    print('Input grammar:')
    cnf_data = ICNF.cnfData('./Data/CNF/test1.txt')
    # cnf_data = ICNF.cnfData('./Data/CNF/test2.txt')
    # cnf_data = ICNF.cnfData('./Data/CNF/test3.txt')
    # cnf_data = ICNF.cnfData('./Data/CNF/test4.txt')
    # cnf_data = ICNF.cnfData('./Data/CNF/test5.txt')

    cnf_data.printCNF()

    print('--------------------------------------')
    
    # Chomsky standard-form grammar
    # Văn phạm dạng chuẩn Chomsky
    print('Chomsky Normal Form:')

    _cnf = cnf(cnf_data)
    _cnf.printNewCNF()
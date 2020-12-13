import copy

production = {
    "T": ["#S#"],
    "S": ["aBd"],
    "B": ["bc"]
}

firstvt = {
    "T": set(),
    "S": set(),
    "B": set()
}

lastvt = {
    "T": set(),
    "S": set(),
    "B": set()
}

table = {
    "a": {},
    "b": {},
    "c": {},
    "d": {},
    "#": {}
}


def classify(s):
    if s.isupper():
        return "nonterminal"
    else:
        return "terminal"

# 懒得写算符优先文法的判断了...


while True:
    firstvt_bp = copy.deepcopy(firstvt)
    for left, right_list in production.items():
        for right in right_list:
            if classify(right[0]) == 'terminal':
                firstvt[left].add(right[0])
            else:  # nonterminal
                firstvt[left].update(firstvt[right[0]])
                # 算符优先文法不能出现相邻的非终结符，所以没必要再判断right[1]是否为terminal
                if len(right) >= 2:
                    firstvt[left].add(right[1])
    if firstvt == firstvt_bp:
        break

print(firstvt)

while True:
    lastvt_bp = copy.deepcopy(lastvt)
    for left, right_list in production.items():
        for right in right_list:
            last = right[len(right)-1]
            second_last = right[len(right)-2]
            if classify(last) == 'terminal':
                lastvt[left].add(last)
            else:  # nonterminal
                lastvt[left].update(lastvt[last])
                # 算符优先文法不能出现相邻的非终结符，所以没必要再判断second_last是否为terminal
                if len(right) >= 2:
                    lastvt[left].add(second_last)
    if lastvt == lastvt_bp:
        break

print(lastvt)

for left, right_list in production.items():
    for right in right_list:
        terminals = []
        for index, s in enumerate(right):
            try:
                type_ = classify(s)
                if type_ == 'terminal':
                    terminals.append(s)
                next = right[index+1]
                next_type_ = classify(next)
                if type_ == 'terminal' and next_type_ == 'nonterminal':
                    for t in firstvt[next]:
                        table[s][t] = '<'
                elif type_ == 'nonterminal':
                    for t in lastvt[s]:
                        table[t][next] = '>'
            except IndexError as e:
                pass
        for i, t in enumerate(terminals):
            j = i+1
            while j < len(terminals):
                table[t][terminals[j]] = '='
                j = j+1

print(table)

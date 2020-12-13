production = {
    "E": ["TG"],
    "G": ["+TG", "ε"],
    "T": ["FH"],
    "H": ["*FH", "ε"],
    "F": ["(E)", 'i']  # id简写成i
}

first = {'E': {'i', '('}, 'G': {'+', 'ε'}, 'T': {'i', '('},
         'H': {'ε', '*'}, 'F': {'i', '('}}

follow = {'E': {'#', ')'}, 'G': {'#', ')'}, 'T': {'#', ')', '+'},
          'H': {'#', ')', '+'}, 'F': {'#', '*', ')', '+'}}

select = []


def classify(s):
    if s.isupper():
        return "nonterminal"
    else:
        return "terminal"


i = 0
for left, right_list in production.items():
    for right in right_list:
        select.append(set())
        flag = 0
        for s in right:
            type_ = classify(s)
            if type_ == 'terminal':
                if s == 'ε':
                    flag = 1
                else:
                    select[i].add(s)
                break
            elif type_ == 'nonterminal':
                select[i].update(first[s])
                if 'ε' in first[s]:
                    flag = 1
                else:
                    flag = 0
                    break
        if flag:
            select[i].update(follow[left])
        i += 1

print(select)
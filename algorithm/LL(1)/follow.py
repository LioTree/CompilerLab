import copy

production = {
    "E": ["TG"],
    "G": ["+TG", "ε"],
    "T": ["FH"],
    "H": ["*FH", "ε"],
    "F": ["(E)", 'i']  # id简写成i
}

first = {'E': {'i', '('}, 'G': {'+', 'ε'}, 'T': {'i', '('},
         'H': {'ε', '*'}, 'F': {'i', '('}}

follow = {
    "E": {'#'},
    "G": set(),  # E'简写成G
    "T": set(),
    "H": set(),  # T'简写成H
    "F": set()
}


def classify(s):
    if s.isupper():
        return "nonterminal"
    else:
        return "terminal"


while True:
    follow_bp = copy.deepcopy(follow)
    for left, right_list in production.items():
        for right in right_list:
            temp = copy.deepcopy(follow[left])
            for s in reversed(right):
                type_ = classify(s)
                if type_ == 'terminal':
                    temp = {s}
                elif type_ == 'nonterminal':
                    follow[s].update(temp)
                    if not 'ε' in first[s]:
                        temp = copy.deepcopy(first[s])
                    else:
                        temp.update(first[s])

    if follow_bp == follow:
        break

for key, value in follow.items():
    try:
        value.remove('ε')
    except:
        pass

print(follow)

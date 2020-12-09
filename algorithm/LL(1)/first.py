import copy

production = {
    "E": ["TG"],
    "G": ["+TG", "ε"],
    "T": ["FH"],
    "H": ["*FH", "ε"],
    "F": ["(E)", 'i']  # id简写成i
}

first = {
    "E": set(),
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
    first_bp = copy.deepcopy(first)
    for left, right_list in production.items():
        for right in right_list:
            for s in right:
                type_ = classify(s)
                if type_ == 'terminal':
                    first[left].add(s)
                    break
                elif type_ == 'nonterminal':
                    first[left].update(first[s])
                    if not 'ε' in first[s]:
                        break
    if first_bp == first:
        break

print(first)

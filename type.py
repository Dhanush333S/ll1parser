import re
from parse_table import *

def read_grammar(filename):
    productions = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = re.split(r'\s*->\s*|\s*\|\s*|\s+', line.strip())
            non_terminal = parts[0]
            production = parts[1:]
            if non_terminal in productions:
                productions[non_terminal].extend(production)
            else:
                productions[non_terminal] = production
    return productions

def compute_first(productions):
    first_set = {}
    wanted={}
    for non_terminal in productions:
        first_set[non_terminal] = set()
        wanted[non_terminal]=set()

    for _ in range(len(first_set)*len(first_set)):
        for non_terminal, production in productions.items():
            for rule in production:
                for symbol in rule:
                    if symbol in first_set:
                        if len(wanted[symbol])==0 and len(first_set[symbol])!=0:
                            first_set[non_terminal].update(first_set[symbol])
                            if symbol in wanted[non_terminal]:
                                wanted[non_terminal].remove(symbol)
                        else:
                            wanted[non_terminal].add(symbol)
                        if '@' not in first_set[symbol]:
                            break
                    else:
                        first_set[non_terminal].add(symbol)
                        break

        repeat=False
        for _,w in wanted.items():
            if len(w)!=0:
                repeat=True
        if not repeat:
            break

    return first_set

def compute_follow(productions, first_set):
    follow_set = {non_terminal: set() for non_terminal in productions}
    follow_set[START_SYMBOL] = {'$'}
    for _ in range(len(follow_set)*len(follow_set)):
        for non_terminal, production in productions.items():
            for rule in production:
                for i, symbol in enumerate(rule):
                    if symbol in follow_set:
                        if i < len(rule) - 1:
                            pos=i+1
                            while pos<=len(rule)-1:
                                if rule[pos] not in first_set:
                                    follow_set[symbol].add(rule[pos])
                                    break
                                first_of_next = first_set[rule[pos]]
                                follow_set[symbol].update(first_of_next - {'@'})
                                if '@' in first_of_next:
                                    pos+=1
                                else:
                                    break                                    
                            if pos==len(rule):
                                follow_set[symbol].update(follow_set[non_terminal])
                        else:
                            follow_set[symbol].update(follow_set[non_terminal])

    return follow_set

if __name__ == "__main__":

    # Read the grammar from the file
    grammar_file = "grammar2.txt"
    productions = read_grammar(grammar_file)
    print(productions)
    first=compute_first(productions)
    print(first)

    START_SYMBOL='S'
    follow=compute_follow(productions,first)
    print(follow)

    build_parse_tree(productions,first,follow)
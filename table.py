import pandas as pd
from tabulate import tabulate
import sys
def parser(productions,first_set,follow_set):
    parse_table = {}  
    data = {}
    non_terminals = list(productions.keys())
    terminals = set()

    for non_terminal,production in productions.items():
        for rule in production:
            for symbol in rule:
                if symbol not in first_set:
                    terminals.add(symbol)
    terminals.add('$')
    terminals.remove('@')
    terminals = sorted(list(terminals))

    for terminal in terminals:
        data[terminal] = {non_terminal: '' for non_terminal in non_terminals}

    for non_terminal, table in parse_table.items():
        for terminal, rule in table.items():
            data[terminal][non_terminal] = rule

    df = pd.DataFrame(data)

    for non_terminal, production in productions.items():
        parse_table[non_terminal]={}
        for rule in production:
            pos=0
            parse_table[non_terminal][rule]=set()
            first=set()
            while pos<=len(rule)-1:
                if rule[pos] not in first_set :
                    if rule[pos]=='@':
                        first.update(follow_set[non_terminal])
                    else: 
                        first.add(rule[pos])
                    break
                first_of_next = first_set[rule[pos]]
                first.update(first_of_next - {'@'})
                if '@' in first_set[rule[pos]]:
                    pos+=1
                else:
                    break
            if pos==len(rule):
                if rule[pos] not in first_set:
                    first.add(rule[pos])
                else:
                    first.add(follow_set(rule[pos]))
            parse_table[non_terminal][rule].update(first)

            for t in first:
                if df.at[non_terminal,t] == "":
                    df.at[non_terminal, t] = rule
                else:
                    print(f"Conflict at {non_terminal} - {t}. Grammar is not LL1. Please resolve conflicts.")
                    sys.exit(1)   

    print('-------------------------------------------------------------------------------------------------------')
    print('Parsing Table')
    print('-------------------------------------------------------------------------------------------------------')
    print("\n")   
    print(tabulate(df, headers='keys', tablefmt='grid'))
    print("\n")   
    return parse_table 
def parser(productions,first_set,follow_set):

    for non_terminal, production in productions.items():
        print(non_terminal,' :')
        for rule in production:
            pos=0
            first=set()
            while pos<=len(rule)-1:
                if rule[pos] not in first_set :
                    if rule[pos]=='@':
                        first.update(follow_set[non_terminal])
                    else: 
                        first.add(rule[pos])
                    break
                first_of_next = first_set[rule[pos]]
                # print(first_of_next)
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
            print(rule,' -> ',first)


START_SYMBOL='E'
# productions={'S': ['(L)', 'a'], 'L': ['SP'], 'P': ['@', ',SP']}
# first_set={'S': {'a', '('}, 'L': {'a', '('}, 'P': {'@', ','}}
# follow_set={'S': {',', ')', '$'}, 'L': {')'}, 'P': {')'}}  


# productions={'S': ['aSbS', 'bSaS', '@']}
# first_set={'S': {'@', 'a', 'b'}}
# follow_set={'S': {'a', 'b', '$'}}

# productions={'E': ['TF'], 'F': ['+TF', '@'], 'T': ['GH'], 'H': ['*GH', '@'], 'G': ['a', '(E)']}
# first_set={'E': {'a', '('}, 'F': {'@', '+'}, 'T': {'a', '('}, 'H': {'*', '@'}, 'G': {'a', '('}}
# follow_set={'E': {')', '$'}, 'F': {')', '$'}, 'T': {')', '$', '+'}, 'H': {')', '$', '+'}, 'G': {'*', ')', 
# '$', '+'}}

# parser(productions,first_set,follow_set)
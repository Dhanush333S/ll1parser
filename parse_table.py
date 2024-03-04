import pandas as pd

def build_parse_tree(productions,first_set,follow_set):
    class LL1ParserError(Exception):
        pass

    def generate_parse_table(productions, first_set, follow_set):
        parse_table = {}

        for non_terminal, production in productions.items():
            for rule in production:
                first_of_rule = first(rule, productions)
                for symbol in first_of_rule:
                    if symbol != '@':
                        if (non_terminal, symbol) in parse_table:
                            raise LL1ParserError(f"Conflict at ({non_terminal}, {symbol}): {parse_table[non_terminal, symbol]} vs {rule}")
                        parse_table[non_terminal, symbol] = rule

                if '@' in first_of_rule or ('@' in first_set[non_terminal] and '$' in follow_set[non_terminal]):
                    for follow_symbol in follow_set[non_terminal]:
                        if (non_terminal, follow_symbol) in parse_table:
                            raise LL1ParserError(f"Conflict at ({non_terminal}, {follow_symbol}): {parse_table[non_terminal, follow_symbol]} vs @")
                        parse_table[non_terminal, follow_symbol] = '@'

        return parse_table

    def first(s, productions):
        ans = set()
        if not s:
            return ans
        
        c = s[0]
        
        if c.isupper():
            for st in productions[c]:
                if st == '@':
                    if len(s) > 1:
                        ans = ans.union(first(s[1:], productions))
                    else:
                        ans = ans.union('@')
                else:    
                    f = first(st, productions)
                    ans = ans.union(x for x in f)
        else:
            ans = ans.union(c)
        
        return ans

    try:
        parsing_table = generate_parse_table(productions, first_set, follow_set)

        # Display the LL(1) Parsing Table
        print("\nLL(1) Parsing Table:")
        df = pd.DataFrame(parsing_table, index=["Production"]).transpose().fillna('-')
        print(df)

    except LL1ParserError as e:
        print(f"\nError in LL(1) parsing table generation: {str(e)}")
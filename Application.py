from tabulate import tabulate
def apply_ll1_parser(input_string,START_SYMBOL,first,parse_table):
    input_string += "$"
    stack = ["$", START_SYMBOL]
    i = 0
    result = []

    while i < len(input_string) and stack:
        letter = input_string[i]
        top = stack.pop()

        if top not in first:
            if top == letter:
                i += 1
            else:
                result.append([input_string[:i], i, ''.join(stack), "Invalid !!"])
                break
        else:
            push = ""
            for rule in parse_table[top]:
                if letter in parse_table[top][rule]:
                    push = rule
                    break
            if push == "":
                result.append([input_string[:i], i, ''.join(stack), "Invalid"])
                break

            if push != "@":
                for p in reversed(push):
                    stack.append(p)

        result.append([input_string[:i], i, ''.join(stack), ""])
        
    if stack:
        result.append([input_string[:i], i, ''.join(stack), "Invalid !!"])
    else:
        result.append([input_string[:i], i, ''.join(stack), "Valid"])

    print(tabulate(result, headers=["Input String", "Index", "Stack", "Validation"], tablefmt="grid"))

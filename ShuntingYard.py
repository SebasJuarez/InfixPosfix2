def get_precedence(op):
    precedences = {'(': 1, '|': 2, '.': 3, '?': 4, '*': 4, '+': 4, '^': 5}
    return precedences.get(op, -1)

def format_reg_ex(regex):
    
    all_operators = {'|', '?', '+', '*', '^'}
    res = ""
    i = 0

    while i < len(regex):
        c1 = regex[i]
        res += c1

        if i + 1 < len(regex):
            c2 = regex[i + 1]
            if (c1 not in all_operators and c1 != '(' and
                c2 not in all_operators and c2 != ')' and c2 != '*'):
                res += '.'

        i += 1

    return res

def infix_to_postfix(regex):
    formatted_regex = format_reg_ex(regex)  
    all_operators = {'|', '?', '+', '*', '^', '.'} 
    stack = []
    postfix = ""
    steps = []

    i = 0
    while i < len(formatted_regex):
        c = formatted_regex[i]
        if c == '(':
            stack.append(c)
            steps.append("Se mueve '(' al stack")
        elif c == ')':
            while stack and stack[-1] != '(':
                popped = stack.pop()
                postfix += popped
                steps.append(f"Se borra {popped} del stack y se añade a la salida")
            stack.pop()  
            steps.append("Se borra '(' del stack sin añadir a la salida")
        elif c in all_operators or c == '.':
            while stack and get_precedence(stack[-1]) >= get_precedence(c):
                popped = stack.pop()
                postfix += popped
                steps.append(f"Se borra {popped} del stack y se añade a la salida")
            stack.append(c)
            steps.append(f"Se mueve '{c}' al stack")
        else:
            postfix += c
            steps.append(f"Se añade '{c}' directamente a la salida")
        i += 1

    while stack:
        popped = stack.pop()
        postfix += popped
        steps.append(f"Se borra {popped} del stack y se añade a la salida")

    return postfix


def read_and_convert(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                print(line)
                if line: 
                    postfix = infix_to_postfix(line)
                    yield postfix
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{file_path}'. Asegúrate de que está en el directorio correcto.")
        return

if __name__ == '__main__':    
    file_path = 'expressions.txt'
    for postfix in read_and_convert(file_path):
        print(postfix)

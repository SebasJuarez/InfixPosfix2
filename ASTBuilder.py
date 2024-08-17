from ShuntingYard import read_and_convert
import sys
import graphviz

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class UnaryOperator(Node):
    def __init__(self, value, child):
        super().__init__(value)
        self.child = child

class BinaryOperator(Node):
    def __init__(self, value, left, right):
        super().__init__(value)
        self.left = left
        self.right = right

def build_ast(postfix):
    stack = []
    operators = {'|', '.', '*', '?', '+'}  # Asegúrate de que todos tus operadores están aquí

    print(f"Construyendo AST para: {postfix}")  # Debugging: Muestra la expresión postfija

    for char in postfix:
        if char in operators:
            if char in {'*', '?'}:  # Operadores unarios
                if not stack:
                    raise Exception(f"No hay suficientes operandos para el operador unario {char}")
                operand = stack.pop()
                node = UnaryOperator(char, operand)
            else:  # Operadores binarios
                if len(stack) < 2:
                    raise Exception(f"No hay suficientes operandos para el operador binario {char}")
                right = stack.pop()
                left = stack.pop()
                node = BinaryOperator(char, left, right)
            stack.append(node)
        else:
            stack.append(Node(char))

    if len(stack) != 1:
        raise Exception("Más de un elemento en la pila después de procesar la expresión, probablemente un error en la entrada")

    return stack.pop()  # Nodo raíz del AST


def visualize_ast(root):
    dot = graphviz.Digraph(comment='AST', format='png')
    def add_nodes_edges(node):
        # Crear un nodo en Graphviz
        dot.node(str(id(node)), label=str(node.value))
        if hasattr(node, 'child'):  # Si es un operador unario
            dot.edge(str(id(node)), str(id(node.child)))
            add_nodes_edges(node.child)
        if hasattr(node, 'left'):  # Si es un operador binario
            dot.edge(str(id(node)), str(id(id(node.left))))
            add_nodes_edges(node.left)
            dot.edge(str(id(node)), str(id(id(node.right))))
            add_nodes_edges(node.right)
    add_nodes_edges(root)
    return dot


if __name__ == '__main__':
    file_path = 'expressions.txt'
    postfix_expressions = read_and_convert(file_path)
    for postfix, steps in postfix_expressions:
        print(f"Postfix recibido: {postfix}")  # Esto te ayudará a ver qué recibe realmente `build_ast`
        ast_root = build_ast(postfix)
        dot = visualize_ast(ast_root)
        dot.render('output', view=True)  # Guarda y muestra el gráfico


import graphviz
from ShuntingYard import read_and_convert

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
    operators = {'|', '.', '*', '?', '+'}
    print(f"Construyendo AST para la expresión postfija: {postfix}")
    for char in postfix:
        if char in operators:
            if char in {'*', '?', '+'}:
                operand = stack.pop()
                node = UnaryOperator(char, operand)
            else:
                right = stack.pop()
                left = stack.pop()
                node = BinaryOperator(char, left, right)
            stack.append(node)
        else:
            stack.append(Node(char))
    return stack.pop()

def visualize_ast(root):
    dot = graphviz.Digraph(comment='AST', format='png')

    def add_nodes_edges(node):
        if node is not None:
            dot.node(str(id(node)), label=str(node.value))
            # Verifica si hay un hijo y luego recursivamente añade nodos/aristas
            if hasattr(node, 'child') and node.child is not None:
                dot.edge(str(id(node)), str(id(node.child)))
                add_nodes_edges(node.child)
            if hasattr(node, 'left') and node.left is not None:
                dot.edge(str(id(node)), str(id(node.left)))
                add_nodes_edges(node.left)
            if hasattr(node, 'right') and node.right is not None:
                dot.edge(str(id(node)), str(id(node.right)))
                add_nodes_edges(node.right)

    add_nodes_edges(root)
    dot.render('output', view=True)

if __name__ == '__main__':
    file_path = 'expressions.txt'
    postfix_expressions = read_and_convert(file_path)
    for postfix in postfix_expressions:
        print(f"Expresión postfija: {postfix}")
        ast_root = build_ast(postfix)
        visualize_ast(ast_root)

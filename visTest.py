import ast
from graphviz import Digraph

def parse_java_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return ast.parse(code)

def create_flow_diagram(tree, output_path='flow_diagram'):
    dot = Digraph(comment='Task Management Service Flow Diagram', format='png')

    def visit_node(node):
        if isinstance(node, ast.FunctionDef):
            dot.node(str(node.lineno), node.name, shape='box')
            for stmt in node.body:
                if isinstance(stmt, ast.Return):
                    dot.node(str(stmt.lineno), 'Return', shape='box')
                    dot.edge(str(node.lineno), str(stmt.lineno))
                elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                    dot.node(str(stmt.lineno), 'Method Call', shape='box')
                    dot.edge(str(node.lineno), str(stmt.lineno))
                    visit_node(stmt.value)
                elif isinstance(stmt, ast.Assign):
                    dot.node(str(stmt.lineno), 'Assignment', shape='box')
                    dot.edge(str(node.lineno), str(stmt.lineno))
                    for target in stmt.targets:
                        if isinstance(target, ast.Attribute):
                            dot.node(str(target.lineno), 'Attribute', shape='box')
                            dot.edge(str(stmt.lineno), str(target.lineno))

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            visit_node(node)

    dot.render(output_path, cleanup=True)

if __name__ == '__main__':
    java_file_path = 'service.java'  # Replace with the actual path to your Java file
    ast_tree = parse_java_file(java_file_path)
    create_flow_diagram(ast_tree)

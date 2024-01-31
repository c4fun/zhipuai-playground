import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.structure = {}

    def visit_ClassDef(self, node):
        self.structure[node.name] = {'methods': []}
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if isinstance(node.parent, ast.ClassDef):
            self.structure[node.parent.name]['methods'].append(node.name)
        self.generic_visit(node)

def attach_parent_nodes(node, parent=None):
    for child in ast.iter_child_nodes(node):
        child.parent = parent
        attach_parent_nodes(child, parent=node)

def analyze_code(code):
    tree = ast.parse(code)
    attach_parent_nodes(tree)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.structure

# Example usage
code = """
class MyClass:
    def method_one(self):
        pass

    def method_two(self):
        pass

def individual_func1(var1):
    return var1

def individual_func2(var2):
    return var2
"""

result = analyze_code(code)
print(result)

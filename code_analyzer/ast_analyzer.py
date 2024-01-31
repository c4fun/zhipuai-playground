import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.structure = {"classes": {}, "functions": []}
        self.current_class = None

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.structure["classes"][node.name] = {'methods': []}
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        if self.current_class is not None:
            self.structure["classes"][self.current_class]['methods'].append(node.name)
        else:
            self.structure["functions"].append(node.name)
        self.generic_visit(node)

def analyze_code(code):
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.structure

# Example usage
code = """
ultimate_answer = 42
class MyClass:
    def method_one(self):
        pass

    def method_two(self):
        pass

def individual_func1(var1):
    print(ultimate_answer)
    return var1

def individual_func2(var2):
    return var2
"""

result = analyze_code(code)
print(result)

import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.structure = {
            "classes": {}, 
            "functions": {}, 
            "global_variables": []
        }
        self.current_class = None
        self.current_method = None
        self.current_function = None

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.structure["classes"][node.name] = {'methods': {}, 'class_variables': []}
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        function_name = node.name
        if self.current_class is not None:
            self.current_method = function_name
            self.structure["classes"][self.current_class]['methods'][function_name] = {'method_variables': []}
        else:
            self.current_function = function_name
            self.structure["functions"][function_name] = {'function_variables': []}
        self.generic_visit(node)
        self.current_method = None
        self.current_function = None

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                variable_name = target.id
                if self.current_class is not None:
                    if self.current_method is not None:
                        # Variable inside a method
                        self.structure["classes"][self.current_class]['methods'][self.current_method]['method_variables'].append(variable_name)
                    else:
                        # Class variable
                        self.structure["classes"][self.current_class]['class_variables'].append(variable_name)
                elif self.current_function is not None:
                    # Variable inside a function
                    self.structure["functions"][self.current_function]['function_variables'].append(variable_name)
                else:
                    # Global variable
                    self.structure["global_variables"].append(variable_name)
        self.generic_visit(node)

def analyze_code(code):
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.structure

# Example usage
code = """
class MyClass:
    class_var = 10

    def method_one(self):
        method_var = 20

    def method_two(self):
        pass

global_var = 30

def individual_func1(var1):
    func_var = 40
    return var1

def individual_func2(var2):
    return var2
"""

result = analyze_code(code)
print(result)

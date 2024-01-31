import ast
import json

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
        self.structure["classes"][node.name] = {
            'methods': {}, 
            'class_variables': [],
            'line_number': node.lineno
        }
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        function_name = node.name
        method_variables = self.extract_variables(node)
        parameters = self.extract_parameters(node)
        if self.current_class is not None:
            self.current_method = function_name
            self.structure["classes"][self.current_class]['methods'][function_name] = {
                'method_variables': method_variables,
                'parameters': parameters,
                'line_number': node.lineno
            }
        else:
            self.current_function = function_name
            self.structure["functions"][function_name] = {
                'function_variables': method_variables,
                'parameters': parameters,
                'line_number': node.lineno
            }
        self.current_method = None
        self.current_function = None

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                variable_name = target.id
                variable_info = {'name': variable_name, 'line_number': node.lineno}
                if self.current_class is not None and self.current_method is None:
                    # Class variable
                    self.structure["classes"][self.current_class]['class_variables'].append(variable_info)
                elif self.current_function is None and self.current_class is None:
                    # Global variable
                    self.structure["global_variables"].append(variable_info)
        self.generic_visit(node)

    def extract_variables(self, node):
        variables = []
        for n in node.body:
            if isinstance(n, ast.Assign):
                for target in n.targets:
                    if isinstance(target, ast.Name):
                        variable_info = {'name': target.id, 'line_number': n.lineno}
                        variables.append(variable_info)
        return variables

    def extract_parameters(self, node):
        return [{'name': arg.arg, 'line_number': node.lineno} for arg in node.args.args]

def analyze_code_from_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.structure

# Example usage with a file path
file_path = '/home/richardliu/code/github.com/geekan/MetaGPT/metagpt/provider/zhipuai_api.py'  # Replace with the path to your Python file

result = analyze_code_from_file(file_path)
json_result = json.dumps(result, indent=4)
print(json_result)

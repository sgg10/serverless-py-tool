import ast
from pathlib import Path


class ImportVisitor(ast.NodeVisitor):

    def __init__(self) -> None:
        super().__init__()
        self.modules = set()
        self.env_vars = set()

    def visit_Import(self, node):
        for name in node.names:
            self.modules.add(name.name.split('.')[0])

    def visit_ImportFrom(self, node):
        self.modules.add(node.module.split('.')[0])

    def visit_Call(self, node):
        # Check if this is a call to os.environ.get
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == 'get':
                parent_node = node.func.value
                if isinstance(parent_node, ast.Attribute) and parent_node.attr == 'environ':
                    grand_parent_node = parent_node.value
                    if isinstance(grand_parent_node, ast.Name) and grand_parent_node.id == 'os':
                        if len(node.args) > 0 and (isinstance(node.args[0], ast.Str) or isinstance(node.args[0], ast.Constant)):
                            self.env_vars.add(node.args[0].value)
        self.generic_visit(node)

    def visit_Subscript(self, node):
        # Check if this is an access to os.environ using subscript notation
        if isinstance(node.value, ast.Attribute):
            if node.value.attr == 'environ':
                parent_node = node.value.value
                if isinstance(parent_node, ast.Name) and parent_node.id == 'os':
                    if isinstance(node.slice, ast.Str) or isinstance(node.slice, ast.Constant):
                        self.env_vars.add(node.slice.value)
                    elif isinstance(node.slice, ast.Index):
                        if isinstance(node.slice.value, ast.Str) or isinstance(node.slice.value, ast.Constant):
                            self.env_vars.add(node.slice.value.value)
        self.generic_visit(node)

    def get_modules(self):
        return self.modules

    def get_env_variables(self):
        return self.env_vars


def analyze_lambda_fucntion(lambda_base_path, layers):
    lambdas = {}
    path = Path(lambda_base_path)
    visitor = ImportVisitor()
    for lambda_fucntion in (x for x in path.glob("*") if x.is_dir()):
        env_variables = []
        associated_layer = []
        for file in (f for f in lambda_fucntion.glob("*.py")):
            with file.open("r") as f:
                tree = ast.parse(f.read())
            visitor.visit(tree)
            env_variables = visitor.get_env_variables()
            imported_modules = visitor.get_modules()

            # Find assocciated layers
            for layer, content in layers.items():
                if any(m in content["modules"] for m in imported_modules):
                    associated_layer.append(layer)

        lambdas[lambda_fucntion.name] = {
            "layers": list(associated_layer),
            "envs": list(env_variables),
            "path": f"{lambda_base_path}/{lambda_fucntion.name}"
        }
    return lambdas

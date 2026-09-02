import ast


def count_function_arguments(function):
    """Count all types of function arguments using the AST."""
    arguments = function.args

    count = (
        len(arguments.posonlyargs)
        + len(arguments.args)
        + len(arguments.kwonlyargs)
    )

    if arguments.vararg is not None:
        count += 1

    if arguments.kwarg is not None:
        count += 1

    return count


class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        pass

    def visit_AsyncFunctionDef(self, node):
        pass


def calculate_complexity(function):
    visitor = ComplexityVisitor()

    for node in function.body:
        visitor.visit(node)

    return visitor.complexity
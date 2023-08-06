import ast
import sys
from typing import (
    Any,
    Dict,
    Generator,
    List,
    NamedTuple,
    Iterable,
    Optional,
    Tuple,
    Type,
)


if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


class Problem(NamedTuple):
    line: int
    col: int
    description: str


class BaseVisitor(ast.NodeVisitor):
    def __init__(self):
        self.problems: List[Problem] = []

    def extend_problems(self, problems: Iterable[Problem]):
        self.problems.extend(problems)


class CheckImportsVisitor(BaseVisitor):
    def __init__(self, alternatives: Dict[str, Tuple[str, str]]):
        self.alternatives = alternatives
        super().__init__()

    def _get_problems(self, line, col, module_name: Optional[str]) -> List[Problem]:
        if module_name is None:
            return []
        if module_name in self.alternatives:
            err_code, alt_module = self.alternatives[module_name]
            return [
                Problem(
                    line,
                    col,
                    f"{err_code} found import of '{module_name}' module. "
                    f"Please use '{alt_module}' instead.",
                )
            ]
        return []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.extend_problems(
                self._get_problems(node.lineno, node.col_offset, alias.name)
            )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.extend_problems(
            self._get_problems(node.lineno, node.col_offset, node.module)
        )
        self.generic_visit(node)


class CheckForbiddenConstantSubstringsVisitor(BaseVisitor):
    def __init__(self, forbidden_substrings: Dict[Any, Tuple[str, str]]):
        self.forbidden_substrings = forbidden_substrings
        super().__init__()

    def _get_problems(self, line, col, constant_value) -> List[Problem]:
        if not isinstance(constant_value, str):
            return []
        return [
            Problem(line, col, f"{err_code} {message}")
            for substring, (err_code, message) in self.forbidden_substrings.items()
            if substring in constant_value
        ]

    def visit_Constant(self, node: ast.Constant) -> None:
        self.extend_problems(
            self._get_problems(node.lineno, node.col_offset, node.value)
        )
        self.generic_visit(node)

    def visit_Str(self, node: ast.Str) -> None:
        self.extend_problems(self._get_problems(node.lineno, node.col_offset, node.s))
        self.generic_visit(node)


class CheckForbiddenFunctionCallVisitor(BaseVisitor):
    def __init__(self, forbidden_function_calls: Dict[Any, Tuple[str, str]]):
        self.forbidden_function_calls = forbidden_function_calls
        super().__init__()

    def _get_problems(self, line, col, expression_value) -> List[Problem]:
        if not isinstance(expression_value, ast.Call):
            return []
        function = expression_value.func
        if not isinstance(function, ast.Name):
            return []
        function_name = function.id
        if function_name in self.forbidden_function_calls:
            err_code, alt_function = self.forbidden_function_calls[function_name]
            return [
                Problem(
                    line,
                    col,
                    f"{err_code} found call to '{function_name}' function. "
                    f"Please use '{alt_function}' instead.",
                )
            ]
        return []

    def visit_Expr(self, node: ast.Expr) -> None:
        self.extend_problems(
            self._get_problems(node.lineno, node.col_offset, node.value)
        )
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:

        visitors = [
            CheckImportsVisitor(
                {
                    "requests": ("SG100", "sgrequests"),
                    "selenium": ("SG101", "sgselenium"),
                }
            ),
            CheckForbiddenConstantSubstringsVisitor(
                {
                    "sslproxies.org": (
                        "SG200",
                        "found possible use of external proxy 'sslproxies.org'. "
                        "We currently only support the Apify proxy.",
                    )
                }
            ),
            CheckForbiddenFunctionCallVisitor(
                {
                    "print": ("SG300", "sglogging"),
                }
            ),
        ]

        for visitor in visitors:
            visitor.visit(self._tree)

        problems = [problem for visitor in visitors for problem in visitor.problems]

        for problem in problems:
            yield (
                problem.line,
                problem.col,
                problem.description,
                type(self),
            )

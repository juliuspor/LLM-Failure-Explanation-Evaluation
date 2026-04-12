import ast
import textwrap


class AlphaRenamer(ast.NodeTransformer):
    """
    AST transformer that renames locally-defined variables to canonical
    names (v0, v1, v2, ...) based on order of definition.
    
    Scope-aware: Only renames variables that are assigned within the
    function scope. External references (cls.UTC, FieldUtils.method(),
    built-ins like ValueError) are NOT renamed.
    """
    
    def __init__(self):
        super().__init__()
        self.local_vars = set()  # Track names defined in this scope
        self.name_map = {}       # Original name -> canonical name
        self.counter = 0
    
    def _collect_local_definitions(self, node):
        """First pass: identify all locally-defined variable names."""
        for child in ast.walk(node):
            # Assignment targets
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Store):
                self.local_vars.add(child.id)
            # Function parameters
            if isinstance(child, ast.arg):
                self.local_vars.add(child.arg)
            # Exception handler names
            if isinstance(child, ast.ExceptHandler) and child.name:
                self.local_vars.add(child.name)
    
    def _get_canonical_name(self, original: str) -> str:
        """Get or create a canonical name for a local variable."""
        if original not in self.name_map:
            self.name_map[original] = f"v{self.counter}"
            self.counter += 1
        return self.name_map[original]
    
    def visit_FunctionDef(self, node):
        """Rename parameters and process function body."""
        for arg in node.args.args:
            if arg.arg in self.local_vars:
                arg.arg = self._get_canonical_name(arg.arg)
        self.generic_visit(node)
        return node
    
    def visit_Name(self, node):
        """Rename only locally-defined variables."""
        if node.id in self.local_vars:
            node.id = self._get_canonical_name(node.id)
        return node
    
    def visit_ExceptHandler(self, node):
        """Rename exception variable if it was locally defined."""
        if node.name and node.name in self.local_vars:
            node.name = self._get_canonical_name(node.name)
        self.generic_visit(node)
        return node


def normalize_python_code(code_str: str, alpha_rename: bool = True) -> str:
    """
    Normalizes Python code using AST to remove comments, docstrings,
    and canonicalize formatting (whitespace, quotes, etc.).
    
    If alpha_rename=True, also renames local variables to canonical 
    names for structural comparison.
    """
    if not code_str or not code_str.strip():
        return ""
    
    try:
        # 1. Parse into AST
        tree = ast.parse(textwrap.dedent(code_str))
        
        # 2. Remove Docstrings
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                if (node.body and isinstance(node.body[0], ast.Expr) and 
                    isinstance(node.body[0].value, ast.Constant) and 
                    isinstance(node.body[0].value.value, str)):
                    node.body.pop(0)
        
        # 3. Alpha-rename local variables
        if alpha_rename:
            renamer = AlphaRenamer()
            renamer._collect_local_definitions(tree)
            tree = renamer.visit(tree)
            ast.fix_missing_locations(tree)
        
        # 4. Unparse back to string
        return ast.unparse(tree)
        
    except SyntaxError:
        # Fallback for ill-formed snippets
        lines = [line.strip() for line in code_str.splitlines() 
                 if line.strip() and not line.strip().startswith("#")]
        return "\n".join(lines)
    except Exception:
        return code_str.strip()


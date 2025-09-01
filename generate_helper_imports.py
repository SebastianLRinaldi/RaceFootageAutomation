import os
import ast

HELPERS_DIR = os.path.join("src", "helper_functions")
# HELPERS_DIR = os.path.join("src", "helper_classes")
INIT_FILE = os.path.join(HELPERS_DIR, "__init__.py")

def get_exported_names(file_path):
    """Parse file and get all top-level class and function names."""
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
    return [
        node.name for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and not node.name.startswith("_")
    ]

lines = []
all_exports = []

for filename in sorted(os.listdir(HELPERS_DIR)):
    if not filename.endswith(".py") or filename.startswith("__"):
        continue

    module_name = filename[:-3]
    file_path = os.path.join(HELPERS_DIR, filename)
    exported = get_exported_names(file_path)

    if exported:
        line = f"from .{module_name} import " + ", ".join(exported)
        lines.append(line)
        all_exports.extend(exported)

# Add __all__ declaration for wildcard imports
lines.append("")
lines.append(f"__all__ = [{', '.join(f'\"{name}\"' for name in all_exports)}]")

# Write to __init__.py
with open(INIT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ Wrote helpers to {INIT_FILE}")

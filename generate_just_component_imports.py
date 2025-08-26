import os

APPS_DIR = os.path.join("src", "components")
# APPS_DIR = os.path.join("src", "features")
# APPS_DIR = os.path.join("src", "modules")
# APPS_DIR = os.path.join("src", "apps")

INIT_FILE = os.path.join(APPS_DIR, "__init__.py")

def to_pascal_case(s):
    return ''.join(word.capitalize() for word in s.split('_'))

lines = []

for app_name in sorted(os.listdir(APPS_DIR)):
    app_path = os.path.join(APPS_DIR, app_name)
    if not os.path.isdir(app_path) or app_name.startswith("__"):
        continue

    alias = to_pascal_case(app_name)
    line = f"from .{app_name} import Component as {alias}"
    lines.append(line)

with open(INIT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ Wrote imports to {INIT_FILE}")

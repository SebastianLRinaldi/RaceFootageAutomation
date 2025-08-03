import os

BASE_DIRS = [
    # os.path.join("src", "apps"),
    os.path.join("src", "components"),
]

IMPORTABLES = ["layout", "logic", "connections"]

def to_pascal_case(s):
    return ''.join(word.capitalize() for word in s.split('_'))

for base_dir in BASE_DIRS:
    init_file = os.path.join(base_dir, "__init__.py")
    lines = []

    if not os.path.exists(base_dir):
        print(f"⚠️ Directory not found: {base_dir}")
        continue

    for widget_name in sorted(os.listdir(base_dir)):
        widget_path = os.path.join(base_dir, widget_name)
        if not os.path.isdir(widget_path) or widget_name.startswith("__"):
            continue

        for part in IMPORTABLES:
            file_path = os.path.join(widget_path, f"{part}.py")
            if os.path.exists(file_path):
                class_name = part.capitalize()
                alias = f"{to_pascal_case(widget_name)}{class_name}"
                line = f"from .{widget_name}.{part} import {class_name} as {alias}"
                lines.append(line)
        lines.append("")  # blank line after each widget block

    with open(init_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Wrote imports to {init_file}")

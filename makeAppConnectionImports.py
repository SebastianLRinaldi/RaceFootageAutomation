import os

def generate_imports_and_vars():
    base_path = "src.apps"
    
    """
    if you have this function in another folder
    # Go up one folder, then into src/apps
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "apps"))
    if you have it in root
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "src", "apps"))
    """
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "src", "apps"))

    print(f"Using app_dir: {app_dir}\n")  # debug
    
    logic_imports = []
    layout_imports = []
    logic_vars = []
    layout_vars = []

    for name in os.listdir(app_dir):
        app_path = os.path.join(app_dir, name)
        if not os.path.isdir(app_path):
            continue
        if name.startswith("__") or name.lower() == "widgets":
            continue
        
        # Capitalize first letter for variable naming convention
        cap_name = name.capitalize()
        var_name = name.lower()

        logic_imports.append(f"from {base_path}.{name}.Functions import Logic as {cap_name}Logic")
        layout_imports.append(f"from {base_path}.{name}.Layout import Layout as {cap_name}Layout")

        logic_vars.append(f"    {var_name}_logic: {cap_name}Logic")
        layout_vars.append(f"    {var_name}_ui: {cap_name}Layout")

    # Print results
    print("\n".join(logic_imports))
    print()
    print("\n".join(layout_imports))
    print()
    print("\n".join(logic_vars))
    print()
    print("\n".join(layout_vars))


if __name__ == "__main__":
    generate_imports_and_vars()

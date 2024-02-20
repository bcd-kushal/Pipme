import os
import sys
import ast

def extract_imports(file_path:str):
    if file_path=="":
        return 

    with open(file_path,'r',encoding='utf-8') as file:
        tree = ast.parse(file.read(),file_path)

    user_imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                user_imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            user_imports.add(node.module)
    
    return user_imports



def get_user_installed_packages(root_path:str=os.getcwd()):
    packages_used = set()
    system_native_packages = set(sys.builtin_module_names)

    for folder_path, _, files in os.walk(root_path):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(folder_path,file_name)
                user_imports = extract_imports(file_path=file_path)
                packages_used.update(user_imports)

    imported_packages = packages_used - system_native_packages
    
    return imported_packages
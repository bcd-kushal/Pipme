import os
import re
import shutil
import requests
import subprocess 

""" 
    # valid package name = valid_user_package_name
    # valid package version = ask_user_version
    # parent_dir = parent_dir
    # packages installed = packages_installed
    # package folder is created with setup.py and markdown.md files in it
"""


# beautifish imports ++++++++++++++++++++++++++++++++++++++
import beautifish.templates as bft
import beautifish.colors as bfc
import beautifish.decorators as bfd
# file imports ++++++++++++++++++++++++++++++++++++++
from pipme.check_inits import *
from pipme.get_installed_packages import get_user_installed_packages
# +++++++++++++++++++++++++++++++++++++++++++++++++++

command = { 
    "bdist_wheel":"python setup.py sdist bdist_wheel", 
    "twine_upload":"twine upload --repository-url https://upload.pypi.org/legacy/ -u __token__ -p <access_token> dist/*" 
}

# ————————————————————————————————————————————————————————————————————————————————————————
# UTIL FUNCTIONS —————————————————————————————————————————————————————————————————————————

def is_valid_version(input_string):
    pattern = r'^\d+(\.\d+){2}$'
    return re.match(pattern, input_string) is not None


def convert_to_valid_package_name(name):
    # Replace non-ASCII letters, digits, underscores, and hyphens with underscores
    valid_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    # Ensure the name starts and ends with an ASCII letter or digit
    valid_name = re.sub(r'^[^a-zA-Z0-9]*|[^a-zA-Z0-9]*$', '', valid_name)
    # Convert the name to lowercase
    valid_name = valid_name.lower()
    return valid_name


def create_package_and_setup(parent_dir,package_name:str):
    SETUPPY_FILE_CODE = """\
from setuptools import setup, find_packages

setup(
    name='',
    version='',
    packages=find_packages(),
    install_requires=[]
)
    """
    package_folder = os.path.join(parent_dir, package_name)
    os.makedirs(package_folder,exist_ok=True)

    # create setup.py file in new folder 
    setupPy_file_path = os.path.join(package_folder,"setup.py")
    with open(setupPy_file_path,"w") as f:
        f.write(SETUPPY_FILE_CODE)


    # create readme.md
    readmeMD_file_path = os.path.join(package_folder,"readme.md")
    with open(readmeMD_file_path,"w") as f:
        pass
    


def check_package_exists_in_pypi(package_name:str):
    PYPI_API_ENDPOINT = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(PYPI_API_ENDPOINT)
    if response.status_code==200:
        return False
    elif response.status_code==404:
        return True
    else:
        print("Unexpected status code while reaching out to PyPI API:",response.status_code)
        return None


def migrate_files(source_path,destination_path):
    try:
        shutil.copytree(source_path, destination_path)
        print(f"Files migrated to new folder...")
    except FileExistsError:
        print(f"Destination directory {destination_path} already exists")


def modify_setup_file(setup_file_path,package_name:str,version:str,packages_to_install:list):
    # reading setup.py contents
    with open(setup_file_path,'r') as file:
        setup_contents = file.readlines()
    
    # updating name and version attributes
    modifications = []
    for line in setup_contents:
        if line.strip().startswith('name='):
            modifications.append(f"    name='{package_name}',\n")
        elif line.strip().startswith('version='):
            modifications.append(f"    version='{version}',\n") 
        elif line.strip().startswith('install_requires='):
            arr = ""
            for package in packages_to_install:
                arr += f"'{package}',"
            arr = arr[:len(arr)-1]
            modifications.append(f"    install_requires=[{arr}],\n") 
        else:
            modifications.append(line)

    # write into the setup.py with modifications
    with open(setup_file_path,'w') as file:
        file.writelines(modifications)


def change_relative_imports(root_folder, old_package_name, new_package_name):
    for folder_path, _, files in os.walk(root_folder):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as f:
                    content = f.read()
                # Use regular expression to find and replace relative imports
                new_content = re.sub(
                    fr'from\s+{old_package_name}(\s+|\.)',
                    fr'from {new_package_name}\g<1>',
                    content
                )
                # Write the modified content back to the file
                with open(file_path, 'w') as f:
                    f.write(new_content)


def rename_folder(old_folder_path,new_folder_name):
    # Get the parent directory of the folder
    parent_directory = os.path.dirname(old_folder_path)
    # Create the new folder path
    new_folder_path = os.path.join(parent_directory, new_folder_name)
    # Rename the folder
    os.rename(old_folder_path, new_folder_path)
    print(f"Folder '{old_folder_path}' renamed to '{new_folder_name}'")

# —————————————————————————————————————————————————————————————————————————————————————————
# —————————————————————————————————————————————————————————————————————————————————————————


# ——— MAIN FUNCTION ———————————————————————————————————————————————————————————————————————
# —————————————————————————————————————————————————————————————————————————————————————————
def run_cli(shell_path:str=os.getcwd()):
    """ 
    this function runs when user runs "pipme" in the shell 
    """

    bft.banner(msg="pipme",color="blue")

    # ask confirmation if this is the root folder where they want to pip ------------------------------------------
    print(f"Using {bfc.blue_text(shell_path)} as root directory.")
    ask_user = bft.input(f"Continue? (y/N): ",color="blue")
    if ask_user=="" or ask_user.lower().split()=='n':
        return 


    # ask if they registered at pypi.org and have an access token ready or not ------------------------------------
    ask_user = input(f"Are you registered at {bfc.blue_text("https://pypi.org/")} and have an {bfc.blue_text("access token")} (y/N): ")
    if ask_user=='' or ask_user.lower().split()=='n':
        return 
    

    # create __init__.py files to each subfolder ------------------------------------------------------------------
    # this creates __init_.py files inside all subfolders if it doesnt already exist
    bft.seperator2(header="Scanning for __init__.py files")
    check_all_folders_got_init(shell_path)


    # get all packages imported into the folder -------------------------------------------------------------------
    dummy = set()
    packages_installed = get_user_installed_packages(shell_path)
    for s in packages_installed:
        dummy.add(s.split('.')[0] if '.' in s else s)
    packages_installed = list(dummy)
    bft.success(msg=" ",title="Found packages used in project")
    bft.list(packages_installed)
    # this will go into the requirements array-------->>


    # get parent dir path -----------------------------------------------------------------------------------------
    parent_dir = os.path.dirname(shell_path)
    user_package_name = os.path.basename(shell_path)
    valid_user_package_name = convert_to_valid_package_name(user_package_name)

    # check if this name already exists and owned by someone in pypi ----------------------------------------------
    check_pip_existence = check_package_exists_in_pypi(valid_user_package_name)
    if(check_pip_existence==False or check_pip_existence==None):
        flag = True  
        while flag:
            is_owner = input(f"Your package name '{valid_user_package_name}' already is owned by someone. If its owned by you, type 'yes': ")
            if(is_owner.lower()=="yes"):
                flag = False
                break
            new_input = input("Enter a different package name you wish to use: ")
            new_input = convert_to_valid_package_name(new_input)
            print(f"Reformatted to: {new_input}...")
            valid_user_package_name = new_input
            if(check_package_exists_in_pypi(new_input)==True):
                flag=False
                valid_user_package_name = new_input

    print(f"{bfi.DOT} Package name used: {bfc.cyan_text(valid_user_package_name)}")
    


    # ask user for the version they wish to make it ----------------------------------------------------------------
    ask_user_version = input(f"What's the version you wish to give {bfc.gray_text("(default 1.0.0)")}: ")
    # check user input to version's authneticity
    if ask_user_version=="":
        ask_user_version = "1.0.0"
    while not is_valid_version(ask_user_version):
        bft.error("Unauthentic version syntax, must be of type num.num.num",mode="spaced")
        ask_user_version = input(f"What's the version you wish to give {bfc.gray_text("(default 1.0.0)")}: ")
        if ask_user_version=="":
            ask_user_version = "1.0.0"
    

    # create package folder and setup.py in it ----------------------------------------------------------------------
    print(f"Creating package in parent dir and adding setup.py file to it")
    create_package_and_setup(parent_dir=parent_dir,package_name=f"{valid_user_package_name}_package")


    # copy shell_path to new folder ---------------------------------------------------------------------------------
    package_path = os.path.join(parent_dir, f"{valid_user_package_name}_package")


    # migrate files to package_path ---------------------------------------------------------------------------------
    print(f"Migrating files from {bfc.gray_text(shell_path)} to {bfc.orange_text(package_path)}")
    migrate_files(shell_path,os.path.join(package_path,valid_user_package_name))
    

    # modify setup files to contain name and version number ---------------------------------------------------------
    print(f"Adding name and version to setup.py...")
    modify_setup_file(setup_file_path=os.path.join(package_path,"setup.py"),package_name=valid_user_package_name,version=ask_user_version,packages_to_install=packages_installed)


    # change relative imports ---------------------------------------------------------------------------------------
    if os.path.basename(shell_path)!=valid_user_package_name:
        print(f"Changing relative imports from {os.path.basename(shell_path)} to {valid_user_package_name}")
        change_relative_imports(os.path.join(package_path,valid_user_package_name),os.path.basename(shell_path),valid_user_package_name)


    # cross-check __init__.py files exist in new cleaned folder directory or not ------------------------------------
    check_all_folders_got_init(os.path.join(package_path,valid_user_package_name))    
    

    # migrate to package directory in shell -------------------------------------------------------------------------
    os.chdir(package_path)
    print("Migrated shell path to:",bfc.orange_text(os.getcwd()))


    # run command to create distwheel -------------------------------------------------------------------------------
    """ the idea is when package will be installed, twine would also be installed already
        as such, its safe to assume twine isnt required as another installation dependency """
    print(bfc.gray_text("Running command to create distwheel..."))
    distwheel_status = subprocess.run(command["bdist_wheel"],shell=True,capture_output=True,text=True)
    print(distwheel_status.stdout)


    # run command to upload using twine -----------------------------------------------------------------------------
    # get access token
    access_token = bft.input("Enter the access token: ",color="blue")
    if len(access_token)<150:
        bft.error("The access token entered seems too short to be precise")
        return
    # run pip upload command
    print(bfc.cyan_text("Running command to upload to pip using twine and access token provided..."))
    upload_command = command["twine_upload"].replace("<access_token>",access_token)
    twine_upload_status = subprocess.run(upload_command,shell=True,capture_output=True,text=True)
    print(twine_upload_status.stdout)

    print(bfc.orange_text("[^^] Thanks for using pipme\n\n - by kushal kumar (dev@kushalkumarsaha.com)\n - www.portfolio.kushalkumarsaha.com\n\n"))




if __name__=="__main__":
    current_shell_path = os.getcwd()
    run_cli(current_shell_path)
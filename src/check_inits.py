import os 
import beautifish.icons as bfi
import beautifish.colors as bfc 

def check_all_folders_got_init(root_path:str=os.getcwd()):
    # traverse through all subfolders under this root path given
    for folder_path, _, _ in os.walk(root_path):
        init_file = os.path.join(folder_path,"__init__.py")

        # create __init__.py if it doesnt exist
        if not os.path.exists(init_file):
            print(f"Creating __init__.py file at: {folder_path}")
            with open(init_file,"w") as f:
                pass        # to create an empty __init__.py in this directory
        else:
            print(f"{bfc.cyan_text(bfi.DOT)} FOUND __init__.py file at {folder_path}")

    return


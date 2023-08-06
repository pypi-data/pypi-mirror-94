from vizcode.graph import Graph
from vizcode.command_line import Command_Line
from vizcode.constants import *
import vizcode.parsing as parsing
import vizcode.helpers as helpers
import os
import glob
import time
import pathlib

CURRENT_DIR_PATH = str(pathlib.Path(__file__).parent.absolute()) + "/"

def main(parsed_files):

    graph = Graph("Newspark Python Example")

    graph.populate_graph(parsed_files)
    print("Built the graph.")

    graph.save_graph()
    print("Saved the graph.")

    print("Starting frontend application...\n")
    graph.start_frontend()

    return None

def start():

    args = Command_Line()

    # Parse the arguments from the Command Line
    path = args.get_path()
    env_path = args.get_env()
    deselect_paths = args.get_deselect()

    # Checks to make sure the paths for the source code,
    # environment, test path are valid
    exists = True
    if not os.path.exists(path):
        print ("Path does not exist.")
        exists = False

    if exists:
        if env_path and not os.path.exists(env_path):
            print ("Not a valid environment path, \
                will default to global environment")
            env_path = None
        
        valid_deselect_paths = []
        for subpath in deselect_paths:
            if not os.path.exists(subpath) and not os.path.isfile(subpath):
                print (subpath + ": invalid object to deselect for visualization, will remove")
            else:
                valid_deselect_paths.append(subpath)

        helpers.remove_old_code()

        parsed_files = None
        if os.path.isdir(path):
            parsed_files = parsing.start_dir_parser((path, env_path, valid_deselect_paths))

        elif '.py' in path:
            parsed_files = parsing.start_file_parser((path, env_path, valid_deselect_paths))

        if parsed_files:
            main(parsed_files)
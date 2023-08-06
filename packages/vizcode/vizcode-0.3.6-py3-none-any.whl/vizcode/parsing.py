from vizcode.constants import *
import hashlib
import vizcode.indexer as indexer
import vizcode.helpers as helpers
import multiprocessing
import os

NUM_PROCESSES = multiprocessing.cpu_count()

class Parsed_File:
    def __init__(self, file_path, client):
        self.client = client
        self.file_path = file_path

# Returns a parsed file.
def parse_file(args):
    file_path, env_path = args

    print ("Parsing file " + file_path)

    with open(file_path, 'r') as f:
        code = f.read()

    save_code_to_file(file_path, code)
    client = indexer.start_indexer(file_path, code, env_path, [])

    return Parsed_File(file_path, client)

def save_code_to_file(file_path, code):
    """
    Saves code to a file in the frontend directory.
    """
    hashed_name = hashlib.sha256(file_path.encode('utf-8')).hexdigest()[:16]
    new_file_path = CURRENT_DIR_PATH + PUBLIC_PATH + FILE_CODE_PATH + hashed_name + ".txt"
    with open(new_file_path, 'w+') as output_file:
        output_file.write(code)

    return

def start_dir_parser(args):
    """
    start_dir_parser utilizes multiprocessing to start
    processing through all python files in a directory.
    """
    path, env_path, deselect_paths = args

    files = helpers.get_files(path, env_path, deselect_paths)
    print(f"Parsing {len(files)} files...")
    pool = multiprocessing.Pool(NUM_PROCESSES)
    parsed_files = pool.map(parse_file, \
        [(file_path, env_path) for file_path in files])

    return parsed_files

def start_file_parser(args):
    """
    start_file_parser utilizes multiprocessing to start
    processing a python file and any python files 
    that can be reached from that file in a path of references. 
    """
    path, env_path, deselect_paths = args

    deslect_files = helpers.get_deselect_files(deselect_paths)

    if path in deslect_files:
        return []

    manager = multiprocessing.Manager()
    seen_files = set()
    seen_files.add(path)
    files = [path]

    parsed_files = manager.list()
    while len(files) != 0:
        jobs_queue = multiprocessing.Queue()
        new_files = manager.dict()
        pool = multiprocessing.Pool(NUM_PROCESSES, worker, \
            (jobs_queue, parsed_files, new_files, env_path))

        for f in files:
            jobs_queue.put(f)

        for i in range(NUM_PROCESSES):
            jobs_queue.put(None)

        # Prevent adding anything more to the queue
        # and wait for queue to empty
        jobs_queue.close()
        jobs_queue.join_thread()

        # Prevent adding anything more to the process pool
        # and wait for all processes to finish
        pool.close()
        pool.join()

        files = []
        for f in new_files.keys():
            if f not in seen_files and f not in deslect_files:
                seen_files.add(f)
                files.append(f)
    
    return parsed_files

def worker(jobs_queue, parsed_files, new_files, env_path):
    """
    worker represents a process in the multiprocessing pool
    of start_file_parser.
    """
    while True:

        # Wait for items in the queue
        file_path = jobs_queue.get(block=True)
        if file_path is None:
            break

        parsed_file = parse_file((file_path, env_path))
        parsed_files.append(parsed_file)

        folder_path = os.path.dirname(file_path)
        refs = helpers.get_file_references(folder_path, \
            parsed_file.client.symbols)

        for ref in refs:
            new_files[ref] = None

    return 

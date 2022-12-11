import os
import hashlib
from tqdm import tqdm

def check_hash(file_name):
    global directory, files_hash
    # directory = os.getcwd()
    files_hash = []
    try:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash in files_hash:
                print('Duplicate file: ', file_name, files_hash)
                os.remove(file_path)
                with open('Removed.txt', 'a') as f:
                    f.write(file_name + ':' + files_hash + '\n')
                print('Removed: ', file_name, files_hash)
            else:
                files_hash.append(file_hash)
    except Exception as e:
        print(e, file_name)
        pass

def main():
    global directory
    # change your directory before running
    directory = 'G:\\Books'
    for file in tqdm(os.listdir(directory)):
        if file.endswith('.pdf'):
            check_hash(file)
    print('Done!')

if __name__ == '__main__':
    main()

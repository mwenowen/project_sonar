import os
import hashlib
from tqdm import tqdm
from datetime import datetime

directory = 'F:\\python\\python3'


file_hash = {}

def time_stamp():
    current_time = datetime.now().strftime('%H:%M:%S')
    return current_time

for file_name in tqdm(os.listdir(directory)):
    if file_name.endswith('.pdf'):
        file_path = os.path.join(directory, file_name)

        with open(file_path, 'rb') as f:
            data = f.read()

        md5 = hashlib.md5(data).hexdigest()

        if md5 in file_hash:
            os.remove(file_path)
            print('\r' + 'Removed: {}'.format(file_name) + ' ' + md5 + '\n')
            try:
                with open('Removed.txt', 'w') as f_romved:
                    f_romved.write(file_name + '\n')
            except:
                pass
        else:
            file_hash[md5] = file_path

print('Done!')

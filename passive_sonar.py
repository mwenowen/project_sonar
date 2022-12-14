import os
import json
from utils import *
from tqdm import tqdm
from urllib.parse import unquote
from threading import Thread
from my_str import *

ERROR = ' \033[1;31m[Error]\033[0m '
INFO = ' \033[1;32m[Info]\033[0m '
WARN = ' \033[1;33m[Warning]\033[0m '


def thread_task(target, args):
    global threads
    threads = []
    t = Thread(target=target, args=(args,))
    threads.append(t)
    t.start()
    for thread in threads:
        thread.join()


def print_menu():
    print('''
        1. Check urls status code
        2. Download files
        3. Read pdf meta data
        4. Check file hash
        99. Exit
        ''')


def get_input(msg) -> str:
    return input(msg)


def get_choice():
    print_menu()
    return get_input(CHOICE_PROMPT)


def handle_domain():
    domain = get_input(DOMAIN_PROMPT)
    urls = fetch_urls(domain)
    for _ in tqdm(urls):
        url = ''.join(_)
        thread_task(check_status_code, url)
        # check_status_code(url)


def main():
    while True:
        choice = get_choice()
        if choice == '1':
            handle_domain()
        elif choice == '2':
            domain = input("Enter domain: ")
            extention = input("Enter file extention: ")
            urls = fetch_urls(domain)
            f_list = open('{}_file_list.txt'.format(domain), 'w')
            i = 1
            for _ in tqdm(urls):
                url = ''.join(_)
                if url.endswith(extention):
                    # url decode twice in case of two times url encoding
                    file_name = unquote(unquote(url.split('/')[-1]))
                    thread_task(download_file, url)
                    # download_file(url)
                    try:
                        f_list.write('[{}]'.format(i) +
                                     file_name + ' ' + url + '\n')
                    except Exception as e:
                        print(e, url)
                        pass
                    i += 1
            f_list.close()
            print('\r\n' + DOWNLOAD_SUCCEED_MSG)
            print('\r\n' + '[Files count: {}]'.format(i-1))
        elif choice == '3':
            directory = os.getcwd()
            for file_name in tqdm(os.listdir(directory)):
                file_path = os.path.join(directory, file_name)
                if file_name.endswith('.pdf'):
                    read_pdf_meta(file_path)
        elif choice == '4':
            directory = os.getcwd()
            for file_name in tqdm(os.listdir(directory)):
                file_path = os.path.join(directory, file_name)
                check_hash(file_path)
        # TODO: add more functions
        elif choice == '99':
            print(INFO + 'Bye!')
            break
        elif choice == '000':
            print(time_stamp(), INFO + 'Debug mode')
            print(time_stamp(), WARN + 'Debug mode')
            print(time_stamp(), ERROR + 'Debug mode')
        else:
            print(ERROR + 'Invalid choice')


if __name__ == "__main__":
    main()

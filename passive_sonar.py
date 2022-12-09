from tqdm import tqdm
from datetime import datetime
import json
import time
import threading
import requests
import urllib.request
import urllib.parse

ERROR = ' \033[1;31m[Error]\033[0m '
INFO = ' \033[1;32m[Info]\033[0m '
WARN = ' \033[1;33m[Warning]\033[0m '
DONE = ' \033[1;32m[Done]\033[0m '


# fetching urls from wayback machine, input is domain
def get_urls(domain):
    url = 'https://web.archive.org/cdx/search/cdx?url=*.' + domain + '/*&output=json&fl=original&collapse=urlkey'
    r = requests.get(url)
    urls = json.loads(r.text)
    return urls

def time_stamp():
    crrent_time = datetime.now().strftime('%H:%M:%S')
    return crrent_time

def hash_check():
    pass

def downloader(url, file_name):
    try:
        urllib.request.urlretrieve(url, file_name)
    except:
        pass

# main function
def main():
    # print(INFO, WARN, ERROR)
    domain = input(time_stamp() + INFO + 'Enter domain name: ')
    extention = input(time_stamp() + INFO + 'Enter file extention: ')
    f_list = open('{}_pdf_list.txt'.format(domain), 'w')
    f_name = open('{}_pdf_name.txt'.format(domain), 'w')
    urls = get_urls(domain)
    i = 1
    for _ in tqdm(urls):
        url = ''.join(_)
        if url.endswith(extention):
            file_name = urllib.parse.unquote(url.split('/')[-1])
            downloader(url, file_name)
            time.sleep(1)
            print('\r\n' + time_stamp() + ' ' + INFO + ' ' + file_name + ' [Downloaded!] ')
            try:
                f_list.write(url + '\n')
                f_name.write('[{}]'.format(i) + ' ' + file_name + '\n')
            except Exception as e:
                print(ERROR, e)
                pass

            i += 1
    f_list.close()
    f_name.close()
    print('\r\n' + time_stamp() + ' ' + DONE + ' ' + '[All files downloaded!]')
    print('\r\n' + time_stamp() + ' ' + INFO + ' ' + '[Files count: {}]'.format(i-1))

if __name__ == '__main__':
    main()


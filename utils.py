import os
import json
import hashlib
import requests
import PyPDF2
import urllib.request
from datetime import datetime
from urllib.parse import unquote


# generate time stamp
def time_stamp():
    current_time = datetime.now().strftime("%H:%M:%S")
    return '[' + current_time + ']'

# fetch all urls from wayback machine for a given domain, return a list of urls
def fetch_urls(domain):
    try:
        url = "http://web.archive.org/cdx/search/cdx?url=*.{}/*&output=json&fl=original&collapse=urlkey".format(domain)
        response = requests.get(url)
        urls = json.loads(response.text)
        return urls[1:]
    except Exception as e:
        print(e)
        pass

# check status code of a given url
def check_status_code(url):
    try:
        response = requests.head(url)
        status_code = response.status_code
        if status_code == 200:
            print('[200] '  + url)
    except Exception as e:
        print(e, url)
        pass

# download file from a given url
def download_file(url):
    # url decode twice in case of two times url encoding
    file_name = unquote(unquote(url.split('/')[-1]))
    try:
        with open(file_name, 'wb') as f:
            response = requests.get(url)
            f.write(response.content)
            print('Downloaded: ' + file_name)
    except Exception as e:
        print(e, url)
        pass

# check file hash, and remove duplicate files
def check_hash(file_name):
    global files_hash
    files_hash = []
    try:
        with open(file_name, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
            if md5 in files_hash:
                os.remove(file_name)
                print('Removed: ' + file_name + ':' + md5)
            else:
                files_hash.append(md5)
            # print(md5)
    except Exception as e:
        print(e, file_name)

# read pdf meta data
def read_pdf_meta(pdf_file):
    try:
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            meta_data = reader.getDocumentInfo()
            # print(meta_data['/Title'])
            for key, value in meta_data.items():
                print(key + ':' + value)
    except Exception as e:
        print(e, pdf_file)
        pass
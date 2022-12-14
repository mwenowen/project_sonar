import requests
import json


class SqlmapUtils:

    def __init__(self, target, host="127.0.0.7", port=8775):
        self.target = target
        self.host = host
        self.port = port
        self.port = str(self.port)
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}

        self.urlnew = "http://" + self.host + ":" + self.port + "/task/new"
        self.urlscan = "http://" + self.host + ":" + self.port + "/scan/"

        self.id = None

    def init_new(self):
        res = requests.get(self.urlnew, self.header)
        print("=" * 5 + "[New Task]" + "=" * 5)
        jsons = res.json()
        self.id = jsons["taskid"]
        self.urlscan = self.urlscan + self.id + "/start"

    def start_scan(self):
        data = json.dumps({"url": "{}".format(self.target)})
        headers = {"Content-Type": "application/json"}
        scan = requests.post(self.urlscan, data=data, headers=headers)

        res = scan.json()
        print("=" * 5 + "[Scan]" + "=" * 5)
        print("Scan ID: {}".format(res["engineid"]))
        print("Succeed: {}".format(res["success"]))

    def get_status(self):
        urlstatus = "http://" + self.host + ":" + self.port + "/scan/{}/status".format(self.id)
        while True:
            res = requests.get(urlstatus, self.header)
            if res.json()["status"] == "terminated":
                urldata = "http://" + self.host + ":" + self.port + "/scan/{}/data".format(self.id)
                data = requests.get(urldata).json()["data"]
                print("Data: ", data)
                break


# Usage
# sql = SqlmapUtils(<target url>)
# sql.init_new()
# sql.start_scan()
# sql.get_status()

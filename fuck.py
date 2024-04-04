import execjs  
import requests

class RouterControl:
    def __init__(self, host, password):
        self.host = host
        self.password = password
        self.base = f'http://{self.host}'
        self.js = self.get_js()
        self.token = None

    def get_js(self): 
        with open("fuck.js", 'r', encoding='UTF-8') as f:
            js = f.read()
            return execjs.compile(js)

    def get_pwd(self):
        return self.js.call('loginHandle', self.password)

    def login(self):
        url = f"{self.base}/cgi-bin/luci/api/xqsystem/login"
        pwd = self.get_pwd()

        headers = {
            "Host": self.host,
            "Accept": "*/*",
            "DNT": "1",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.base,
            "Referer": f"{self.base}/cgi-bin/luci/web",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "sec-gpc": "1"
        }

        data = {
            "username": 'admin',
            "password": pwd[0],
            "logtype": "2",
            "nonce": pwd[1]
        }

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            result_json = response.json()
            self.token = result_json.get("token", "")
            return True
        else:
            return False

    def reboot(self):
        if not self.token:
            return "Token not available. Please login first."

        url_index = f"{self.base}/cgi-bin/luci/;stok={self.token}"
        url_reboot = f"{url_index}/api/xqsystem/reboot?client=web"

        self.api(url_reboot)

    def wifi_detail(self):
        if not self.token:
            return "Token not available. Please login first."

        url_index = f"{self.base}/cgi-bin/luci/;stok={self.token}"
        url_detail = f"{url_index}/api/xqnetwork/wifi_detail_all"

        self.api(url_detail)

    def api(self, url):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-gpc': '1'
        }

        response = requests.get(url, headers=headers, verify=False) 
        print(response.text)


router = RouterControl('192.168.0.1', 'pwd')

if router.login():
    router.wifi_detail()
else:
    print("Login failed.")

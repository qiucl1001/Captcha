# coding:utf-8
import os
import http.client, mimetypes, urllib, json, time, requests
from captcha.settings import USERNAME, PASSWORD, APPID, APPKEY, CODETYPE, TIMEOUT


class YDMHttp(object):
    """
    借用三方云打码平台技术栈(验证码平台captcha-platform)
    dst_url：http://www.yundama.com/
    """

    def __init__(self, username='', password='', appid=None, appkey=''):
        """
        初始化
        :param username: 用户名
        :param password: 密码
        :param appid: 软件ＩＤ，开发者分成必要参数
        :param appkey: 软件密钥，开发者分成必要参数
        """
        self.apiurl = 'http://api.yundama.com/api.php'
        self.username = username
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    def request(self, fields, files=[]):
        response = self.post_url(self.apiurl, fields, files)
        response = json.loads(response)
        return response
    
    def balance(self):
        data = {'method': 'balance',
                'username': self.username,
                'password': self.password,
                'appid': self.appid,
                'appkey': self.appkey
                }
        response = self.request(data)
        if response:
            if response['ret'] and response['ret'] < 0:
                return response['ret']
            else:
                return response['balance']
        else:
            return -9001
    
    def login(self):
        data = {'method': 'login',
                'username': self.username,
                'password': self.password,
                'appid': self.appid,
                'appkey': self.appkey
                }
        response = self.request(data)
        if response:
            if response['ret'] and response['ret'] < 0:
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001

    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload',
                'username': self.username,
                'password': self.password,
                'appid': self.appid,
                'appkey': self.appkey,
                'codetype': str(codetype),
                'timeout': str(timeout)
                }
        file = {'file': filename}
        response = self.request(data, file)
        if response:
            if response['ret'] and response['ret'] < 0:
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result',
                'username': self.username,
                'password': self.password,
                'appid': self.appid,
                'appkey': self.appkey,
                'cid': str(cid)
                }
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, filename, codetype, timeout):
        cid = self.upload(filename, codetype, timeout)
        if cid > 0:
            for i in range(0, timeout):
                result = self.result(cid)
                if result != '':
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

    def report(self, cid):
        data = {'method': 'report',
                'username': self.username,
                'password': self.password,
                'appid': self.appid,
                'appkey': self.appkey,
                'cid': str(cid),
                'flag': '0'
                }
        response = self.request(data)
        if response:
            return response['ret']
        else:
            return -9001

    @staticmethod
    def post_url(url, fields, files=[]):
        # for key in files:
        #     files[key] = open(files[key], 'rb');
        res = requests.post(url, files=files, data=fields)
        return res.text


def identify(content):
    # 图片文件
    filename = content
    # 检查
    if USERNAME == 'username':
        print('请设置好相关参数再测试')
    else:
        # 初始化
        yundama = YDMHttp(USERNAME, PASSWORD, APPID, APPKEY)

        # 登陆云打码
        uid = yundama.login()
        print('uid: %s' % uid)

        # 查询余额
        balance = yundama.balance()
        print('balance: %s' % balance)

        # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
        cid, result = yundama.decode(filename, CODETYPE, TIMEOUT)
        print('cid: %s, result: %s' % (cid, result))
        return result


if __name__ == '__main__':
    # yundama = YDMHttp("yixiao", "qcl123456", 5744, "59064192fc649008a000568bb1daccc5")
    #
    # # 登陆云打码
    # uid = yundama.login();
    # print('uid: %s' % uid)
    #
    # # 查询余额
    # balance = yundama.balance();
    # print('balance: %s' % balance)
    #
    # # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
    # cid, result = yundama.decode("./getimage.jpg", 3004, 60);
    # print('cid: %s, result: %s' % (cid, result))

    url = "http://qian.sicent.com/Login/code.do"
    content = requests.get(url).content
    with open("test.png", "wb") as f:
        f.write(content)

    # image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images/words_captcha.png')
    # # 读取图片二进制数据
    # with open(image_path, "rb") as f:
    #     content = f.read()
    # item = identify(content)
    # print(item)

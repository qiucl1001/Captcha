# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import time
# import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from captcha.libs.chaojiying import Chaojiying
from base64 import b64decode
import pytesseract


class ZhiHuLogin(object):
    """使用selenium网页端自动化测试套件模拟知乎登入页面"""

    def __init__(self):
        """初始化"""
        self.dst_url = "https://www.zhihu.com/signin"
        self.proxy_url = "http://127.0.0.1:5000/random"
        self.driver_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"  # chrome浏览器驱动路径
        # self.proxy = requests.get(self.proxy_url).text
        # print("Success Get IP Proxy ！", "proxy:", self.proxy)
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument("--headless")
        # self.chrome_options.add_argument("--proxy-server=http://" + self.proxy)
        self.browser = webdriver.Chrome(executable_path=self.driver_path, options=self.chrome_options)
        self.wait = WebDriverWait(self.browser, timeout=10)
        self.action_chains = ActionChains(self.browser)

        self.username = ""  # 登入用户名
        self.password = ""  # 登入密码
        self.retry_click_times = 3  # 重复点击登入按钮，触发点触验证码的出现
        
        # 初始化超级鹰连接对象
        # <传递三个参数，超级鹰打码平台的用户名，登入密码，验证码对应的类型编号：903344代表返回4-6个点触文字所在位置坐标>
        self.chaojiying = Chaojiying('', '', '903344')

    # def __del__(self):
    #     self.browser.close()

    def get_user_pass_btn_ele(self):
        """
        获取登入页面的用户名密码输入框以及登入按钮元素
        :return: 以列表的形式返回个元素
        """
        # 用户名所在标签元素对象
        user_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
        # 密码所在标签元素对象
        password_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
        # 登入按钮所在标签元素对象
        login_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "Button--blue")]'))
        )
        return [user_input, password_input, login_button]

    def run(self):
        """启动selenium网页端自动化测试工具套件"""
        # 向目标网页发送请求
        self.browser.get(url=self.dst_url)
        # try:
        #     self.browser.get(url='http://httpbin.org/get')
        #     time.sleep(1)
        #     response = self.browser.page_source  # 获取网页源代码
        #     print(response)
        # except TimeoutException:
        #     print("Request Httpbin.org Failed, Try Again")
        #     self.run()
        # except Exception as e:
        #     print(e.args)

        # 获取登入界面，选择登入方式，知乎默认为免密码登入(使用手机号短信验证码)
        # 这里我们使用selenium则选择使用密码登入的范式
        # 获取登入密码标签元素
        pass_login_element = None
        try:
            pass_login_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="SignFlow-tabs"]/div[2]'))
            )
        except TimeoutException:
            self.run()
        if pass_login_element:
            pass_login_element.click()
        # 获取登入页面的用户名密码输入框以及登入按钮元素
        elements_list = self.get_user_pass_btn_ele()
        # 输入用户名和密码
        elements_list[0].send_keys(self.username)
        elements_list[1].send_keys(self.password)
        time.sleep(1)
        # 点击登入按钮
        elements_list[2].click()

        # 获取验证码图片
        image = self.get_captcha_image()
        if isinstance(image, str):
            # 输入验证码
            captcha_input = self.browser.find_element_by_xpath('//div[@class="SignFlowInput"]')
            captcha_input.send_keys(str)
            time.sleep(0.5)
        else:
            bytes_array = BytesIO()
            image.save(bytes_array, format="PNG")
            # 调用三方技术栈辅助识别验证码
            result = self.chaojiying.post_pic(bytes_array.getvalue(), 9004)
            # 获取倒立验证码中的文字坐标
            locations = self.get_points(result)
            # 点击验证码
            self.touch_captcha_words(locations)
        # 点击登入按钮
        elements_list[2].click()
        # 退出浏览器
        time.sleep(2)
        self.browser.close()

    def touch_captcha_words(self, locations):
        """
        点击验证码图片中的文字
        :param locations: 文字坐标
        :return:
        """
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "Captcha-chinese")]/div[1]'))
            ), location[0], location[1]).click().perform()
            time.sleep(1)

    @staticmethod
    def get_points(result):
        """
        获取倒立验证码中的文字坐标
        :param result: 验证码识别结果
        e.g: {'err_no': 0,
              'err_str': 'OK',
              'pic_id': '3094720063783500001',
              'pic_str': '200,234|120,390|...',
              'md5': 'a38c860c5207ce034d5e47964c6f61b8'
            }
        :return: 倒立文字坐标：[[200, 234], [120, 390]...]
        """
        coordinates = result.split("|")
        locations = [[int(number) for number in coordinate.split(",")]for coordinate in coordinates]
        return locations

    def get_captcha_image(self, name="zhi_hu_captcha.jpg"):
        """
        获取验证码图片
        :param name: 验证码图片名称
        :return:
        """
        # 获取验证码在网页中的位置
        res = self.get_captcha_position()
        if isinstance(res, tuple):
            left, top, right, bottom = res
            screen_shot = self.get_screen_shot()
            captcha = screen_shot.crop((left, top, right, bottom))
            # 将图片保存到本地
            captcha.save(name)
            return captcha
        elif isinstance(res, str):
            return res

    def get_screen_shot(self):
        """
        获取网页截图
        :return: 返回截图图片对象: screen_shot
        """
        screen_shot = self.browser.get_screenshot_as_png()
        screen_shot = Image.open(BytesIO(screen_shot))
        # 将截屏图片保存到本地
        screen_shot.save("222.png")
        return screen_shot

    def get_captcha_position(self):
        """
        获取验证码图片位置
        :return: 返回图片位置元祖：(left, top, right, bottom)
        """
        # 获取验证码图片元素
        try:
            # 文字点选验证码识别
            image_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "Captcha-chinese")]/div[1]'))
            )
        except TimeoutException:
            # 字符验证码识别
            # 获取字符验证码
            return self.get_words_captcha()

        location = image_element.location
        size = image_element.size
        left = location['x'] + 85
        right = location['x'] + size['width'] + 85 + 85
        top = location['y'] + 60
        bottom = location['y'] + size['height'] + 60 + 23
        print({"size": size})
        print({"left": left, "top": top, "right": right, "bottom": bottom})

        return left, top, right, bottom

    def get_words_captcha(self):
        """
        获取字符图片验证码
        :return:
        """
        image_element = self.browser.find_element_by_xpath('//img[@class="Captcha-chineseImg"]')
        src_data = image_element.get_attribute('src').split(",")[1]
        image_bytes = b64decode(src_data)
        # 将字符验证码保存到本地
        with open("zh_words_captcha.png", 'wb') as f:
            f.write(image_bytes)
        # 将图片转化为字符
        image_str = pytesseract.image_to_string(image_bytes)
        return image_str


def main():
    """启动程序"""
    q = ZhiHuLogin()
    q.run()


if __name__ == '__main__':
    main()



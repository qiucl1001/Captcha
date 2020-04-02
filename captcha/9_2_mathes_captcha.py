# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import os
import io
import time
import base64
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pytesseract
from captcha.libs.ydm3 import identify


class MathCaptcha(object):
    """计算型验证码识别"""
    def __init__(self):
        """初始化"""
        self.url = "http://www.porters.vip/captcha/mathes.html"
        self.driver_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        self.browser = webdriver.Chrome(executable_path=self.driver_path)
        self.wait = WebDriverWait(self.browser, timeout=20)

    def __str__(self):
        self.browser.close()

    def run(self):
        # 发送网络请求
        self.browser.get(url=self.url)
        time.sleep(1)

    def get_screen_shot(self):
        """
        获取网页截图
        :return: 网页截图对象
        """
        # 获取网页截图对象
        screen_shot = self.browser.get_screenshot_as_png()
        screen_shot = Image.open(io.BytesIO(screen_shot))
        # screen_shot.show()
        return screen_shot

    def get_position(self):
        """
        获取验证码图片位置
        :return: 返回验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.ID, 'matchesCanvas')))
        time.sleep(2)
        # img.send_keys("qcl0306777@163.com")  #  {'x': 30, 'y': 456}
        location = img.location
        print(location)  # {'x': 421, 'y': 412} "???" canvas标签location位置定位不准确？！

        size = img.size
        print(size)  # {'height': 40, 'width': 200} "√"
        top = location['y']
        bottom = location['y'] + size['height']
        left = location['x']
        right = location['x'] + size['width']

        return top, bottom, left, right

    def get_math_captcha(self, name='captcha.png'):
        """
        获取计算型验证码图片
        :param name:验证码图片名称
        :return:图片对象
        """
        # 启动selenium套件
        self.run()
        screen_shot = self.get_screen_shot()
        top, bottom, left, right = self.get_position()
        print("验证码图片位置：", {'left': left, 'top': top, 'right': right, 'bottom': bottom})
        captcha = screen_shot.crop((left, top, right, bottom))
        print(type(captcha))
        print(captcha)
        captcha.show()

    def get_canvas_pic(self):
        """selenium利用js获取前端canvas画布标签的图片内容"""
        self.browser.get(self.url)
        time.sleep(1)
        # 下面的js代码根据canvas文档说明而来
        js = 'return document.getElementById("matchesCanvas").toDataURL("image/png");'
        # 执行js代码并拿到图片base64数据
        img_info = self.browser.execute_script(js)

        # 获取经过base64加密的图片信息
        img_base64 = img_info.split(",")[1]

        # 将base64加密的图片信息转化为图片字节流(bytes)
        img_bytes = base64.b64decode(img_base64)

        print(img_bytes)
        # 将图片保存到本地文件
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/math_captcha.png')
        if not os.path.exists(image_path):
            with open(image_path, 'wb') as f:
                f.write(img_bytes)

        print(img_base64)
        time.sleep(5)


def use_pytesseract():
    """使用pytesseract库识别图片"""
    # 保存在本地的图片路径
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/math_captcha.png')
    # print(pytesseract.image_to_string(image_path))  # 识别失败
    # 借用三方打码平台
    # with open(image_path, 'rb') as f:
    #     content = f.read()
    #     res = identify(content)
    #     print(res)
    # 将图片灰度处理
    grays = Image.open(image_path).convert("L")
    # grays.show()
    # print(pytesseract.image_to_string(grays))  # 图片进行灰度处理识别不了图片内容

    # # 将图片二值化处理
    threshold = 160
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    res = grays.point(table, '1')
    res.show()
    print(pytesseract.image_to_string(res))  # 90-18:? I 能识别 "√"


def main():
    """程序主入口"""
    m = MathCaptcha()
    # m.get_math_captcha('math_captcha.png')
    m.get_canvas_pic()


if __name__ == '__main__':
    # main()
    use_pytesseract()


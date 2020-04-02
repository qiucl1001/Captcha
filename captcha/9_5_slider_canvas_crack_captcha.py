# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import os
import time
import base64
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image
from PIL import ImageChops


class SliderCanvasCrackCaptcha(object):
    """基于canvas的普通滑块缺口验证码"""

    def __init__(self):
        """初始化"""
        self.url = "http://www.porters.vip/captcha/jigsawCanvas.html"
        self.driver_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        self.browser = webdriver.Chrome(executable_path=self.driver_path)
        self.wait = WebDriverWait(self.browser, timeout=20)
        self.action_chains = ActionChains(self.browser)

    def __del__(self):
        self.browser.close()

    def get_captcha_img(self, name='captcha.png'):
        """
        获取验证码图片
        :param name: 验证码图片名字
        :return:
        """
        # 获取canvas图片
        js = 'return document.getElementById("jigsawCanvas").toDataURL("image/png");'

        # 执行js代码并拿到图片base64数据
        img_info = self.browser.execute_script(js)

        # 获取经过base64加密的图片信息
        img_base64 = img_info.split(",")[1]

        # 将base64加密的图片信息转化为图片字节流(bytes)
        img_bytes = base64.b64decode(img_base64)

        # 将图片保存到本地文件
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/{}'.format(name))
        if not os.path.exists(image_path):
            with open(image_path, 'wb') as f:
                f.write(img_bytes)

    def get_slide_button(self):
        """获取滑块元素对象"""
        # 获取滑块按钮元素对象
        slider_btn = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jigsawCircle")))
        return slider_btn

    def run(self):
        # 发送网页请求
        self.browser.get(url=self.url)
        time.sleep(1)

        # 获取不带缺口的验证码图片
        image1 = "before_crack.png"
        self.get_captcha_img(image1)
        time.sleep(1)

        # 点击滑块触发缺口出现的canvas验证码背景图片
        # 获取滑块按钮元素对象
        slider_btn = self.get_slide_button()
        slider_btn.click()
        time.sleep(0.5)

        # 获取带缺口的canvas背景图片
        image2 = 'after_crack.png'
        self.get_captcha_img(image2)
        time.sleep(1)

        # 获取缺口位置
        slide_distance = self.get_distance(image1, image2)

        # 模拟拖动滑块
        self.move_2_distance(slide_distance)

    def move_2_distance(self, slide_distance):
        """
        模拟拖动滑块
        :param slide_distance: 滑块拖动距离
        :return:
        """
        # 获取滑块按钮元素对象
        slider_btn = self.get_slide_button()
        self.action_chains.click_and_hold(slider_btn).perform()
        self.action_chains.move_by_offset(slide_distance-10, 0)  # 设置移动距离
        self.action_chains.release().perform()

        time.sleep(5)

    @staticmethod
    def get_distance(img1, img2):
        """
        比对两张图片的像素点，判断出缺口位置
        :param img1: 不带缺口的canvas背景图片
        :param img2: 带缺口的canvas背景图片
        :return:
        """
        img1_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/{}'.format(img1))
        img2_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/{}'.format(img2))

        # 打开待对比的图片
        image1 = Image.open(img1_path)
        image2 = Image.open(img2_path)

        # 比对两张图片的像素点的不同
        diff_position = ImageChops.difference(image1, image2).getbbox()
        print(diff_position)  # (174, 64, 213, 103) (left, top, right, bottom)
        return int(diff_position[0])


class SliderCanvasCrack2Captcha(object):
    """
    基于canvas的第二种滑动拼图验证码
    dst_url: https://account.zbj.com/login (猪八戒网站登录页面)
    特征：点击按钮触发验证码的出现(第一次触发验证码图片就带有缺块和缺口)
    解决方案：通过js给canvas画布添加style样式：display:none--->作用是去掉带缺块剩缺口的验证码图片
    在次添加对应的canvas画布添加style样式: display: block--->作用是显示不带缺块缺口的验证码图片
    """

    def __init__(self):
        """初始化"""
        self.url = "https://account.zbj.com/login"
        self.driver_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        self.browser = webdriver.Chrome(executable_path=self.driver_path)
        self.wait = WebDriverWait(self.browser, timeout=20)
        self.action_chains = ActionChains(self.browser)

    def __str__(self):
        self.browser.close()

    def get_slide_click_button(self):
        """
        获取初始验证按钮
        :return:
        """
        button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_radar_tip_content")))
        return button

    def run(self):
        """启动验证码识别图片"""
        # 发送网页请求
        self.browser.get(url=self.url)
        time.sleep(3)

        # 点击初始验证按钮，触发验证码的出现
        button = self.get_slide_click_button()
        button.click()
        time.sleep(0.5)

        # 获取带缺口的验证码图片
        # 隐藏带缺块的验证码
        js1 = 'document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].style["display"]="none";'
        # 获取canvas验证码
        js2 = 'return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png");'
        name1 = "zhu_after_captcha.png"  # 验证码图片名字
        js_list = [js1, js2]
        self.get_captcha_img(js_list, name1)

        # 获取不带缺口的验证码图片
        # 隐藏带缺口缺块的原始图片
        js1 = 'document.getElementsByClassName("geetest_canvas_fullbg geetest_fade geetest_absolute")' \
              '[0].style["display"]="block";'
        # 获取canvas验证码
        js2 = 'return document.getElementsByClassName("geetest_canvas_fullbg geetest_fade geetest_absolute")' \
              '[0].toDataURL("image/png");'
        name2 = "zhu_before_captcha.png"  # 验证码图片名字
        js_list = [js1, js2]
        self.get_captcha_img(js_list, name2)

        # 获取缺口位置
        slide_distance = self.get_distance(name1, name2)
        # 模拟拖动滑块
        self.move_2_distance(slide_distance)

        time.sleep(5)

    def get_captcha_img(self, js_list, name="captcha.png"):
        """
        获取验证码图片
        :param js_list: 待执行的JS脚本列表容器
        :param name: 验证码图片对象
        :return:
        """
        # 执行js脚本,给canvas画布添加style样式：display: none;
        self.browser.execute_script(js_list[0])
        time.sleep(0.5)

        # 获取canvas图片
        # 执行js代码并拿到图片base64数据
        img_info = self.browser.execute_script(js_list[1])

        # 获取经过base64加密的图片信息
        img_base64 = img_info.split(",")[1]

        # 将base64加密的图片信息转化为图片字节流(bytes)
        img_bytes = base64.b64decode(img_base64)

        # 将图片保存到本地文件
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/{}'.format(name))
        if not os.path.exists(image_path):
            with open(image_path, 'wb') as f:
                f.write(img_bytes)

    def move_2_distance(self, slide_distance):
        """
        模拟拖动滑块
        :param slide_distance: 滑块拖动距离
        :return:
        """
        # 获取滑块按钮元素对象
        slider_btn = self.get_slide_click_button()
        self.action_chains.click_and_hold(slider_btn).perform()
        self.action_chains.move_by_offset(slide_distance - 10, 0)  # 设置移动距离
        self.action_chains.release().perform()

        time.sleep(5)

    @staticmethod
    def get_distance(img1, img2):
        """
        比对两张图片的像素点，判断出缺口位置
        :param img1: 不带缺口的canvas背景图片
        :param img2: 带缺口的canvas背景图片
        :return:
        """
        img1_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/{}'.format(img1))
        img2_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/{}'.format(img2))

        # 打开待对比的图片
        image1 = Image.open(img1_path)
        image2 = Image.open(img2_path)

        # 比对两张图片的像素点的不同
        diff_position = ImageChops.difference(image1, image2).getbbox()
        print(diff_position)  # (174, 64, 213, 103) (left, top, right, bottom)
        return int(diff_position[0])


def main():
    # s = SliderCanvasCrackCaptcha()
    # s.run()
    s = SliderCanvasCrack2Captcha()
    s.run()


if __name__ == '__main__':
    main()




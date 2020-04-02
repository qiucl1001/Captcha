# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
from parsel import Selector


class SliderCrackCaptcha(object):
    """滑块缺口验证码"""

    def __init__(self):
        """初始化"""
        self.url = "http://www.porters.vip/captcha/jigsaw.html"
        self.driver_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        self.browser = webdriver.Chrome(executable_path=self.driver_path)
        self.wait = WebDriverWait(self.browser, timeout=20)
        self.action_chains = ActionChains(self.browser)

    def __str__(self):
        self.browser.close()

    def run(self):
        # 使用selenium发送网络请求
        self.browser.get(url=self.url)
        time.sleep(1)

        # 获取滑块按钮元素对象
        slider_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jigsawCircle")))

        # 点击滑块按钮元素触发缺口位置的出现
        slider_button.click()
        time.sleep(0.5)

        # 获取网页源代码
        html = self.browser.page_source
        self.get_style(html)

    def get_style(self, html):
        """
        获取缺块和缺口元素的样式
        :param html: 带有缺口缺块的网页源代码
        :return:
        """
        selector = Selector(html)
        # 获取缺块的css样式
        missblock = selector.css('#missblock::attr("style")').get()
        # 获取缺口的css样式
        targetblock = selector.css('#targetblock::attr("style")').get()
        print({"missblock": missblock, "targetblock": targetblock})

        # 获取缺块和缺口的left样式属性值
        miss_target_left_li = list(map(lambda x: re.findall(r'left: (\d+|\d+\.\d+)px', x), [missblock, targetblock]))
        print(miss_target_left_li)

        # 计算缺口位置
        slider_distance = float(miss_target_left_li[1][0]) - float(miss_target_left_li[0][0])
        self.move_2_dst(slider_distance)

    def move_2_dst(self, slider_distance):
        """
        模拟鼠标滑动缺块拼图
        :param slider_distance:滑块轨迹距离
        :return:
        """
        # 在次获取滑块按钮元素对象
        slider_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jigsawCircle")))

        self.action_chains.click_and_hold(slider_button).perform()  # 鼠标按住滑块不松手
        self.action_chains.move_by_offset(slider_distance, 0)  # 模拟鼠标按住滑块拖动slider_distance距离
        self.action_chains.release().perform()  # 松开鼠标

        time.sleep(5)


def main():
    s = SliderCrackCaptcha()
    s.run()


if __name__ == '__main__':
    main()




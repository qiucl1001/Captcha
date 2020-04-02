# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SliderCaptcha(object):
    """滑块验证码"""

    def __init__(self):
        self.url = "http://www.porters.vip/captcha/sliders.html"
        self.driver_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        self.browser = webdriver.Chrome(executable_path=self.driver_path)
        self.wait = WebDriverWait(self.browser, timeout=20)
        self.action_chains = ActionChains(self.browser)

    def __str__(self):
        self.browser.close()

    def run(self):
        self.browser.get(url=self.url)
        time.sleep(1)
        # 获取滑块元素对象
        # hover = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "hover")))  # 通过类选择器来定位滑块元素
        hover = self.wait.until(EC.presence_of_element_located((By.ID, "sliderblock")))

        # 模拟人为拖动滑块
        # 通过分析CSS样式得出滑块需要滑动的轨迹为340px
        self.action_chains.click_and_hold(hover).perform()  # 点击并按住滑块不松手
        self.action_chains.move_by_offset(340, 0)  # 设置滑块轨迹， 模拟滑块横向滑动340px，纵向滑块滑动距离为0px
        self.action_chains.release().perform()  # 松快鼠标

        time.sleep(5)


def main():
    s = SliderCaptcha()
    s.run()


if __name__ == '__main__':
    main()


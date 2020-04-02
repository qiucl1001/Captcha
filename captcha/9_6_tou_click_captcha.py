# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import time
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class TouClick(object):
    """
    点触验证码之文字点选验证码识别
    本例以网页版YY登入页面本例
    dst_url: "https://aq.yy.com/"
    """

    def __init__(self):
        """初始化"""
        self.dst_url = "https://aq.yy.com/"
        self.driver_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"  # chrome浏览器驱动路径
        self.browser = webdriver.Chrome(executable_path=self.driver_path)
        self.wait = WebDriverWait(self.browser, timeout=10)
        self.action_chains = ActionChains(self.browser)

        self.username = "qcl"  # 登入用户名
        self.password = "123456"  # 登入密码
        self.retry_click_times = 3  # 重复点击登入按钮，触发点触验证码的出现

    def get_user_pass_btn_ele(self):
        """
        获取登入页面的用户名密码输入框以及登入按钮元素
        :return: 以列表的形式返回个元素
        """
        # 定位元素，切换到子frame标签中
        self.browser.switch_to.frame("udbsdk_frm_normal")
        # 用户名所在标签元素对象
        user_input = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="form_item"]/span[@class="m_textbox"]/input[@class="placeholder E_acct"]'))
        )
        # 密码所在标签元素对象
        password_input = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="form_item"]/span[@class="m_textbox"]/input[@class="placeholder E_passwd"]'))
        )
        # 登入按钮所在标签元素对象，此处能获取到2个，第一个不可见，第二个可用
        login_button = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.m_button_large.E_login'))
        )
        return [user_input, password_input, login_button]

    def run(self):
        """启动selenium网页端自动化测试工具套件"""
        # 向目标网页发送请求
        self.browser.get(url=self.dst_url)
        # response = self.browser.page_source  # 获取网页源代码
        time.sleep(1)

        # 获取登入页面的用户名密码输入框以及登入按钮元素
        elements_list = self.get_user_pass_btn_ele()

        # 模拟登入，触发点触验证码出现
        elements_list[0].send_keys(self.username)
        elements_list[1].send_keys(self.password)
        for _ in range(self.retry_click_times):
            elements_list[2][1].click()
            try:
                m_interactive = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.ID, 'm_interactive'))
                )
            except TimeoutException:
                continue
            if m_interactive:
                break

        # 获取点触验证码图片
        time.sleep(3)
        self.get_tou_click_image()

        time.sleep(2)
        self.browser.close()

    def get_screen_shot(self):
        """
        获取网页截图
        :return: 网页截图：screen_shot
        """
        # self.browser.switch_to.parent_frame()
        # time.sleep(1)
        screen_shot = self.browser.get_screenshot_as_png()
        screen_shot = Image.open(BytesIO(screen_shot))
        screen_shot.save("111.png")
        return screen_shot

    def get_captcha_location(self):
        """
        获取点触验证码位置和大小
        :return: 以元组的范式返回: (left, top, right, bottom)
        """
        # 获取点触验证码图片元素
        tou_click = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "pw_main"))
        )
        location = tou_click.location
        size = tou_click.size
        print(size)  # {'height': 173, 'width': 272}
        left = location['x']
        right = location['x'] + size['width']
        top = location['y']
        bottom = location['y'] + size['height']
        # {'left': 17, 'top': 42, 'right': 289, 'bottom': 215}
        return left, top, right, bottom

    def get_tou_click_image(self, name="tou_click.png"):
        """
        获取点触验证码图片
        :param name: 验证码图片名字
        :return:
        """
        left, top, right, bottom = self.get_captcha_location()
        print({"left": left, "top": top, "right": right, "bottom": bottom})
        screen_shot = self.get_screen_shot()
        captcha = screen_shot.crop((left, top, right, bottom))
        print(type(captcha))
        print(captcha)

        # 将图片保存到本地
        captcha.save(name)


def main():
    """启动程序"""
    t = TouClick()
    t.run()


if __name__ == '__main__':
    main()





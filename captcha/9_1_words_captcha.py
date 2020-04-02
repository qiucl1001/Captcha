# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import os
import pytesseract
from PIL import Image
from captcha.libs.ydm3 import identify


def use_pytesseract():
    """使用pytesseract开源OCR库识别文字图片"""

    # 获取保存哎本地的图片路径
    # 图片文字：PJ2ZM2
    images = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/words_captcha.png')

    # 使用pytesseract开源OCR库识别图片中的文字并打印
    print(pytesseract.image_to_string(images))  # PJ ZZIVIZ


def use_image_handle_l():
    """使用PIL中的Image对图片进行灰度处理(去彩色)"""
    # 获取保存哎本地的图片路径
    # 图片文字：PJ2ZM2
    images = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/words_captcha.png')

    # 对图片进行灰度处理
    grays = Image.open(images).convert('L')
    # print(grays.show())
    return grays


def use_image_handle_bin(threshold=160):
    """
    对灰度处理后的图片进行二值化处理(降低干扰，噪点等)
    :param threshold: 二值化阈值(0~255)；默认为160
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    grays = use_image_handle_l()
    res = grays.point(table, '1')
    # print(res.show())
    print(pytesseract.image_to_string(res))  # 无法识别图片中的内容！！！


def use_ydm():
    """借助三方技术栈云打码平台"""
    # 获取本地保存的图片路径
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/words_captcha.png')

    # 获取图片的二进制数据
    with open(image_path, "rb") as f:
        content = f.read()
        # 调用云打码进行识别
        if content:
            res = identify(content)
            print(res)


if __name__ == '__main__':
    # use_pytesseract()
    # use_image_handle_l()
    # use_image_handle_bin()
    use_ydm()




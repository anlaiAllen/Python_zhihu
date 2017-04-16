import time
import requests
from lxml import etree

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
}

session = requests.Session()

def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=headers)
    sel = etree.HTML(response.content)
    xsrf = sel.xpath('//input[@name="_xsrf"]/@value')[0]
    return xsrf


def get_captcha():
    """
    把验证码图片保存到当前目录，手动识别验证码
    :return:
    """
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
    captcha = input("验证码：")
    return captcha


def login(email, password):
    login_url = 'https://www.zhihu.com/login/email'
    data = {
        'email': email,
        'password': password,
        '_xsrf': get_xsrf(),
        "captcha": get_captcha(),
        'remember_me': 'true'
    }
    response = session.post(login_url, data=data, headers=headers)
    login_code = response.json()
    print(login_code['msg'])



if __name__ == '__main__':
    email = "843004460@qq.com"
    password = "anlaichun"
    login(email, password)


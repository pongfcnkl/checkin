import requests
import sys
import json
import time

# note.youdao.com 有道云笔记签到


def noteyoudao(YNOTE_SESS: str, user: str, passwd: str):
    s = requests.Session()
    checkin_url = 'https://note.youdao.com/yws/mapi/user?method=checkin'
    cookies = {
        'YNOTE_LOGIN': 'true',
        'YNOTE_SESS': YNOTE_SESS
    }
    r = s.post(url=checkin_url, cookies=cookies, verify=True)
    if r.status_code == 200:
        # print(r.text)
        info = json.loads(r.text)
        total = info['total'] / 1048576
        space = info['space'] / 1048576
        t = time.strftime('%Y-%m-%d %H:%M:%S',
                          time.localtime(info['time'] / 1000))
        print(user + '签到成功，本次获取' + str(space) +
              'M, 总共获取' + str(total) + 'M, 签到时间' + str(t))
    # cookie 登录失效，改用用户名密码登录
    else:
        login_url = 'https://note.youdao.com/login/acc/urs/verify/check?app=web&product=YNOTE&tp=ursto' \
                    'ken&cf=6&fr=1&systemName=&deviceType=&ru=https%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2Flo' \
                    'ginCallback.html&er=https%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&vc' \
                    'ode=&systemName=Windows&deviceType=WindowsPC&timestamp=1517235699501'
        parame = {
            'username': user,
            'password': passwd
        }

        r = s.post(url=login_url, data=parame, verify=True)
        x = [i.value for i in s.cookies if i.name == 'YNOTE_SESS']
        if x.__len__() == 0:
            YNOTE_SESS = "-1"
            print(user + "登录失败")
            print(r.history)
            print(s.cookies)
            return
        else:
            print(user + '登陆成功，更新YNOTE_SESS,重新签到')
            YNOTE_SESS = x[0]
            noteyoudao(YNOTE_SESS, user, passwd)
            return YNOTE_SESS


if __name__ == '__main__':
    # 直接调用可以使用用户名密码登录
    if len(sys.argv) < 3:
        print('请输入用户名密码')
    else:
        noteyoudao('1', sys.argv[1], sys.argv[2])

import requests


class AliyunSignIn(object):
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token

    def get_access_token(self):
        url = 'https://auth.aliyundrive.com/v2/account/token'
        headers = {
            "Content-Type": "application/json; charset=utf-8",
        }
        data = {
            "grant_type": "refresh_token",
            "app_id": "pJZInNHN2dZWk8qg",
            "refresh_token": self.refresh_token
        }
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            self.access_token = f'Bearer {res.json()["access_token"]}'
            self.nick_name = res.json()['nick_name']
            return True
        return False

    def sign_in(self):
        print('开始获取access_token')
        if_ = self.get_access_token()
        print(f'access_token获取完成，欢迎{self.nick_name}\n开始签到')
        if not if_:
            print('获取access_token失败')
        url = 'https://member.aliyundrive.com/v1/activity/sign_in_list'
        headers = {
            "Content-Type": "application/json",
            'Authorization': self.access_token,
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'
        }
        data = {}
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200 and res.json()['success']:
            res_json = res.json()
            notice = ''
            prefix = ''
            for l in res_json['result']['signInLogs']:
                if l['status'] != 'miss':
                    prefix = f'第{l["day"]}天'
                    notice = l['notice'] + ' ' + l['reward']['description']
            notifyStr = f'🎉{prefix}签到成功'
            if notice:
                notifyStr = f'{notifyStr},获得【{notice}】'
            print(notifyStr)


if __name__ == '__main__':
    refresh_token = ''
    ali = AliyunSignIn(refresh_token)
    ali.sign_in()

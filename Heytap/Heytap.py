# -*- coding: utf-8 -*-
# @Time    : 2021/7/18
# @Author  : hwkxk(丶大K丶)
# @Email   : k@hwkxk.cn
# Modified By liqman
## 新增多账号功能
## 新增pushplus、tgbot、钉钉机器人、企业微信机器人通知
## 新增早睡打卡任务申请
## 早睡打卡任务打卡待更新

import requests, json, time, traceback, hmac, hashlib, base64, urllib.parse

# 请配置该值 ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
## 早睡打卡瓜分积分开关，开启请填true
zaoshui_open = 'false'
## 下面HT_cookies_list、HT_UserAgent_list、notice_list请一一对应，notice_list某一行无通知可留空
## 填入APP抓取到Cookies,可以直接把抓包的全部cookie值填入，一般包含sa_distinct_id=、TOKENSID=、ENCODE_TOKENSI=、app_param=、 这几项即可，一个cookie一行
HT_cookies_list = [
    'sa_distinct_id=d3BNWWJFZjErYTlIK3pJb1k4bnRjZz09;source_type=501;path=/;UM_distinctid=17979ebd03d1b7-06454763109e3e-2d2c1303-50a5a-17979ebd03e7d6;Op_lvt_f18367c55fd7569d9000cd9986846577=1621878820;Op_lpvt_f18367c55fd7569d9000cd9986846577=1621878820;sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22d3BNWWJFZjErYTlIK3pJb1k4bnRjZz09%22%2C%22%24device_id%22%3A%221799f82922a3b9-08243c123416ba-2d2c1303-330330-1799f82922b583%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22d3BNWWJFZjErYTlIK3pJb1k4bnRjZz09%22%7D;newopkey=3vDW31dCcHvC9056hlC7dNw0sBzNUYt_DF3zEbjqOx5YRC2US81dFnA-SiRRrV0RU89gMLT80_M;s_channel=oppo_appstore;s_version=200402;app_utm={"utm_source":"direct","utm_medium":"direct","utm_campaign":"direct","utm_term":"direct"};app_innerutm={"us":"direct","um":"direct","uc":"direct","ut":"direct"};Personalized=1;token=TOKEN_eyJhbGciOiJFQ0RTQSIsInYiOiIxIn0.eyJleHAiOjE2MjkxMDY3MzIxNDEsImlkIjoiNDY1ODExMTM1IiwiaWRjIjoic2hvdW1pbmciLCJ0aWQiOiIyWUVXeFZYbFpLUXBaNS9rVm1BUEg4eEdiZys2R1hJNkJNdmJFbnhKZU5yTnNQVFZYMnMxZlMrZHRabmlMcGY4QWtZa0R0Q3FxbHFsV3JwQmRhc0oxUEdSbEI2SmYwUkRmMlltamI1aGs2cz0ifQ.MEQCIERs_KT_DOnid5zmod0Ze_X6RVsnYKgs7mXLOfR-SPu3AiBv9qiq7H6bVbxouxOP44aCRm32bhsAUbnJdkKSImYKLw;us=direct;um=direct;uc=direct;ut=direct;utm_source=direct;utm_medium=direct;utm_campaign=direct;utm_term=direct;memberinfo=%7B%22id%22%3A%22465811135%22%2C%22name%22%3A%22%E7%94%A8%E6%88%B702576761998%22%2C%22oid%22%3A%22d3BNWWJFZjErYTlIK3pJb1k4bnRjZz09%22%7D;app_param={"model":"LE2120","brand":"OnePlus","rom":"Hydrogen OS","guid":"","ouid":"","duid":"","udid":"","apid":"","sa_device_id":"c7c8fe1d36db9d13","romVersion":"Oxygen OS 11.2.7.7.LE15AA","apkPkg":"com.oppo.store"};NEWOPPOSID=eyJpdiI6IlJnYVpyc0VweFlhWUU5M2NaZEVTVXc9PSIsInZhbHVlIjoiOVptcFJUQzgxY0h1cTEwdGpES1ZUS21zdEFBdFE0ZjRnb3pUajFmQTNvQ1ZBR0NCVWUrd1JablNnVWJ1K3piWjlqSGw2QVdIVStGdjlvM05MamdjS1BjNytQT2JEYVd3M1RScXBuajdYS2p4YUhycmsvdVB5cXRPUWVmYjRqZlkiLCJtYWMiOiJhZmU2YzgxNDQ0NGYwMzMzNzYwNzE2YzEyYzQyZmQyM2RmODUxYmZhNTgyYzkxMWU0M2VhNWQ0Y2Y4MDhiOTRlIn0=;opkey=eyJpdiI6IlJnYVpyc0VweFlhWUU5M2NaZEVTVXc9PSIsInZhbHVlIjoiOVptcFJUQzgxY0h1cTEwdGpES1ZUS21zdEFBdFE0ZjRnb3pUajFmQTNvQ1ZBR0NCVWUrd1JablNnVWJ1K3piWjlqSGw2QVdIVStGdjlvM05MamdjS1BjNytQT2JEYVd3M1RScXBuajdYS2p4YUhycmsvdVB5cXRPUWVmYjRqZlkiLCJtYWMiOiJhZmU2YzgxNDQ0NGYwMzMzNzYwNzE2YzEyYzQyZmQyM2RmODUxYmZhNTgyYzkxMWU0M2VhNWQ0Y2Y4MDhiOTRlIn0=',  # 账号1
]
## 填入抓取到User-Agent，参考以下 【建议使用自己抓取的！避免异常/防黑(推测）】
HT_UserAgent_list = [
    'Mozilla/5.0 (Linux; Android 11; LE2120 Build/RKQ1.201105.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.88 Mobile Safari/537.36 oppostore/200402 Hydrogen OS/Oxygen OS 11.2.7.7.LE15AA brand/OnePlus model/LE2120',  # 账号1
]
## 填入推送方式及对应值

# 用户登录全局变量
client = None
session = None
loggerinfo = None


# 获取个人信息，判断登录状态
def get_infouser(HT_cookies, HT_UA):
    flag = False
    global session
    session = requests.Session()
    headers = {
        'Host': 'www.heytap.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'User-Agent': HT_UA,
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'cookie': HT_cookies
    }
    response = session.get('https://www.heytap.com/cn/oapi/users/web/member/info', headers=headers)
    response.encoding = 'utf-8'
    try:
        result = response.json()
        if result['code'] == 200:
            loggerinfo = '==== 欢太商城任务 ====\n\n'
            loggerinfo += '【登录成功】: ' + result['data']['realName']+'\n\n'
            flag = True
        else:
            loggerinfo += '【登录失败】: ' + result['errorMessage']+'\n\n'
    except Exception as e:
        print(traceback.format_exc())
    if flag:
        return session,loggerinfo
    else:
        return False


# 任务中心列表，获取任务及任务状态
def taskCenter():
    headers = {
        'Host': 'store.oppo.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'User-Agent': HT_UserAgent,
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'cookie': HT_cookies,
        'referer': 'https://store.oppo.com/cn/app/taskCenter/index'
    }
    res1 = client.get('https://store.oppo.com/cn/oapi/credits/web/credits/show', headers=headers)
    res1 = res1.json()
    print(res1)
    return res1


# 每日签到
# 位置: APP → 我的 → 签到
def daySign_task(loggerinfo):
    try:
        dated = time.strftime("%Y-%m-%d")
        headers = {
            'Host': 'store.oppo.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': HT_UserAgent,
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'cookie': HT_cookies,
            'referer': 'https://store.oppo.com/cn/app/taskCenter/index'
        }
        res = taskCenter()
        status = res['data']['userReportInfoForm']['status']
        if status == 0:
            res = res['data']['userReportInfoForm']['gifts']
            for data in res:
                if data['date'] == dated:
                    qd = data
            if qd['today'] == False:
                data = "amount=" + str(qd['credits'])
                res1 = client.post('https://store.oppo.com/cn/oapi/credits/web/report/immediately', headers=headers,
                                   data=data)
                res1 = res1.json()
                if res1['code'] == 200:
                    loggerinfo += '【每日签到成功】: ' + res1['data']['message']+'\n\n'
                else:
                    loggerinfo += '【每日签到失败】: ' + res1+'\n\n'
            else:
                # print(str(qd['credits']),str(qd['type']),str(qd['gift']))
                if len(qd['type']) == 0:
                    data = "amount=" + str(qd['credits'])
                else:
                    data = "amount=" + str(qd['credits']) + "&type=" + str(qd['type']) + "&gift=" + str(qd['gift'])
                res1 = client.post('https://store.oppo.com/cn/oapi/credits/web/report/immediately', headers=headers,
                                   data=data)
                res1 = res1.json()
                if res1['code'] == 200:
                    loggerinfo += '【每日签到成功】: ' + res1['data']['message']+'\n\n'
                else:
                    loggerinfo += '【每日签到失败】: ' + str(res1)+'\n\n'
        else:
            loggerinfo += '【每日签到】: 已经签到过了！\n\n'
        time.sleep(1)
        return loggerinfo
    except Exception as e:
        print(traceback.format_exc())


# 浏览商品 10个sku +20 分
# 位置: APP → 我的 → 签到 → 每日任务 → 浏览商品
def daily_viewgoods(loggerinfo):
    try:
        headers = {
            'clientPackage': 'com.oppo.store',
            'Host': 'msec.opposhop.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': 'okhttp/3.12.12.200sp1',
            'Accept-Encoding': 'gzip',
            'cookie': HT_cookies,
        }
        res = taskCenter()
        res = res['data']['everydayList']
        for data in res:
            if data['name'] == '浏览商品':
                qd = data
        if qd['completeStatus'] == 0:
            shopList = client.get('https://msec.opposhop.cn/goods/v1/SeckillRound/goods/3016?pageSize=12&currentPage=1')
            res = shopList.json()
            if res['meta']['code'] == 200:
                for skuinfo in res['detail']:
                    skuid = skuinfo['skuid']
                    print('正在浏览商品ID：', skuid)
                    client.get('https://msec.opposhop.cn/goods/v1/info/sku?skuId=' + str(skuid), headers=headers)
                    time.sleep(5)
                res2 = cashingCredits(qd['marking'], qd['type'], qd['credits'])
                if res2 == True:
                    loggerinfo += '【每日浏览商品】: ' + '任务完成！积分领取+' + str(qd['credits'])+'\n\n'
                else:
                    loggerinfo += '【每日浏览商品】: ' + '领取积分奖励出错！'+'\n\n'
            else:
                loggerinfo += '【每日浏览商品】: ' + '错误，获取商品列表失败'+'\n\n'
        elif qd['completeStatus'] == 1:
            res2 = cashingCredits(qd['marking'], qd['type'], qd['credits'])
            if res2 == True:
                loggerinfo += '【每日浏览商品】: ' + '任务完成！积分领取+' + str(qd['credits'])+'\n\n'
            else:
                loggerinfo += '【每日浏览商品】: ' + '领取积分奖励出错！'+'\n\n'
        else:
            loggerinfo += '【每日浏览商品】: ' + '任务已完成！'+'\n\n'
        return loggerinfo
    except Exception as e:
        print(traceback.format_exc())


def daily_sharegoods(loggerinfo):
    try:
        headers = {
            'clientPackage': 'com.oppo.store',
            'Host': 'msec.opposhop.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': 'okhttp/3.12.12.200sp1',
            'Accept-Encoding': 'gzip',
            'cookie': HT_cookies,
        }
        daySignList = taskCenter()
        res = daySignList
        res = res['data']['everydayList']
        for data in res:
            if data['name'] == '分享商品到微信':
                qd = data
        if qd['completeStatus'] == 0:
            count = qd['readCount']
            endcount = qd['times']
            while (count <= endcount):
                client.get('https://msec.opposhop.cn/users/vi/creditsTask/pushTask?marking=daily_sharegoods',
                           headers=headers)
                count += 1
            res2 = cashingCredits(qd['marking'], qd['type'], qd['credits'])
            if res2 == True:
                loggerinfo += '【每日分享商品】: ' + '任务完成！积分领取+' + str(qd['credits'])+'\n\n'
            else:
                loggerinfo += '【每日分享商品】: ' + '领取积分奖励出错！'+'\n\n'
        elif qd['completeStatus'] == 1:
            res2 = cashingCredits(qd['marking'], qd['type'], qd['credits'])
            if res2 == True:
                loggerinfo += '【每日分享商品】: ' + '任务完成！积分领取+' + str(qd['credits'])+'\n\n'
            else:
                loggerinfo += '【每日分享商品】: ' + '领取积分奖励出错！'+'\n\n'
        else:
            loggerinfo += '【每日分享商品】: ' + '任务已完成！'+'\n\n'
        return loggerinfo
    except Exception as e:
        print(traceback.format_exc())


def daily_viewpush(loggerinfo):
    try:
        headers = {
            'clientPackage': 'com.oppo.store',
            'Host': 'msec.opposhop.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': 'okhttp/3.12.12.200sp1',
            'Accept-Encoding': 'gzip',
            'cookie': HT_cookies,
        }
        daySignList = taskCenter()
        res = daySignList
        res = res['data']['everydayList']
        for data in res:
            if data['name'] == '点推送消息':
                qd = data
        if qd['completeStatus'] == 0:
            count = qd['readCount']
            endcount = qd['times']
            while (count <= endcount):
                client.get('https://msec.opposhop.cn/users/vi/creditsTask/pushTask?marking=daily_viewpush',
                           headers=headers)
                count += 1
            res2 = cashingCredits(qd['marking'], qd['type'], qd['credits'])
            if res2 == True:
                loggerinfo += '【每日点推送】: ' + '任务完成！积分领取+' + str(qd['credits'])+'\n\n'
            else:
                loggerinfo += '【每日点推送】: ' + '领取积分奖励出错！'+'\n\n'
        elif qd['completeStatus'] == 1:
            res2 = cashingCredits(qd['marking'], qd['type'], qd['credits'])
            if res2 == True:
                loggerinfo += '【每日点推送】: ' + '任务完成！积分领取+' + str(qd['credits'])+'\n\n'
            else:
                loggerinfo += '【每日点推送】: ' + '领取积分奖励出错！'+'\n\n'
        else:
            loggerinfo += '【每日点推送】: ' + '任务已完成！'+'\n\n'
        return loggerinfo
    except Exception as e:
        print(traceback.format_exc())

# 早睡早起打卡
def zaoshui_task(loggerinfo):
    print(HT_cookies)
    try:
        headers = {
            'Host':'store.oppo.com',
            'Connection':'keep-alive',
            's_channel':'huawei',
            'utm_term':'direct',
            'utm_campaign':'direct',
            'utm_source':'direct',
            'ut':'direct',
            'uc':'zaoshuidaka',
            'sa_device_id':'a47b10e94b2de15a',
            'guid':'',
            'sa_distinct_id':'T0Q1bjExZ2pFL0crWUlMVmROOFFNdz09',
            'clientPackage':'com.oppo.store',
            'Cache-Control':'no-cache',
            'um':'hudongleyuan',
            'User-Agent': HT_UserAgent,
            'ouid':'',
            'Accept':'application/json, text/plain, */*',
            'source_type':'501',
            'utm_medium':'direct',
            'brand':'samsung',
            'appId':'',
            's_version':'200804',
            'us':'gerenzhongxin',
            'appKey':'',
            'X-Requested-With':'com.oppo.store',
            'Sec-Fetch-Site':'same-origin',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Dest':'empty',
            'Referer':'https://store.oppo.com/cn/app/cardingActivities?us=gerenzhongxin&um=hudongleyuan&uc=zaoshuidaka',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': HT_cookies,
        }
        response = client.get('https://store.oppo.com/cn/oapi/credits/web/clockin/applyOrClockIn',
                              headers=headers)
        print(json.loads(response.text)['code'])
        if json.loads(response.text)['code'] == 200:
            loggerinfo += '【早睡打卡】申请成功，请当天19:30-22:00手动打卡'+'\n\n'
        if json.loads(response.text)['code'] == 1000005:
            loggerinfo += '【早睡打卡】积分不足，申请失败'+'\n\n'
        return loggerinfo
    except Exception as e:
        print(traceback.format_exc())


# 执行完成任务领取奖励
def cashingCredits(info_marking, info_type, info_credits):
    headers = {
        'Host': 'store.oppo.com',
        'clientPackage': 'com.oppo.store',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'User-Agent': HT_UserAgent,
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'cookie': HT_cookies,
        'Origin': 'https://store.oppo.com',
        'X-Requested-With': 'com.oppo.store',
        'referer': 'https://store.oppo.com/cn/app/taskCenter/index?us=gerenzhongxin&um=hudongleyuan&uc=renwuzhongxin'
    }

    data = "marking=" + str(info_marking) + "&type=" + str(info_type) + "&amount=" + str(info_credits)
    res = client.post('https://store.oppo.com/cn/oapi/credits/web/credits/cashingCredits', data=data, headers=headers)
    res = res.json()
    if res['code'] == 200:
        return True
    else:
        return False


# 活动平台抽奖通用接口
def lottery(datas):
    headers = {
        'clientPackage': 'com.oppo.store',
        'Accept': 'application/json, text/plain, */*;q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Connection': 'keep-alive',
        'User-Agent': HT_UserAgent,
        'Accept-Encoding': 'gzip, deflate',
        'cookie': HT_cookies,
        'Origin': 'https://hd.oppo.com',
        'X-Requested-With': 'XMLHttpRequest',
    }
    res = client.post('https://hd.oppo.com/platform/lottery', data=datas, headers=headers)
    res = res.json()
    return res


# 活动平台完成任务接口
def task_finish(aid, t_index):
    headers = {
        'Accept': 'application/json, text/plain, */*;q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Connection': 'keep-alive',
        'User-Agent': HT_UserAgent,
        'Accept-Encoding': 'gzip, deflate',
        'cookie': HT_cookies,
        'Origin': 'https://hd.oppo.com',
        'X-Requested-With': 'XMLHttpRequest',
    }
    datas = "aid=" + str(aid) + "&t_index=" + str(t_index)
    res = client.post('https://hd.oppo.com/task/finish', data=datas, headers=headers)
    res = res.json()
    return res


# 活动平台领取任务奖励接口
def task_award(aid, t_index):
    headers = {
        'Accept': 'application/json, text/plain, */*;q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Connection': 'keep-alive',
        'User-Agent': HT_UserAgent,
        'Accept-Encoding': 'gzip, deflate',
        'cookie': HT_cookies,
        'Origin': 'https://hd.oppo.com',
        'X-Requested-With': 'XMLHttpRequest',
    }
    datas = "aid=" + str(aid) + "&t_index=" + str(t_index)
    res = client.post('https://hd.oppo.com/task/award', data=datas, headers=headers)
    res = res.json()
    return res


# 天天积分翻倍活动 - 长期 最多3次
def tiantianjifen_lottery(loggerinfo):
    x = 1
    while x <= 3:
        data = "aid=675&lid=1289&mobile=&authcode=&captcha=&isCheck=0&source_type=501&s_channel=oppo_appstore&sku=&spu="
        res = lottery(data)
        msg = res['msg']
        print(msg)
        goods_name = res['data']['goods_name']
        loggerinfo += '【天天积分翻倍活动】第' + str(x) + '次，获得:' + str(goods_name)+'\n\n'
        x += 1
        time.sleep(5)
    return loggerinfo


# 位置: APP → 我的 → 赚积分 → 转盘
def zhuanjifen_task(loggerinfo):
    headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': HT_UserAgent,
        'Accept-Encoding': 'gzip, deflate',
        'cookie': HT_cookies,
        'X-Requested-With': 'XMLHttpRequest',
        'referer': 'https://hd.oppo.com/act/m/2021/jifenzhuanpan/index.html?us=gerenzhongxin&um=hudongleyuan&uc=yingjifen'
    }
    data = "aid=1418&lid=1307&mobile=&authcode=&captcha=&isCheck=0&source_type=501&s_channel=oppo_appstore&sku=&spu="
    res = lottery(data)
    print(res)
    goods_name = res['data']['goods_name']
    msg = res['msg']
    loggerinfo += '【赚积分-天天抽奖】获得:' + str(goods_name)+'\n\n'

    taskList = client.get('https://hd.oppo.com/task/list?aid=1418', headers=headers)
    taskList = taskList.json()
    for i, jobs in enumerate(taskList['data']):
        print(jobs['t_status'])  # print (jobs.get('t_index'))
        if jobs['t_status'] == 0:
            t_index = jobs['t_index']
            aid = t_index[:t_index.index("i")]
            finishmsg = task_finish(aid, t_index)
            if finishmsg['no'] == 200:
                time.sleep(1)
                awardmsg = task_award(aid, t_index)
                if awardmsg['no'] == 200:
                    res = lottery(data)
                    msg = res['msg']
                    print(msg)
                    goods_name = res['data']['goods_name']
                    loggerinfo += '【赚积分-天天抽奖】获得:' + str(goods_name)+'\n\n'
                    time.sleep(3)
                else:
                    print('领取奖励出错：', awardmsg)
            else:
                print('完成任务出错：', finishmsg)
        elif jobs['t_status'] == 1:
            t_index = jobs['t_index']
            aid = t_index[:t_index.index("i")]
            awardmsg = task_award(aid, t_index)
            print(awardmsg['no'])
            if awardmsg['no'] == 200:
                res = lottery(data)
                msg = res['msg']
                print(msg)
                goods_name = res['data']['goods_name']
                loggerinfo += '【赚积分-天天抽奖】获得:' + str(goods_name)+'\n\n'
                time.sleep(3)
            else:
                print('领取奖励出错：', awardmsg)
    return loggerinfo


# 智能生活0元抽奖-宠粉转盘
def zhinengshenghuo_lottery(loggerinfo):
    x = 1
    while x <= 5:
        data = "aid=1270&lid=1431&mobile=&authcode=&captcha=&isCheck=0&source_type=501&s_channel=oppo_appstore&sku=&spu="
        res = lottery(data)
        msg = res['msg']
        print(msg)
        goods_name = res['data']['goods_name']
        loggerinfo += '【智能生活转盘】第' + str(x) + '次，获得:' + str(goods_name)+'\n\n'
        x += 1
        time.sleep(5)
    return loggerinfo


# realme宠粉计划-幸运抽奖-转盘
def realme_lottery(loggerinfo):
    data = "aid=1182&lid=1429&mobile=&authcode=&captcha=&isCheck=0&source_type=501&s_channel=oppo_appstore&sku=&spu="
    res = lottery(data)
    msg = res['msg']
    print(msg)
    goods_name = res['data']['goods_name']
    loggerinfo += '【realme宠粉计划转盘】获得:' + str(goods_name)+'\n\n'
    time.sleep(3)
    return loggerinfo

#
# —————短期活动任务↓———————
#

# 超级会员日 瓜分1亿积分转盘抽奖2021.7.12-2021.7.18  每日1次
def vipdate_lottery(loggerinfo):
    dated = int(time.time())
    endtime = time.mktime(time.strptime("2021-7-18 23:59:59", '%Y-%m-%d %H:%M:%S'))  # 设置活动结束日期
    if dated < endtime:
        data = "aid=1589&lid=1486&mobile=&authcode=&captcha=&isCheck=0&source_type=501&s_channel=oppo_appstore&sku=&spu="
        res = lottery(data)
        # print(res)
        msg = res['msg']
        print(msg)
        goods_name = res['data']['goods_name']
        loggerinfo += '【瓜分1亿转盘抽奖活动】获得:' + str(goods_name)+'\n\n'
    else:
        loggerinfo += '【瓜分1亿转盘抽奖活动已结束，不再执行】'+'\n\n'
    return loggerinfo

#企业微信推送
def sendmessage(loggerinfo):
    corpid='wwafb62523249a01bd'
    corpsecret='XfNTpWjf-dSrsEQmPwIzTpF1n1xwnyijbhOGbppHFSE'
    agentid=1000002

    access_token_url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}'
    reg = client.get(url=access_token_url)
    access_token=json.loads(reg.text)['access_token']
    #print(reg.text)

    send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
    #message='hello!'
    content = loggerinfo
    send_msg = {
        "touser": "@all",
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": content,
        },
    }
    client.post(url=send_msg_url, data=json.dumps(send_msg))

# 腾讯云函数入口
def main(event, context):
    # users = readConfig()
    global client
    global loggerinfo
    global HT_cookies
    global HT_UserAgent
    # print(HT_cookies,HT_UserAgent)
    num = len(HT_cookies_list)
    for i in range (num):
        HT_cookies = HT_cookies_list[i]
        HT_UserAgent = HT_UserAgent_list[i]
        print(HT_cookies)
        print(HT_UserAgent)
        client,loggerinfo = get_infouser(HT_cookies, HT_UserAgent)

        # 如果不想做特定任务可以手动注释
        if client != False:
            loggerinfo = daySign_task(loggerinfo)  # 执行每日签到
            loggerinfo = daily_viewgoods(loggerinfo)  # 执行每日商品浏览任务
            loggerinfo = daily_sharegoods(loggerinfo)  # 执行每日商品分享任务
            loggerinfo = daily_viewpush(loggerinfo)  # 执行每日点推送任务
            loggerinfo = tiantianjifen_lottery(loggerinfo)  # 天天积分翻倍
            loggerinfo = zhuanjifen_task(loggerinfo)  # 我的-赚积分-转盘
            loggerinfo = vipdate_lottery(loggerinfo)  # 超级会员日转盘
            loggerinfo = zhinengshenghuo_lottery(loggerinfo)  # 智能生活-0元抽奖-宠粉转盘 可能此活动中奖率低！返回空白是正常
            loggerinfo = realme_lottery(loggerinfo)  # realme宠粉计划 转盘
            if zaoshui_open == 'true':
                loggerinfo = zaoshui_task(loggerinfo)
        sendmessage(loggerinfo)



# 主函数入口
if __name__ == '__main__':
    main("", "")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#从这里开始看。

#比一般教程的签到方法可以存活时间更长，一般半年没有问题（改密码也没事！），正常方法估计三天cookie就失效（二次签到可能会提前失效）~

#比一般教程多增加了，二次签到、观看60分钟、弹幕、赠送片等签到入口！！
#并不能帮你完成观看，弹幕任务，需要你自己手动完成任务，然后帮你签到。
#觉得自己看完、下载完片的记得自己点签到的，不要骂我程序没用，直接删了~

#改好了可以直接从import requests复制到腾讯云函数内使用！建议每天23点55分执行，省的忘记签看片60分钟等。

#腾讯视频签到用，会玩的直接看5、6、7步就好。

#需要准备的东西：1、cookie；2、auth_refresh链接；3、cookie去尾巴；4、自己的server酱（可有可无，微信通知你签到情况）。

#cookie、auth_refresh提取方式：
#1、谷歌浏览器打开https://v.qq.com；（我用的是360极速浏览器，讲道理google浏览器应该一样）
#2、登录自己的腾讯视频账号；
#3、按F12后Filter搜索框左侧选择all，搜索框输入auth，按F5刷新；
#4、点击name栏里的auth_refresh链接；

#5、general栏目里的Request UR，就是auth_refresh链接########################
#6、Request Headers栏目里的cookie就是你的cookie############################
#7、cookie删除“vqq_vusession=”以后的内容，就是你的”cookie去尾巴“#############

import requests
def start():
    login_headers = {
        'Referer': 'https://v.qq.com',
        'Cookie': 'pgv_pvi=8375384064; pgv_pvid=6144973719; eas_sid=01j6O0C2R6r8C7W9C778I1D387; RK=mcgRNPvyMo; ptcz=3fd69fcb96cdac1593bf75c9d8c4122d4ccb30e5fc549638d49fa23369ee3534; tvfe_boss_uuid=c5fb014505515437; video_guid=c4f474fc649f77bc; video_platform=2; o_cookie=874325546; Qs_lvt_323937=1610881585; Qs_pv_323937=2922750869489360000; pgg_appid=101503919; pgg_access_token=8469C48FA5D33E0D9C7E6988E70CB086; pgg_type=1; pgg_user_type=5; main_login=qq; vqq_access_token=BFA1ADC39987618D77E4C416E79EF16F; vqq_appid=101483052; vqq_openid=F24556CDCF0692236C7D4B0861AC9D3B; vqq_vuserid=202340045; vqq_refresh_token=1A2352A82912DC723071A01F0C9DEC7F; LW_uid=9156J2u0e8f0B6t2j7F082m2N6; LW_sid=V1O6U2K0f850j692C8F3V348D2; pgg_uid=309731937; pgg_openid=E924181B4AF03944FE4B37A5A55FD595; pac_uid=1_874325546; iip=0; ptui_loginuin=874325546; uin_cookie=o0874325546; ied_qq=o0874325546; luin=o0874325546; lskey=00010000cfec10397b2d9fde515aa49d7cb147dd539aef7dc6567202d47b0bd4364f58bd5aa1310c88a74e1a; vqq_vusession=59CPbLAHXOsbdOSGCxFusQ..; vqq_next_refresh_time=6600; vqq_login_time_init=1625539977; login_time_last=2021-7-6 10:52:57; uid=318381751; pgv_info=ssid=s4401000971'#1.这里把cookie替换成自己的cookie，别把引号删了！！
    }
    login = requests.get('https://access.video.qq.com/user/auth_refresh?type=qq&g_tk=83743011&g_vstk=367982652&g_actk=1799500784&raw=1&vappid=11059694&vsecret=fdf61a6be0aad57132bc5cdf78ac30145b6cd2c1470b0cfe',headers=login_headers)#2.这里把auth_refres换成自己的，别把引号删了！！
    cookie = requests.utils.dict_from_cookiejar(login.cookies)
    sign_headers = {
        'Cookie': 'pgv_pvi=8375384064; pgv_pvid=6144973719; eas_sid=01j6O0C2R6r8C7W9C778I1D387; RK=mcgRNPvyMo; ptcz=3fd69fcb96cdac1593bf75c9d8c4122d4ccb30e5fc549638d49fa23369ee3534; tvfe_boss_uuid=c5fb014505515437; video_guid=c4f474fc649f77bc; video_platform=2; o_cookie=874325546; Qs_lvt_323937=1610881585; Qs_pv_323937=2922750869489360000; pgg_appid=101503919; pgg_access_token=8469C48FA5D33E0D9C7E6988E70CB086; pgg_type=1; pgg_user_type=5; main_login=qq; vqq_access_token=BFA1ADC39987618D77E4C416E79EF16F; vqq_appid=101483052; vqq_openid=F24556CDCF0692236C7D4B0861AC9D3B; vqq_vuserid=202340045; vqq_refresh_token=1A2352A82912DC723071A01F0C9DEC7F; LW_uid=9156J2u0e8f0B6t2j7F082m2N6; LW_sid=V1O6U2K0f850j692C8F3V348D2; pgg_uid=309731937; pgg_openid=E924181B4AF03944FE4B37A5A55FD595; pac_uid=1_874325546; iip=0; ptui_loginuin=874325546; uin_cookie=o0874325546; ied_qq=o0874325546; luin=o0874325546; lskey=00010000cfec10397b2d9fde515aa49d7cb147dd539aef7dc6567202d47b0bd4364f58bd5aa1310c88a74e1a;'+cookie['vqq_vusession']+';'#这里把“cookie去尾巴”替换成自己的，别把引号删了！！
    }
    sign1 = requests.get('https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2',headers=sign_headers).text #1次签到接口
    sign1_1 = requests.get('http://v.qq.com/x/bu/mobile_checkin',headers=sign_headers).text #2次签到接口
    sign2 = requests.get('https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=1',headers=sign_headers).text #观看60分钟签到接口
    sign3 = requests.get('https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=3',headers=sign_headers).text #弹幕签到接口
    sign4 = requests.get('https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=6',headers=sign_headers).text #赠片签到接口
    sign5 = requests.get('https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=7',headers=sign_headers).text #下载签到接口
    if 'Account Verify Error' in sign1:
        print ('Sign error,Cookie Invalid')
        requests.get('https://sc.ftqq.com/SCU140264Tebe1b0ea383878be225f4ddda0d3970e5fe997235082d.send?text=%E8%85%BE%E8%AE%AF%E8%A7%86%E9%A2%91%E5%85%A8%E7%AD%BE%E5%88%B0Cookie%E5%A4%B1%E6%95%88&desp=%E8%BF%98%E6%9C%89%E7%A9%BA%E7%82%B9%E5%BC%80%E7%9C%8B%EF%BC%8CCookie%E5%A4%B1%E6%95%88%E4%BA%86%E8%BF%98%E4%B8%8D%E5%8E%BB%E6%9B%B4%E6%96%B0')#这里把“你自己的server酱”替换成你自己的
    else:
        print ('Sign Success')
        requests.get('https://sc.ftqq.com/SCU140264Tebe1b0ea383878be225f4ddda0d3970e5fe997235082d.send?text=%E6%81%AD%E5%96%9C%E6%81%AD%E5%96%9C%EF%BC%8C%E8%85%BE%E8%AE%AF%E8%A7%86%E9%A2%91%E5%85%A8%E9%83%A8%E7%AD%BE%E5%88%B0%E6%88%90%E5%8A%9F&desp=%E7%9B%B4%E6%8E%A5%E7%AD%BE%E5%88%B0%3A'+sign1[42:-14]+'%EF%BC%9B%E4%BA%8C%E6%AC%A1%E7%AD%BE%E5%88%B0%E5%AE%8C%E6%88%90'+'%EF%BC%9B%E8%A7%82%E7%9C%8B60%E5%88%86%E9%92%9F%3A'+sign2[42:-3]+'%EF%BC%9B%E5%BC%B9%E5%B9%95%3A'+sign3[42:-3]+'%EF%BC%9B%E8%B5%A0%E7%89%87%3A'+sign4[42:-3]+'%EF%BC%9B%E4%B8%8B%E8%BD%BD%3A'+sign5[42:-3]+'%E3%80%82')#这里把“你自己的server酱”替换成你自己的
def main_handler(event, context):
    return start()
if __name__ == '__main__':
    start()

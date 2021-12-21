import requests
import time
import random
import asyncio
import json
# CustomerList   参数 product 0 全部
# 1 HPV九价 2 HPV四价 3 HPV二价-进口 54 HPV二价-进口（国产）
# 详情接口  每个社区或者医院的详情接口
# https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx?act=CustomerProduct&id=5448&lat=34.21803249782986&lng=108.87995171440973

from _config import logger
from sendNotify import send
allMess = ''
def notify(content=None):
    global allMess
    allMess = allMess + content + '\n'
    logger.info(content)
def generate_random_str(randomlength):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

# duan ="--------------------------"
# def praserJsonFile(jsonData):
#     value = json.loads(jsonData)
#     rootlist = value.keys()
#     print rootlist
#     print duan
#     for rootkey in rootlist:
#         print rootkey
#     print duan
#     subvalue = value[rootkey]
#     print subvalue
#     print duan
#     for subkey in subvalue:
#         print subkey, subvalue[subkey]


def Code_0():
    # print('（1）开始获取医院列表')
    notify(f"任务:获取医院列表\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")
    # data_array = []
    numFlag = 0
    time.sleep(int_time)
    payload = {
        'act': 'CustomerList',
        'city': '["陕西省","西安市","雁塔区"]',
        'lat': '34.21803249782986',
        'lng': '108.87995171440973',
        "id": 0,
        'cityCode': 0,
        'product': 0,
    }
    code = requests.get(
        url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
        headers=headers, params=payload, verify=False)
    if int(code.status_code) == 200:
        code_json_list = code.json()
        notify(f"获取医院列表OK\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")
        # logger.info('医院列表获取成功')
        for l in code_json_list['list']:
            # print('地址:', l['addr'], '名字:', l['cname'], 'ID:', l['id'])
            # data_array.append(
            #       {
            #         'addr' :l['addr'],
            #         'cname' :l['cname'],
            #         'id':l['id'],
            #         'lat': l['lat'],
            #         'lng': l['lng'],
            #       }
            # )
            # print(data_array)
            # fp = open('a.json','w',encoding='utf-8')
            # json.dump(code_json_list,fp=fp,ensure_ascii=False)
            logger.info('===================start=========================')
            detail = requests.get(
                url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
                headers=headers, params={
                    'act': 'CustomerProduct',
                    'id': l['id'],
                    'lat': l['lat'],
                    'lng': l['lng'],
                }, verify=False)
            # print(detail.status_code)
            if int(detail.status_code) == 200:
                  # print(detail.json())
                  detailInfo = detail.json()
                  for n in detailInfo['list']:
                          notify(f"医院名称:{detailInfo['cname']}")
                          notify(f"按钮状态:{n['BtnLable']}")
                          notify(f"状态:{n['enable']}")
                          notify(f"数据:{n['date']}")
                          # logger.info('医院名称',detailInfo['cname'])
                          # logger.info('按钮状态',n['BtnLable'])
                          # logger.info('状态',n['enable'])
                          # logger.info('数据',n['date'])
                          logger.info('===================End=========================')
                          if(n['enable']==True):
                            numFlag=numFlag+1
            else:
                logger.info('详情请求失败')
    else:
        logger.info('医院列表请求失败')
    # logger.info('共',len(code_json_list['list']),'家医院','可预约',numFlag,)
    notify(f"共:{len(code_json_list['list'])}家医院,可预约{numFlag}")
    send('西安九价疫苗预约',allMess)
# def detailFun():
#     detail = requests.get(
#       url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
#       headers=headers, params={
#           'act': 'CustomerProduct',
#       }, verify=False)
#     if int(detail.status_code) == 200:
#         print(detail.json())
#     else:
#         print('请求失败')


def Code_1():
    print('（1）开始访问获取客户订阅日期详细信息:GetCustSubscribeDateDetail')
    time.sleep(int_time)
    payload = {
        'act': 'GetCustSubscribeDateDetail',
        'pid': p_id,
        'id': '243',
        'scdate': yuyue_times,
    }
    code = requests.get(
        url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
        headers=headers, params=payload, verify=False)
    # 转json
    if int(code.status_code) == 200:
        print(code, '33')
        # code_json_dict = code.json()
        print(code_json_dict)
        if int(code_json_dict['status']) == 200:
            if code_json_dict['list']:
                print(code_json_dict['list'][0]['mxid'])
                mxid = code_json_dict['list'][0]['mxid']
                check_mxid = False
                return check_mxid, mxid
            else:
                print('九价还没开放')
                check_mxid = True
                mxid = ''
                return check_mxid, mxid
        else:
            check_mxid = True
            mxid = ''
            return check_mxid, mxid
    else:
        print(code.status_code)
        check_mxid = True
        print('访问异常,继续访问')
        mxid = ''
        return check_mxid, mxid


def Code_2():
    # 获取验证码
    print('（2）访问验证码：GetCaptcha')
    time.sleep(int_time)
    payload = {
        'act': 'GetCaptcha',
    }
    code = requests.get(
        url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
        headers=headers, params=payload, verify=False)
    # 转json
    if int(code.status_code) == 200:
        ck_s = YanZheng302()
        return ck_s
    else:
        print('访问异常,继续访问%s' % code.status_code)
        ck_s = True
        return ck_s


def GetCustSubscribeDateDetail():
    print('访问获取客户订阅日期详细信息：GetCustSubscribeDateDetail')
    time.sleep(int_time)
    payload = {
        'act': 'GetCustSubscribeDateDetail',
        'pid': p_id,
        'id': '243',
        'scdate': yuyue_times,
    }
    code = requests.get(
        url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
        headers=headers, params=payload, verify=False)
    # 转json
    if int(code.status_code) == 200:
        code_json_dict = code.json()
        print(code_json_dict)
        if int(code_json_dict['status']) == 200:
            print(code_json_dict['list'][0]['mxid'])
            mxid = code_json_dict['list'][0]['mxid']
            check_mxid = False
            return check_mxid, mxid
        else:
            check_mxid = True
            mxid = ''
            return check_mxid, mxid
    else:
        print(code.status_code)
        check_mxid = True
        print('访问异常,继续访问')
        mxid = ''
        return check_mxid, mxid


def YanZheng302():
    print("（3）开始验证：CaptchaVerify")
    time.sleep(int_time)
    payload = {
        'act': 'CaptchaVerify',
        'token': '',
        'x': x,
        'y': '5',
    }
    code = requests.get(
        url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
        headers=headers, params=payload, verify=False)
    # 转json
    if int(code.status_code) == 200:
        code_json_dict = code.json()
        print(code_json_dict)
        if int(code_json_dict['status']) != 204 and int(code_json_dict['status']) != 201:
            if int(code_json_dict['status']) != 408:
                print('验证码-验证成功')
                print('guid:%s' % code_json_dict['guid'])
                guid = code_json_dict['guid']
                Checks = False
                # 成功后去访问Save20结果去提交数据=预约成功
                print('（4）马上提交')
                Save20(yuyue_times, p_id, mxid, guid)
                return Checks
            else:
                Checks = True
                print('请重新授权Cookies')
                return Checks
        else:
            Checks = True
            print('继续验证')
            return Checks


def Save20(times, p_id, mxid, guid):
    payload = {
        'act': 'Save20',
        'birthday': "1999-02-22",
        'tel': "电话",
        'sex': "2",  # 性别2 女  1 男
        'cname': "姓名",
        'doctype': "1",
        'idcard': "身份证",
        'mxid': mxid,
        'date': times,
        'pid': p_id,
        'Ftime': "1",
        'guid': guid,
    }
    print(payload)
    tongyong = requests.get(
        url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
        headers=headers, params=payload, verify=False)
    # 转json
    json_dict = tongyong.json()
    print(json_dict)
    if int(json_dict['status']) != 201:
        print(json_dict)
        print('预约成功')
    else:
        pass


if __name__ == '__main__':
    # 延迟时间
    int_time = 4
    # Cookies
    headers = {
        'Host': 'cloud.cn2030.com',
        'Connection': 'keep-alive',
        'Cookie': 'ASP.NET_SessionId=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2Mzk5ODIwMzIuMTg3NTAzOCwiZXhwIjoxNjM5OTg1NjMyLjE4NzUwMzgsInN1YiI6IllOVy5WSVAiLCJqdGkiOiIyMDIxMTIyMDAyMzM1MiIsInZhbCI6Ik1rTWdBUUlBQUFBUU5UWXhOamt5TWpSbE1HSTVNamhsWkJ4dmNYSTFielZCYlhwV1VqY3lVR0p1VW5CM1pYcHdXSFp4TWxnMEFCeHZcclxuVlRJMldIUXpZVll6T1ZSaFRYTjJhRnBsT1RkMmNGZHdPVUpORGpFeU15NHhNemt1T0RFdU1qRTRBQUFBQUFBQUFBPT0ifQ.YLopy35hoIcMB443RD9HxfMSAPo31s4kfw26aTsNwnw',
        'content-type': 'application/json',
        'zftsl': 'd674f8934077fa87eefbd10f92a2e484',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.15(0x18000f2e) NetType/4G Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx2c7f0f3c30d99445/91/page-frame.html',
    }
    requests.packages.urllib3.disable_warnings()
    # 猜测验证码的X
    x = '33'
    Checks = True
    Checks0 = True
    # 填写预约时间
    yuyue_times = '2021-07-24'
    # 1= 九价
    p_id = '12'
    Code_0()
    # while Checks0:
    #     Checks0, mxid = Code_0()
    # 获取订阅日期mxid
    # while Checks:
    # Checks, mxid = Code_1()

    # 获取验证码
    # Checks2 = True
    # while Checks2:
    #     Checks2 = Code_2()

    # 7Q90AC5oAABeYzQB = 26670

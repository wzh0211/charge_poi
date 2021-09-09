# -*- coding: utf-8 -*-
import io
import sys
import time
import pandas as pd
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')    # 设置打印编码


def addressToLocation_count(adcode):

    # key为在高德地图开发者平台（https://lbs.amap.com/）申请的wei api key，需要替换为自己的
    parameters = {
        'key': '  ',
        'types':'011100',   # 充电站标签
        'city':adcode,
        'citylimit':'true',
        'offsest':20,       # 每次返回的数据个数，根据高德文档，最多25个
        'page':1            # 返回第几页的数据，从1开始
    }
    base = 'https://restapi.amap.com/v3/place/text?'
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    contest = s.get(base,params=parameters, verify=False).json()
    # print(contest)  # 查看获取的页面数据
    count = int(contest['count'])
    print(count)
    if count != 0 :
        integer = count // 20
        remainder = count % 20
        print(integer,remainder)
        if remainder != 0 :
            integer = integer + 1
        integer = integer + 1
    else:
        integer = 0
    return integer

def addressToLocation_info(adcode,page):

    # key为在高德地图开发者平台（https://lbs.amap.com/）申请的wei api key，需要替换为自己的
    parameters = {
        'key': '  ',
        'types':'011100',
        'city':adcode,
        'citylimit':'true',
        'offsest':20,
        'page':page
    }
    base = 'https://restapi.amap.com/v3/place/text?'
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    contest = s.get(base,params=parameters, verify=False).json()
    print(contest)
    count = int(contest['count'])
    print(count)
    poi_list = contest['pois']
    print(len(poi_list))
    return poi_list

if __name__ == '__main__':

    '''
    根据高德给出的区域码adcode加工删除部分数据后的数据，原因是市辖区数据会和下属的区数据重复，且充电站大于800时（这个数不确定），获取的不全，只会显示800多，如获取北京市数据，返回800多条，肯定是不对的
    因此使用各个区的编码获取充电站数据，adcode_2即为去除了地级市、省份（表现为00结尾），市辖区（表现为01结尾），但是自治区自治县这些01要保留
    '''

    data_adcode = pd.read_csv('adcode/adcode_2.csv')
    adcode_list = data_adcode['adcode']


    result_name = []    # 名
    result_address = [] # 地址
    result_pname = []   # 省
    result_cname = []   # 市
    result_adname = []  # 区
    result_location = []    # poi
    k = 0
    for adcode in adcode_list:
        print("--------------- " + str(adcode) + ' ---------------')
        integer = addressToLocation_count(adcode)   # 先调用一次，无数据则跳过，此处高德接口每次返回的数据不一样，有一定的误差，大约在5%
        time.sleep(0.25)    # 请求太快会被封
        if integer > 1:     # 只要有数据，integer就从2开始
            for i in range(1,integer):
                poi_list = addressToLocation_info(adcode,i)
                time.sleep(0.25)    # 请求太快会被封
                for p in poi_list:
                    k = k+1
                    charge_poi_info = p
                    # 高德返回的数据不标准，有的竟然会缺失key，导致程序中断，因此加了判断，没有的数据填充------
                    if 'name' in charge_poi_info.keys():
                        charge_name = charge_poi_info['name']
                        if charge_name:
                            result_name.append(charge_name)
                        else:
                            result_name.append('------')
                    else:
                        result_name.append('------')
                    if 'address' in charge_poi_info.keys():
                        charge_address = charge_poi_info['address']
                        if charge_address:
                            result_address.append(charge_address)
                        else:
                            result_address.append('------')
                    else:
                        result_address.append('------')
                    if 'location' in charge_poi_info.keys():
                        charge_location = charge_poi_info['location']
                        if charge_location:
                            result_location.append(charge_location)
                        else:
                            result_location.append('------')
                    else:
                        result_location.append('------')
                    if 'pname' in charge_poi_info.keys():
                        charge_pname = charge_poi_info['pname']
                        if charge_pname:
                            result_pname.append(charge_pname)
                        else:
                            result_pname.append('------')
                    else:
                        result_pname.append('------')
                    if 'cityname' in charge_poi_info.keys():
                        charge_cname = charge_poi_info['cityname']
                        if charge_cname:
                            result_cname.append(charge_cname)
                        else:
                            result_cname.append('------')
                    else:
                        result_cname.append('------')
                    if 'adname' in charge_poi_info.keys():
                        charge_adname = charge_poi_info['adname']
                        if charge_adname:
                            result_adname.append(charge_adname)
                        else:
                            result_adname.append('------')
                    else:
                        result_adname.append('------')

            print(k)

    result = pd.DataFrame({'name': result_name, 'address': result_address,'pname':result_pname,'cname':result_cname,'adname':result_adname,
                           'location': result_location},
                          columns=['name', 'address', 'pname','cname','adname','location'])
    result_url  = 'charge_china_all.csv'
    result.to_csv(result_url, index=False, encoding='utf_8_sig')




















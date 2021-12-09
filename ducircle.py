import requests
import numpy as np
import pandas as pd
import time
import json
from pyecharts import options as opts
from pyecharts.charts import Geo


def getTime():
    return int(round(time.time() * 1000))


def getList(length):
    List = []
    for i in range(length):
        temp = js['returndata']['datanodes'][i]['data']['strdata']
        # 原网站有同比增长数据为空，若直接使用eval()会报错，需要先判断
        if (len(temp) != 0):
            # eval()数字转字符串
            List.append(eval(temp))
    return List

if __name__ == '__main__':
    # 请求目标网址(链接?前面的东西)
    url = 'https://data.stats.gov.cn/easyquery.htm'
    # 请求头，User-Agent: 用来证明你是浏览器，满足一定格式即可，不一定和自己的浏览器一样
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}  # 浏览器代理
    key = {}  # 参数键值对
    key['m'] = 'QueryData'
    key['dbcode'] = 'fsnd'
    key['rowcode'] = 'reg'
    key['colcode'] = 'sj'
    key['wds'] = '[{"wdcode":"zb","valuecode":"A0P0906"}]'
    key['dfwds'] = '[]'
    key['k1'] = str(getTime())
    # 禁用安全请求警告
    requests.packages.urllib3.disable_warnings()
    # 发出请求，使用post方法，这里使用前面自定义的头部和参数
    # ！！！verify=False，国家统计局20年下半年改用https协议,若不加该代码无法通过SSL验证
    r = requests.post(url, headers=headers, params=key, verify=False)
    # 使用json库中loads函数，将r.text字符串解析成dict字典格式存储于js中
    js = json.loads(r.text)
    # print(js)
    # 得到所需数据的一维数组，利用np.array().reshape()整理为二维数组
    length = len(js['returndata']['datanodes'])
    res = getList(length)
    # 总数据划分成31行的格式
    # print(res)
    array = np.array(res).reshape(31, 10)
    # np.array()转换成pd.DataFrame格式，后续可使用to_excel()直接写入excel表格

    df_overmarry = pd.DataFrame(array)
    # print(df_overmarry)
    df_overmarry.columns = ['2020年',
                            '2019年',
                            '2018年',
                            '2017年',
                            '2016年',
                            '2015年',
                            '2014年',
                            '2013年',
                            '2012年',
                            '2011年']
    # print(df_overmarry)
    for ind in df_overmarry.columns:
        # print(df_overmarry)
        # print(ind)
        arr = df_overmarry[""+ind+""]
        # print(ar)

        c = (
            Geo()
                .add_schema(maptype="china")
                .add("离婚登记数", [list(z) for z in zip(['北京',
        '天津',
        '河北',
        '山西',
        '内蒙古',
        '辽宁',
        '吉林',
        '黑龙江',
        '上海',
        '江苏',
        '浙江',
        '安徽',
        '福建',
        '江西',
        '山东',
        '河南',
        '湖北',
        '湖南',
        '广东',
        '广西',
        '海南',
        '重庆',
        '四川',
        '贵州',
        '云南',
        '西藏',
        '陕西',
        '甘肃',
        '青海',
        '宁夏',
        '新疆'],arr)])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(min_=0,
                                                  is_piecewise=True,  # 是否分段
                                                  # 自定义的每一段的范围，以及每一段的文字，以及每一段的特别的样式
                                                  pieces=[
                                                      {"min": 0, "max": 5, 'color': "#ffe7b2"},
                                                      {"min": 5, "max": 10, 'color': "#ffcea0"},
                                                      {"min": 10, "max": 15, 'color': "#ffa577"},
                                                      {"min": 15, "max": 20, 'color': "#ff6341"},
                                                      {"min": 20, "max": 25, 'color': "#ff2736"},
                                                      {"min": 25, 'color': "#de1f05"},
                                                  ]),
                title_opts=opts.TitleOpts(title=str(ind)+"全国各省离婚登记（万对）数据分布"),
            )
        )
        filepath = 'map/' +str(ind) + '全国各省离婚登记数据分布.html'
        c.render(path=filepath)

    # print(df_overmarry)




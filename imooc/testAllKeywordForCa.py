# -*-coding:utf-8 -*-
from urllib import request
import time
import _thread
from bs4 import BeautifulSoup as bs
import re

# "fm transmitter",
# "car bluetooth fm transmitter",
# "car fm transmitter bluetooth",
# "fm transmitter for car bluetooth",
# "fm transmitter for phone",
# "car bluetooth fm",
# "bluetooth usb transmitter",
# "fm transmitter charger",
# "fm transmitter car charger",
# "fm transmitter kit",
# "fm transmitter car kit",
# "car fm transmitter usb",
# "fm transmitter hands free",
# "bluetooth fm transmitter car kit"

# key_world_list = ["fm transmitter",
#     		"car bluetooth fm transmitter",
#     		"car fm transmitter bluetooth",
#     		"fm transmitter for car bluetooth",
#     		"fm transmitter for phone",
#     		"car bluetooth fm",
#     		"bluetooth usb transmitter",
#     		"fm transmitter charger",
#     		"fm transmitter car charger",
#     		"fm transmitter kit",
#     		"fm transmitter car kit",
#     		"car fm transmitter usb",
#     		"fm transmitter hands free",
#     		"bluetooth fm transmitter car kit"];
key_world_list = [
    "car mount",
    "cell phone car mount",
    "phone holder",
    "car phone mount",
    "holder for car",
    "car mount phone",
    "phone mount holder",
    "cell phone holder",
    "car mount holder",
    "phone mount",
    "cell phone mount",
    "car holder"
];
key_world_able_list = [
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
]


def init_url(url):
    req = request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
    req.add_header("Host", "www.amazon.ca")
    req.add_header("Accept-Language", "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4")
    req.add_header("Host", "www.amazon.ca")
    req.add_header("Upgrade-Insecure-Requests", "1")
    req.add_header("Connection", "keep-alive")
    req.add_header("Cache-Control", "max-age=0")

    resp = request.urlopen(req)
    htmlContentBuf = resp.read().decode('utf-8')
    return htmlContentBuf;


def searchKeyworld(nextUrl, page, key_world, key_world_inde, ):
    htmlContent = init_url(nextUrl)

    soup = bs(htmlContent, "html.parser")
    # li_list = soup.find_all('li', attrs={'class': 's-result-item  celwidget '})
    li_list = soup.find_all('li', attrs={'id': re.compile('result_')})
    for text in li_list:
        asin = text.get('data-asin')
        if asin == 'B0757M136J': # 支架
        # if asin == 'B0757M136J':
            position = li_list.index(text) + 1
            if position % 3 == 0:
                row_position = int(position / 3)
                list_position = 3
            else:
                row_position = int(position / 3) + 1
                list_position = position % 3
            if len(text.find_all(attrs={'class': "a-spacing-none a-color-tertiary a-text-normal"})) <= 0:
                # if len(text.find_all(attrs={'class' : 'a-declarative'})) <= 0:
                print(key_world + "搜索排名在第" + str(page) + "页" + "，第" + str(row_position) + "行" + ",第" + str(
                    list_position) + "个")
                key_world_able_list[key_world_inde] -= 1;
                break
            else:
                if key_world_able_list[key_world_inde] <= 0 :
                    break
                print(key_world + "广告在第" + str(page) + "页" + "，第" + str(row_position) + "行" + ",第" + str(
                    list_position) + "个")
                key_world_able_list[key_world_inde] -= 1;
                break


for key_world_str in key_world_list:

    print("正在搜索关键词：" + key_world_str)
    current_world_inde = key_world_list.index(key_world_str);
    # print(str(current_world_inde) + " : " + key_world_str)
    key_world_str = key_world_str.replace(" ", "+")
    base_url = "https://www.amazon.ca/s/ref=nb_sb_noss_2?url=search-alias%3Delectronics&field-keywords=" + key_world_str + "&rh=n%3A667823011%2Ck%3A" + key_world_str
    # base_url = "https://www.amazon.ca/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=" + key_world_str
    htmlContent = init_url(base_url)
    # getResult = htmlContent.find("Bluetooth FM Transmitter,[Newest Version]Etybetopstar T11 Car Transmitter Radio Adapter Car Kit with 4 Music Play Mode/Hands-Free Calling/1.44 Inch Screen Display/USB Car")

    # if getResult != -1:
    #     print("找到了，在第1页")

    _thread.start_new_thread(searchKeyworld, (base_url, 1, key_world_str, current_world_inde))

    index_start_string = htmlContent.find("/s/ref=sr_pg_2/")
    index_start = int(index_start_string)
    index_end_string = htmlContent.find("\"", index_start)
    index_end = int(index_end_string)
    pg2_undecode_url = htmlContent[index_start:index_end]
    pg2_undecode_url = pg2_undecode_url.replace(pg2_undecode_url[14: 34], "")

    for i in range(5):
        pg2_undecode_url = pg2_undecode_url.replace("&amp;", "&")

    for i in range(2, 20):
        # if the value is 0,then mean it fond 2 place of the key world, so dont need to do next anymore
        if key_world_able_list[current_world_inde] <= 0 :
            break
        nextUrl = "https://www.amazon.ca" + pg2_undecode_url.replace("/s/ref=sr_pg_2", "/s/ref=sr_pg_" + str(i))
        nextUrl = nextUrl.replace("page=2", "page=" + str(i))
        try:
            _thread.start_new_thread(searchKeyworld, (nextUrl, i, key_world_str, current_world_inde,))
        except:
            print("Error: 无法启动线程")
        time.sleep(1)
    time.sleep(1)

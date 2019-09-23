from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import pandas as pd
#表投欄位
c = ["名稱","地址","類別","車位坪數","土地坪數","建物坪數","主+陽坪數","房齡(年)","販賣樓層","總樓層","房(室)","廳","衛","價格","車位類型"]
df = pd.DataFrame(columns=c)
page = 1
first_title = ""
hjgtiu=1
while True:

    url = "https://buy.yungching.com.tw/region/%E4%BD%8F%E5%AE%85_p/%E5%8F%B0%E5%8C%97%E5%B8%82-_c/?pg=" + str(page)
    try:
        response = urlopen(url)
        print(response)
    except HTTPError:
        print("大概是最後一頁了")
        break
    html = BeautifulSoup(response, from_encoding="utf-8")
    restaurants = html.find_all("li", class_="m-list-item")
    i=0
    end = 0

    for r in restaurants:
        #進每一頁
        p = r.find("a","item-title")
        r_addr = "https://buy.yungching.com.tw" + p["href"]
        r1=urlopen(r_addr)
        html1 = BeautifulSoup(r1, from_encoding="utf-8")
        #抓車位類型,因這筆資料不是都有所以要寫判斷有就抓沒有填空值
        try:
            p = html1.find('section', class_='bg-car')
            p = p.find('ul', class_='detail-list-lv1')
            p = p.find('li', class_='left')
            abc = p.text
        except:
            abc=""
#我的最後一頁沒有停止點,所以寫抓到的標題如果重複即停止,if first_title == place.text: end = 1 break
        place = r.find("h3")
        name = place.text.split()
        if first_title == place.text:
            end = 1
            break
        if i==0:
            first_title = place.text
            i=i+1

        price = r.find("span", class_="price-num")
        price1 = price.text
        price2 = price1.replace(',', '')
        price3 = int(price2) * 10000 #把總價從字串轉整數後乘一萬
        counts = r.find_all("li")
        category = counts[0].text
        car = counts[8].text.replace("(含車位","").replace("坪","").replace(")","")#抓到的資料會有一些不想要的字,把字剃除
        earth = counts[3].text.replace("土地","").replace("坪","").replace("--","")
        build = counts[5].text.replace("建物","").replace("坪","")
        ma = counts[4].text.replace("主","").replace("+","").replace("陽","").replace("坪","").replace("平","").replace("露","")
        years = counts[1].text.replace("年","")
        sell = counts[2].text.replace("樓", "").split("/")[0]
        floors = counts[2].text.replace("樓","").split("/")[-1]
        room = counts[6].text.replace("房(室)", "").replace("廳", "").replace("衛", "")[2]
        room2 = counts[6].text.replace("房(室)", "").replace("廳", "").replace("衛", "")[3]
        room3 = counts[6].text.replace("房(室)", "").replace("廳", "").replace("衛", "")[4]
        #print(count)
        print("第{}頁，第{}筆.地點:".format(i,hjgtiu),place.text)
        #填入資料
        s = pd.Series([name[0],name[1], category,car,earth,build,ma,years,sell,floors,room,room2,room3,price3,abc],
                      index=c)
        df = df.append(s, ignore_index=True)
        hjgtiu += 1
    page = page + 1
    if end==1:
        break

df.to_csv("house.csv", encoding="utf-8", index=False)
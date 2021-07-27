from lxml import html
import requests
from datetime import datetime
from fake_headers import Headers


keys = ('title', 'date', 'link')
date_format = '%Y-%m-%dT%H:%M:%S%z'
header = Headers(headers=True).generate()
url_lenta = 'https://lenta.ru/'
url_mail = 'https://mail.ru/'
url_yandex = 'https://newssearch.yandex.ru/news/search?text=yandex-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8'

news_l = []
news_m = []

def news_lenta_ru():


    response = requests.get(url_lenta, headers=header)

    parsed = html.fromstring(response.text)
    parsed.make_links_absolute(url_lenta)

    news_links = parsed.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 | 
                                //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])
                                /a/@href''')
    print(news_links)
    news_text = parsed.xpath('''(//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 | 
                                //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"])
                                /a/text()''')
    print(news_text)

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')
        print(news_text[i])

    news_date = []

    for item in news_links:
        response = requests.get(item)
        parsed = html.fromstring(response.text)
        date = parsed.xpath('//time[@itemprop="datePublished"]/@datetime')
        news_date.extend(date)

    for i in range(len(news_date)):
        news_date[i] = datetime.strptime(news_date[i], date_format)
#        print(news_date[i])

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value
            print(news_dict[key])

        news_dict['source'] = 'lenta.ru'
        print(news_dict)
        news_l.append(news_dict)

    return news_l

lenta = news_lenta_ru()
print(lenta)

def news_mail_ru():


    request_m = requests.get(url_mail, headers=header)
    parsed = html.fromstring(request_m.text)

    news_links1 = parsed.xpath('''(//div[@class =  "news-item o-media news-item_media news-item_main"]  |  
                                //div[@class =  "news-item__inner"])
                                /a[contains(@href, "news.mail.ru")]/@href''')

    news_text1 = parsed.xpath('''(//div[@class =  "news-item o-media news-item_media news-item_main"]//h3  |  
                               //div[@class =  "news-item__inner"]/a[contains(@href, "news.mail.ru")])
                               /text()''')

    for i in range(len(news_text1)):
        news_text1[i] = news_text1[i].replace(u'\xa0', u' ')
        print(news_text1[i])

    news_links_temp = []
    for item in news_links1:
        item = item.split('/')
        news_links_temp.append('/'.join(item[0:5]))

    news_links_m = news_links_temp
    del (news_links_temp)

    news_date_m = []

    for item in news_links_m:
        request = requests.get(item, headers=header)
        root = html.fromstring(request.text)
        date = root.xpath('//span[@class="note__text breadcrumbs__text js-ago"]/@datetime')
        news_date_m.extend(date)

    for i in range(len(news_date_m)):
        news_date_m[i] = datetime.strptime(news_date_m[i], date_format)

    for item in list(zip(news_text1, news_date_m, news_links_m)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value

        news_dict['source'] = 'mail.ru'
        news_m.append(news_dict)

    return news_m

mail = news_mail_ru()
print(mail)

def news_yandex_ru():


    request_y = requests.get(url_yandex, headers=header)
    parsed = html.fromstring(request_y.text)


    news_links2 = parsed.xpath('//*[@id="neo-page"]/div/div[1]/div/div[1]/article[2]/div[1]/h1')
    print(news_links2)

    news_text2 = parsed.xpath('// *[ @ id = "neo-page"] / div / div[1] / div / div[1] / article[2] / div[2]')
    print(news_links2)

    for i in range(len(news_text2)):
        news_text2[i] = news_text2[i].replace(u'\xa0', u' ')
        print(news_text2[i])



#mail = news_mail_ru()
#print(mail)
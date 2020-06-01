import requests
from lxml import etree

def weather_info():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 '
        }

    # 天气信息
    try:
        tianqi_url = 'http://tianqi.2345.com/ninghe1d/60517.htm'
        tianqi_response = requests.get(tianqi_url, headers=headers)
        tianqi_response.encoding = tianqi_response.apparent_encoding
        # print(tianqi_response.text)
        tianqi_html = etree.HTML(tianqi_response.text)
        tianqi_data1=tianqi_html.xpath('//div[@class="real-today"]/span/text()')[0][3:]
        # print(tianqi_data1)
        tianqi_data2=tianqi_html.xpath('//ul[@class="real-data"]/li/span/text()')[0]
        # print(tianqi_data2)
        # tianqi_data3=tianqi_html.xpath('//div[@id="day7info"]/ul[1]/li[1]/i/text()')[0]
        # tianqi_data4=tianqi_html.xpath('//div[@id="day7info"]/ul[1]/li[1]/i/font/text()')[1]
        # tianqi_data5=tianqi_html.xpath('//div[@id="day7info"]/ul[1]/li[1]/i/text()')[2].strip()

        tianqi_str = '【天气信息】' + '\n' + tianqi_data1 + '\n' + tianqi_data2
        print(tianqi_str)
        
    except:
        tianqi_str = '【天气信息】' + '\n' + '***没有获取到数据***'
        print(tianqi_str)
    return tianqi_str
if __name__=="__main__":
    weather_info()
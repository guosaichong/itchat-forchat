import requests
from lxml import etree

def get_data(keyword):
    data_list=[]
    url = "http://www.youdao.com/w/eng/{}/".format(keyword)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}
    try:
        r = requests.get(url,headers=headers)
        HTML = etree.HTML(r.text)
        word = HTML.xpath('//*[@id="phrsListTab"]/h2/span/text()')[0]
        IPA = HTML.xpath('//*[@id="phrsListTab"]/h2/div/span[1]/span/text()')[0]
        paraphrase = HTML.xpath('//*[@id="phrsListTab"]/div[2]/ul//text()')
        if HTML.xpath('//*[@id="phrsListTab"]/div[2]/ul/following-sibling::p[1]'):
            other = HTML.xpath('//*[@id="phrsListTab"]/div[2]/ul/following-sibling::p[1]/text()')[0][1:-2]
        else:
            other=""
        example_sentence1 = HTML.xpath('//*[@id="bilingual"]/ul/li[1]/p[1]')[0]
        example_sentence2 = HTML.xpath('//*[@id="bilingual"]/ul/li[1]/p[2]//text()')
        example_sentence1=etree.tostring(example_sentence1,method = "text").decode()
        # example_sentence=example_sentence1+str(example_sentence2)
        # print(word)
        # print(IPA)
        # print(paraphrase)
        istr=""
        for i in paraphrase:
            istr += i
        # print(istr.strip())
        # print(example_sentence1)
        # print(example_sentence2)
        example_sentence2_str=''
        for i in example_sentence2:
            example_sentence2_str  += i
        # print(example_sentence2_str.strip())
        # print(other.strip())
        data_list.extend([word.strip(),IPA.strip(),istr.strip(),example_sentence1.strip(),example_sentence2_str.strip(),other.strip()])
        # print(data_list)
        # print(len(data_list))
        return data_list
    except Exception as e:
        return e
if __name__=="__main__":
    get_data("reco")
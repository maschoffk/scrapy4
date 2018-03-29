import scrapy

class BlogSpider(scrapy.Spider):
    name = 'adidasspider'
    start_urls = ['http://shop.adidas.com.sg/catalogsearch/result/index/?limit=120&p=1']

    def parse(self, response):
        hxs = scrapy.selector.HtmlXPathSelector(response)
        title = hxs.select('//*[@id="top"]/body/div[1]/div/div[3]/div[1]/div[2]/div[2]/div/div')
        for title in title:
            id = title.select('//*[@id="loadhere"]/ul').extract()
            print(id)
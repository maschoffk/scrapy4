import scrapy
from scrapy.crawler import CrawlerProcess
from adidas.items import AdidasItem
import requests
import csv
import pandas

class AdidasSpider(scrapy.Spider):
    name = 'adidas'
    allowed_domains = ['adidas.com.sg']
    start_urls = ['http://shop.adidas.com.sg/catalogsearch/result/index/?limit=120']
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'adidas3.csv'
    }
    def parse(self, response):
        soup = response.xpath("//*[@class='product-info-wrapper']")
        for prod in soup:
            item = AdidasItem()
            item['name'] = prod.xpath('a/@title').extract_first()
            item['id'] = prod.xpath('a/@id').extract_first()
            item['price'] = prod.xpath('div[@class="price-box"]/p/span/@pricerounded').extract_first()
            item['discounted_price'] = prod.xpath('div[@class="price-box"]/p[@class="special-price"]/span/@pricerounded').extract_first()
            yield item

        nextPageLinkSelect = response.xpath('//div[@class="prevnextbuttons"]/a[2]/@href')
        if nextPageLinkSelect:
            nextPageLink = nextPageLinkSelect.extract_first()
            print(nextPageLink)
            yield scrapy.Request(url=nextPageLink, callback=self.parse)



process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})

process.crawl(AdidasSpider)
process.start()


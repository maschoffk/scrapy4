import scrapy
from adidas.items import AdidasItem
import requests
import csv
import pandas

class BlogSpider(scrapy.Spider):
    name = 'adidas'
    allowed_domains = ['adidas.com.sg']
    start_urls = ['http://shop.adidas.com.sg/catalogsearch/result/index/?limit=120']

    def parse(self, response):
        soup = response.xpath("//*[@class='product-info-wrapper']")
        for prod in soup:
            item = AdidasItem()
            item['name'] = prod.xpath('a/@title').extract()
            item['id'] = prod.xpath('a/@id').extract()
            yield item
            
        nextPageLinkSelect = response.xpath('//div[@class="prevnextbuttons"]/a[2]/@href')
        if nextPageLinkSelect:
            nextPageLink = nextPageLinkSelect.extract_first()
            print(nextPageLink)
            yield scrapy.Request(url=nextPageLink, callback=self.parse)
        



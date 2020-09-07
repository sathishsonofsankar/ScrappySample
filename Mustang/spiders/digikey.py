import scrapy


class DigikeySpider(scrapy.Spider):
    name = 'digikey'
    allowed_domains = ['digikey.com']
    start_urls = ['https://www.digikey.com/products/en']
    

    def parse(self, response):
        components = response.xpath("//a[@class='catfilterlink']/@href")
        baseurl='https://www.digikey.com/'
        for link in components:
            requestUrl = baseurl+link.extract()+'?&page=1&pageSize=500'
            #print(requestUrl)
            yield scrapy.Request(url=requestUrl,callback=self.parseproducts)
            #partHref = categoryResponse.xpath("//tbody[@id='lnkPart']/*/td[@class='tr-dkPartNumber nowrap-culture']/a/@href")
            #partUrl = baseurl + partHref
            #print(partUrl)

        #digikeyPartno = response.xpath("//td[contains(@id,'reportPartNumber')]/text()[2]")
        #availableStock= response.xpath("//span[contains(@id,'dkQty')]/text()")
        #manPartno = response.xpath("//table[@id='product-overview']/tbody/tr[3]/td/text()[1]")
        #print(manPartno)
    
    def parseproducts(self,response):
        baseurl1='https://www.digikey.com/'
        partHrefs = response.xpath("//tbody[@id='lnkPart']/*/td[@class='tr-dkPartNumber nowrap-culture']/a/@href")
        for link in partHrefs:
            partDetailUrl =baseurl1 + link.extract()
            yield scrapy.Request(url=partDetailUrl,callback=self.retrievePartDetails)
            #print(partDetailUrl)

    def retrievePartDetails(self,response):
        print('URL:' + response.request.url)
        stock=response.xpath("//span[contains(@id,'dkQty')]/text()").get()
        yield {
           'partUrl' : response.request.url,
           'Stock Quantity': stock
        }
        #baseurl1='https://www.digikey.com/'
        #partUrl = baseurl1 + partHref
        


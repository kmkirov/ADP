# -*- coding: utf-8 -*-
import datetime as dt
import scrapy
import re


class ElectricityVolumesPolandSpider(scrapy.Spider):
    name = 'price-poland'

    def __init__(self, date='2018-01-01'):
        self.date = dt.date(*map(int, date.split('-', 3)))

    def start_requests(self):
        yield scrapy.Request(
            'https://wyniki.tge.pl/en/wyniki/euroindex/spot/?date=%s'
            % self.date
        )

    def parse(self, response):
        allPrices = response.css("#tabbed > table.t-02")
        
        datesListSelecteor = allPrices.css("thead tr td")
        datesList = list()
        for item in datesListSelecteor:
            p = item.css('span.date::text')
            datesList.append(p.get())
            # single date 1 - 7
        
        allSinglePrice = allPrices.css('tbody')
        spl = allPrices.css('tbody tr.prices') 
        splElems = spl[0].css('td span.wrap')
        priceList = list()
        for elem in splElems:
            item = elem.css('span.wrap::text').get()
            if not re.search('[a-zA-Z] ', item): #filter words and space
                priceList.append(float(item))            
        
        allSingleVolumes = allPrices.css('tbody')
        splVol = allSingleVolumes.css('tbody tr.volumes') 
        volElems = splVol[0].css('td span.wrap')
        volList = list()
        for elem in volElems:
            itemVol = elem.css('span.wrap::text').get()
            if not re.search('[a-zA-Z] ', itemVol): #filter words and space
                volList.append(float(itemVol))
                        
        for iterNum in range(0,6):
            yield dict(country='pl', indicator='volume',
                       period='day', datetime=datesList[iterNum],
                       value=volElems[iterNum], price = priceList[iterNum])
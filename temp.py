
import scrapy
import json


class Spider(scrapy.Spider):
    name = 'spider'
    
    start_urls = ['https://www.kinopoisk.ru/s/type/film/list/1/m_act[country]/2/m_act[genre][0]/8/']

    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        results = response.css('div.element')
        for i, result in enumerate(results):
            name = result.css('p.name').css('a::text').get()
            year = result.css('p.name').css('span.year::text').get()
            duration = result.css('div.info').css('span.gray')[0].css('::text').get()
            country = result.css('div.info').css('span.gray')[1].css('::text').get().split('<')[0]
            author = result.css('div.info').css('span.gray')[1].css('a::text').get()
            yield {i: {'name': name, 'year': year, 'duration': duration,
                       'country': country, 'author': author}}
    
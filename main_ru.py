import subprocess
import json
import configparser
from settings import genres, countries


if __name__ == '__main__':
    print('Loading filters......')

    with open('filters_ru', 'r', encoding='UTF-8') as file:
        row_text = ''.join([x for x in file.read()])
    input_countries = row_text.split('\n')[0].split()
    output_countries: list = []
    for country in input_countries:
        if country in countries:
            output_countries.append(countries[country])
        else:
            print(f'Country with name {country} does not founded. skipped')

    input_genres = row_text.split('\n')[1].split()
    output_genres = []
    for genre in input_genres:
        if genre in genres:
            output_genres.append(genres[genre])
        else:
            print(f'Genre with name {genre} does not founded. skipped')

    print('Loaded...............')
    print('Link generation......')

    link_base = 'https://www.kinopoisk.ru/s/type/film/list/1/'
    link = link_base
    for i in output_countries:
        link += f'm_act[country]/{i}/'

    if not len(output_genres):
        link += f'm_act[genre][0]/0/'

    for i, genre in enumerate(output_genres):
        link += f'm_act[genre][{i}]/{genre}/'

    base_first = """
import scrapy
import json


class Spider(scrapy.Spider):
    name = 'spider'
    """
    base_middleware = "    start_urls = ['{link}']".format(link=link)
    base_second = """
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
    """
    with open('temp.py', 'w') as file:
        file.write(base_first + '\n' + base_middleware + '\n' + base_second)

    print('OK...................')
    with open('data.json', 'w') as _:
        # Need to clear data file.
        pass
    subprocess.run('scrapy runspider temp.py --output=data.json -L WARNING')
    print('..............SUCCESS')

    with open('data.json') as file:
        data = json.load(file)

    for i in data:
        print(i)

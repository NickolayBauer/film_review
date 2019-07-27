# Импорт необходимых модулей
import bs4
import requests
import re
import unicodedata

'''
Испольмая функция:
need_dict - сбор данных о фильме со стороннего сайта.
Формальный параметр:
link - ссылка на фильм.
Используемые переменные:
agent - содержит данные, необходимые для маккировки под браузер;
s - объект запроса;
b - объект сбора данных;
table - содержит таблицу с данными;
box_office - кассовые сборы;
bufget - бюджет фильма;
year - год выпуска фильма;
genres - жанры фильма;
directors - режиссёры фильма;
elem - элемент таблицы;
i - индекс элемента таблицы;
'''

def need_dict(link):
    agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    s = requests.get(link, headers=agent)
    b = bs4.BeautifulSoup(s.text, "html.parser")

    table = b.select(".info td")
    box_office = budget = year = genres = directors = None
    for i, elem in enumerate(table):
        if elem.getText() == "год":
            year = table[i + 1].a.getText()
        if elem.getText() == "жанр":
            genres = [elem.getText() for elem in table[i + 1].select("a") if elem.getText() != "..." and elem.getText() != "слова"]
        if elem.getText() == "режиссер":
            directors = [elem.getText() for elem in table[i + 1].select("a") if elem.getText() != "..." and elem.getText() != "слова"]
        if elem.getText() == "сборы в мире":
            box_office = re.findall(r'=\s(.+)', unicodedata.normalize("NFKD", table[i + 1].select("a")[0].getText()))[0]
        if elem.getText() == "бюджет":
            if table[i + 1].select("a"):
                budget = unicodedata.normalize("NFKD", table[i + 1].select("a")[0].getText())
            else:
                budget = unicodedata.normalize("NFKD", table[i + 1].select("div")[0].getText())

    return {
        "title": b.select("h1.moviename-big")[0].getText(),
        "img": b.select(".popupBigImage img")[0].attrs["src"],
        "box_office": box_office,
        "budget": budget,
        "year": year,
        "description": unicodedata.normalize("NFKD", b.select(".brand_words.film-synopsys")[0].getText()),
        "rating": b.select(".rating_ball")[0].getText(),
        "genres": genres,
        "actors": [elem.getText() for elem in b.select("#actorList ul li")[:3]],
        "directors": directors
    }

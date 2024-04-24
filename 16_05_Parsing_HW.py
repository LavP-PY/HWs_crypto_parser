# Домашнее задание по теме "Парсинг сайтов"
# Цель задания:
#
# Реализовать парсер на реальном примере, закрепив знания по теме.
#
# Задание:
#
# Один из работников Urban'a огромный фанат криптовалюты и всё что с ней связано.
# Говорят, он готов продать целый Эфир лишь за то, чтобы у него была небольшая программка,
# которая поможет ему распределять финансы между криптовалютами входящими в топ-100 капитализации.
#
# Самые актуальные данные по криптовалютам можно найти на CoinMarketCap. https://coinmarketcap.com/ru/
# На домашней странице этого сайта и находится топ-100 всех криптовалют.
#
# Так должна выглядеть таблица из которой будете брать данные:
# ....
# ....
# ....
# Как можно заметить здесь нет процента от общей капитализации топ-100 криптовалют.
#
# Техническое задание:
# Программа должна считывать данные с сайта CoinMarketCap.
# Для парсинга и запросов разрешено использовать любую из перечисленных библиотек: requests, selenium, beautifulsoup, scrapy.
# Ваш код должен выполнять следующий функционал:
# Считывать данные с сайта: название криптовалюты, текущая рыночная капитализация

import time
import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from datetime import datetime
import locale


url = 'https://coinmarketcap.com/ru/'
driver = webdriver.Chrome()
driver.get(url)
SCROLL_PAUSE_TIME = 2

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # прокручиваем до низа
    driver.execute_script("window.scrollBy(0, window.innerHeight)")
    # ждём
    time.sleep(SCROLL_PAUSE_TIME)
    # расчитываем высоту новой прокрутки, сравниваем с высотой последней прокрутки
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

response = driver.page_source

soup = BeautifulSoup(response, features='html.parser')
table = soup.find('tbody')
rows_name = table.find_all('p', {'class': 'sc-4984dd93-0 kKpPOn'})
rows_capitalization = table.find_all('span', {'class': 'sc-7bc56c81-1 bCdPBp'})

rating_start = 0
rating = []
coins_name = []
market_capitalization = []
for name, values in zip(rows_name, rows_capitalization):
    rating_start += 1
    rating.append(rating_start)
    coins_name.append(name.text)
    clean_value = re.sub(r'[^\w\s]', '', values.text)
    market_capitalization.append(int(clean_value))


data = {'Rating': rating, 'Name': coins_name, 'MC': market_capitalization}
frame = pd.DataFrame(data)

frame['MD, %'] = round(100 * frame['MC']/frame['MC'].sum(), 2)

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
for i in frame['MC']:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    j = locale._format('%d', i, grouping=True)
    frame['MC'].replace(i, j, inplace=True) #



print(frame)

files_name = datetime.today().strftime("%H.%M %d.%m.%Y")
frame.to_csv(f'{files_name}.csv', sep=' ', index=False)

# Записывать данные в CSV файл в следующем порядке: название криптовалюты, текущая рыночная капитализация, процент от общей капитализации топ-100 криптовалют.
# 4.Процент одной криптовалюты должен рассчитывать по первым 100 криптовалютам на странице.
# 5.Разделитель между столбцами в CSV файле - пробелы.
# 6.Каждый следующий файл при записи должен иметь название в следующем формате: H.M dd.mm.yyyy, где H - Часы, M-минуты, dd- день, mm-месяц, yyyy-год.
#
# Запись в CSV файл должна быть в следующем формате (цифры случайны):
# ....
# ....
# ....
# Name - название криптовалюты
# MC - market capitalization (рыночная капитализация)
# MP - Market percentage (процент рынка)
#
# Примечания:
# Лучше реализовать эту программу в виде функции, например, назвав её write_cmc_top.
# Данные, получившиеся у вас
# Пришлите ссылку на репозиторий GitHub со следующими файлами:
# Файл с основной функцией
# CSV Файлы с записями в разные дни (мин. 2)
#
# Помните, что веткой по умолчанию (default) должна быть выбрана та, где находятся необходимые файлы.
#
# Успеха!

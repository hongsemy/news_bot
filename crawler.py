import requests
from bs4 import BeautifulSoup
import pprint

webpage = requests.get('https://www.utoronto.ca/news')
soup = BeautifulSoup(webpage.content, 'html.parser')

page = soup.find('div', attrs={'id': 'block-system-main'})

contents = page.find_all('div', attrs={'class': 'view-content'})

news_chunk = contents[1]

# print(news_chunk.prettify())


news_urls = []
news_titles = []
news = news_chunk.find_all('a')

for anchor in news:
    urls = 'https://www.utoronto.ca' + anchor['href']
    news_urls.append(urls)
pprint.pprint(news_urls)

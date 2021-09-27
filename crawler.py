import requests
from bs4 import BeautifulSoup
import pprint
import copy
from typing import List

# ===================== Template ========================
NEWS_TEMPLATE = {
    'title': '',
    'url': '',
    'thumbnail': '',
    'date': ''
}

# ================== Private Functions ==================
def _crawl_main_page(url: str):
    """ Crawl main page to get information container.
    
    Params
        url: A URL of webpage to crawl
    Return
        A tag object that contains every contents of the website
    """
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    container = soup.find('div', attrs={'id': 'block-system-main'})
    return container


def _crawl_list_page(container):
    """ Crawl list page to get news content wrapper. 

    Parmas
        container: A tag object that contains every contents of a ceratin website
    Return
        A tag object that contains every latest news
    """
    view_content = container.find_all('div', attrs={'class': 'view-content'})
    if len(view_content) < 2:
        return []
    else:
        all_news = view_content[1]
        return all_news


def _crawl_each_news(all_news) -> List[dict]:
    urls = _get_urls(all_news)
    titles = _get_titles(all_news)
    dates = _get_dates(all_news)
    thumbnails = _get_thumbnails(all_news)
    lst_news = []
    for i in range(len(urls)):
        news = copy.deepcopy(NEWS_TEMPLATE)
        news['url'] = urls[i]
        news['title'] = titles[i]
        news['thumbnail'] = thumbnails[i]
        news['date'] = dates[i]
        lst_news.append(news)
    
    return lst_news


def _get_urls(all_news):
    news_urls = []
    for anchor in all_news.find_all('a'):
        url = 'https://www.utoronto.ca' + anchor['href']
        news_urls.append(url)
    
    return news_urls


def _get_titles(all_news):
    news_titles = []
    for title in all_news.find_all('div', {'class': 'title'}):
        news_titles.append(title.get_text().strip())

    return news_titles


def _get_thumbnails(all_news):
    news_thumbnails = []
    for picture in all_news.find_all('div', {'class': 'picture'}):
        thumbnail = picture.find('img')['src']
        news_thumbnails.append(thumbnail)
    
    return news_thumbnails


def _get_dates(all_news):
    news_dates = []
    for date in all_news.find_all('div', {'class': 'date'}):
        news_dates.append(date.get_text().strip())

    return news_dates


def main():
    container = _crawl_main_page('https://www.utoronto.ca/news')
    all_news = _crawl_list_page(container)
    news_lst = _crawl_each_news(all_news)
    
    for i in range(len(news_lst)):
        print(i)
        for key in news_lst[i]:
            print(key + ": " + news_lst[i][key])
        print()


if __name__ == '__main__':
    main()

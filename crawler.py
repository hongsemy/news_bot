import requests
from bs4 import BeautifulSoup
import pprint
import copy
from typing import List
import bot as bot_handler

# ===================== Templates ========================

NEWS_TEMPLATE = {
    'title': '',
    'url': '',
    'thumbnail': '',
    'date': ''
}

# ================== Private Functions ===================

def _crawl_main_page(url: str):
    """ Crawl main page to get information container.
    
    Params
        url: A URL of webpage to crawl
    Return
        A tag object that contains every contents of the website
    """
    try:
        webpage = requests.get(url)
        if webpage.status_code != 200:
            webpage.raise_for_status()
        soup = BeautifulSoup(webpage.content, 'html.parser')
        container = soup.find('div', attrs={'id': 'block-system-main'})
        return container
    except requests.exceptions.HTTPError as e:
        print(e) 
        # TODO: Should be replaced with proper exception handling method
    except AttributeError as ae:
        print(ae) 
        # TODO: Should be replaced with proper exception handling method


def _crawl_list_page(container):
    """ Crawl list page to get news content wrapper. 

    Parmas
        container: A tag object that contains every contents of a
        uoft news website
    Return
        A tag object that contains every latest news
    """
    try:
        view_content = container.find_all('div',
                                          attrs={'class': 'view-content'})
        if len(view_content) < 2:
            print('News chunk missing...')
            # TODO: Should be replaced with proper exception handling method
            return None
        else:
            all_news = view_content[1]
            return all_news
    except AttributeError as ae:
        print(ae)
        # TODO: Should be replaced with proper exception handling method


def _crawl_each_news(all_news) -> List[dict]:
    """ Crawl information in each news uploaded on a uoft news website. 

    Parmas
        all_news: A tag object that contains every latest news of a
        uoft news website
    Return
        A tag object that contains every latest news
    """
    lst_news = []
    for news_home in all_news.find_all('div', attrs={'class': 'news-home'}):
        news = copy.deepcopy(NEWS_TEMPLATE)
        _get_url(news_home, news)
        _get_title(news_home, news)
        _get_date(news_home, news)
        _get_thumbnail(news_home, news)
        lst_news.append(news)
    return lst_news


def _get_url(news_home, news: dict) -> None:
    """ Crawl URL of a news that news_home object represents.
    
    Params
        news_home: A tag object that contains information about a
        single news.
        news: A dictionary that information of a single news will
        be stored
    """
    try:
        anchor = news_home.find('a')
        url = 'https://www.utoronto.ca' + anchor['href']
        news['url'] = url
    except KeyError as ke:
        print(ke)
        print('Anchor is None.')
        news['url'] = 'URL MISSING'
        # TODO: Should be replaced with proper exception handling method


def _get_title(news_home, news: dict) -> None:
    """ Crawl title of a news that news_home object represents.
    
    Params
        news_home: A tag object that contains information about a
        single news.
        news: A dictionary that information of a single news will
        be stored
    """
    try:
        title = news_home.find('div', {'class': 'title'})
        news_title = title.get_text().strip()
        news['title'] = news_title
    except AttributeError as ae:
        print(ae)
        print('Title is None.')
        news['title'] = 'TITLE MISSING'
        # TODO: Should be replaced with proper exception handling method


def _get_thumbnail(news_home, news: dict) -> None:
    """ Crawl thumbnail of a news that news_home object represents.
    
    Params
        news_home: A tag object that contains information about a
        single news.
        news: A dictionary that information of a single news will
        be stored
    """
    try:
        picture = news_home.find('div', {'class': 'picture'})
        thumbnail = picture.find('img')['src']
        news['thumbnail'] = thumbnail
    except KeyError as ke:
        print(ke)
        print('Thumbnail is None.')
        news['thumbnail'] = 'THUMBNAIL MISSING'
        # TODO: Should be replaced with proper exception handling method


def _get_date(news_home, news: dict) -> None:
    """ Crawl date of a news that news_home object represents.
    
    Params
        news_home: A tag object that contains information about a
        single news.
        news: A dictionary that information of a single news will
        be stored
    """
    try:
        date = news_home.find('div', {'class': 'date'})
        news['date'] = date.get_text().strip()
    except AttributeError as ae:
        print(ae)
        print('Date is None.')
        news['date'] = 'DATE MISSING'
        # TODO: Should be replaced with proper exception handling method


# ==================== Public Functions ====================

def main() -> None:
    """ Main Function """
    container = _crawl_main_page('https://www.utoronto.ca/news')
    all_news = _crawl_list_page(container)
    news_lst = _crawl_each_news(all_news)
    bot = bot_handler.create_bot()
    for news in news_lst:
        caption = '"' + news['title'] + '"' + '\n\n' \
                  + news['date'] + '\n\n' + news['url']
        bot_handler.send_photo(bot, news['thumbnail'], caption)


if __name__ == '__main__':
    main()

import requests
from bs4 import BeautifulSoup
import copy
from typing import List
import bot as bot_handler
import csv
import schedule
import time
import logging

# ===================== Templates ========================

NEWS_TEMPLATE = {
    'title': '',
    'url': '',
    'thumbnail': '',
    'date': ''
}

logger = logging.getLogger('uoft')
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(message)s")
console = logging.StreamHandler()
file_handler = logging.FileHandler("C:/Users/bcd/Desktop/bunchofcrawlers/news_bot/uoft.log")
console.setLevel(logging.INFO)
file_handler.setLevel(logging.WARNING)
console.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console)
logger.addHandler(file_handler)

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
        raise Exception(str(e) + ": " + url)
    except AttributeError as ae:
        raise Exception(str(ae) + ": " + url)


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
        raise Exception(str(ae) + \
                     ": Either html format has changed or request went wrong.")


def _crawl_each_news(all_news) -> List[dict]:
    """ Crawl information in each news uploaded on a uoft news website. 

    Parmas
        all_news: A tag object that contains every latest news of a
        uoft news website
    Return
        A tag object that contains every latest news
    """
    lst_news = []
    i = 1
    for news_home in all_news.find_all('div', attrs={'class': 'news-home'}):
        news = copy.deepcopy(NEWS_TEMPLATE)
        try:
            _get_url(news_home, news)
        except Exception as e:
            message = "#" + str(i) + ": " + str(e)
            bot_handler.report_error(bot_handler.create_error_reporter(),
                                     message)
            logger.warning(message)
        try:
            _get_title(news_home, news)
        except Exception as e:
            message = "#" + str(i) + ": " + str(e)
            bot_handler.report_error(bot_handler.create_error_reporter(),
                                     message)
            logger.warning(message)
        try:
            _get_date(news_home, news)
        except Exception as e:
            message = "#" + str(i) + ": " + str(e)
            bot_handler.report_error(bot_handler.create_error_reporter(),
                                     message)
            logger.warning(message)
        try:
            _get_thumbnail(news_home, news)
        except Exception as e:
            message = "#" + str(i) + ": " + str(e)
            bot_handler.report_error(bot_handler.create_error_reporter(),
                                     message)
            logger.warning(message)
        i += 1
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
        news['url'] = 'URL MISSING'
        raise Exception('Anchor is None. ')
    except AttributeError as ae:
        news['url'] = 'URL MISSING'
        raise Exception('Anchor is None. ')


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
        news['title'] = 'TITLE MISSING'
        raise Exception('Title is None. ')


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
        news['thumbnail'] = 'THUMBNAIL MISSING'
        raise Exception('Thumbnail is None. ')
    except AttributeError as ae:
        news['thumbnail'] = 'THUMBNAIL MISSING'
        raise Exception('Thumbnail is None. ')


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
        news['date'] = 'DATE MISSING'
        raise Exception('Date is None')


def _write_csv_file(lst_of_news: List[dict], location: str) -> None:
    """ Write crawled information to a csv file located at specified
    location
    
    Params
        lst_of_news: A list that contains dictionaries that each
        represents a single news
        location: Location where a csv file will be saved
    """
    labels = []
    for keys in lst_of_news[0]:
        labels.append(keys)

    with open(location, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames = labels)
        writer.writeheader()
        for elem in lst_of_news:
            writer.writerow(elem)


def _read_csv_file(location: str) -> List[dict]:
    """ Read from a csv file located at specified location and save
    information as a list of dictionaries where each dictionaries
    refers to each row in a csv file.
    
    Params
        location: Location where a csv file is located
    Return
        A list that contains dictionaries that each represents
        a single row in a csv file
    """
    news_lst = []
    with open(location, mode='r', encoding='UTF8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            news_lst.append(row)
    
    return news_lst


def _compare_news(new: List[dict], old: List[dict]) -> int:
    """ Read from a csv file located at specified location and save
    information as a list of dictionaries where each dictionaries
    refers to each row in a csv file.
    
    Params
        new: A list of news crawled from the current cycle 
        old: A list of news crawled from the previous cycle
    Return
        An integer that represents the number of news updates
    """
    count = 0
    for news in new:
        if news['title'] == old[0]['title'] \
                                and news['thumbnail'] == old[0]['thumbnail'] \
                                and news['date'] == old[0]['date'] \
                                and news['url'] == old[0]['url']:
            return count
        else:
            count += 1    
    
    return count


# ==================== Public Functions ====================

def main() -> None:
    """ Main Function """
    reporter = bot_handler.create_error_reporter()
    bot_handler.report_error(reporter, "NOTIFICATION: STARTING LATEST NEWS UPDATE...")
    try:
        container = _crawl_main_page('https://www.utoronto.ca/news')
    except Exception as e:
        logger.warning(str(e))
        bot_handler.report_error(reporter, str(e))
        return
    try:
        all_news = _crawl_list_page(container)
    except Exception as e:
        logger.warning(str(e))
        bot_handler.report_error(reporter, str(e))
        return
    if all_news is not None:
        news_lst = _crawl_each_news(all_news)
    else:
        news_lst = []
    old_news = _read_csv_file(
                    'C:/Users/bcd/desktop/bunchofcrawlers/news_bot/news.csv')
    num_updates = _compare_news(news_lst, old_news)
    bot = bot_handler.create_bot()
    for i in range(num_updates):
        caption = '"' + news_lst[i]['title'] + '"' + '\n\n' \
                  + news_lst[i]['date'] + '\n\n' + news_lst[i]['url']
        try:
            bot_handler.send_photo(bot, news_lst[i]['thumbnail'], caption)
        except Exception as e:
            message = "(Sending messsage failed.) #" + str(i) + ": " + str(e)
            logger.warning(message)
            bot_handler.report_error(reporter, message)
    if len(news_lst) != 0:
        _write_csv_file(news_lst,
                    'C:/Users/bcd/desktop/bunchofcrawlers/news_bot/news.csv')
    else:
        message = 'ERROR: No news has been found.'
        logger.warning(message)
        bot_handler.report_error(reporter, message)
    bot_handler.report_error(reporter, "NOTIFICATION: FINISHED ONE CYCLE")


if __name__ == '__main__':
    main()

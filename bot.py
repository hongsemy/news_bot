import telegram
import crawler

# =================== Global Variables ===================
TOKEN = '1956707809:AAF7QQ2c6Wrcxy-iemmcF-zhF7cLzFjTIIg'
CHAT_ID = '@uoft_news_bot_channel'


# =================== Public Functions ===================
def create_bot():
    """ Creates a bot with telegram module. 
    
    Return
        A telegram bot created with a bot token.
    """
    bot = telegram.Bot(token=TOKEN)
    return bot


def send_message(bot, message: str) -> None:
    """ Makes a bot to send message to a uoft news channel.
    
    Params
        bot: A bot that sends a message
        message: A text chunk that a bot needs to send
    """
    bot.send_message(chat_id=CHAT_ID, text=message)

def send_photo(bot, img_url: str, caption: str) -> None:
    bot.sendPhoto(chat_id=CHAT_ID, photo=img_url, caption=caption)

if __name__ == '__main__':
    info = {
        'title': 'Higher levels of organic pollutants found in homes located near natural gas wells: U of T study',
        'url': 'https://www.utoronto.ca/news/higher-levels-organic-pollutants-found-homes-located-near-natural-gas-wells-u-t-study',
        'thumbnail': 'https://www.utoronto.ca/sites/default/files/styles/750x500/public/GettyImages-130904081-crop.jpg?itok=H6IvhXFR',
        'date': 'September 23'  
    }

    bot = create_bot()
    caption = '"' + info['title'] + '"' + '\n\n' + info['date'] + '\n\n' + info['url']
    send_photo(bot, info['url'], caption)

from logging import error
import telegram

# =================== Global Variables ===================
CHAT_ID = '@uoft_news_bot_channel'
CHAT_ID_ERROR = '@error_report_uoft'

TOKEN = '1956707809:AAF7QQ2c6Wrcxy-iemmcF-zhF7cLzFjTIIg'
TOKEN_ERROR ='2010994162:AAEADgLnnMHg0BptC6udzHghWKP4aKn7IYc'

# =================== Public Functions ===================
def create_bot():
    """ Creates a bot with telegram module. 
    
    Return
        A telegram bot created with a bot token.
    """
    bot = telegram.Bot(token=TOKEN)
    return bot

def create_error_reporter():
    """ Creates a bot with telegram module for error reporting.
    
    Return
        A telegram bot created with a bot token that will report error
        privately.
    """
    bot = telegram.Bot(token=TOKEN_ERROR)
    return bot

def send_message(bot, message: str) -> None:
    """ Makes a bot to send message to a uoft news channel.
    
    Params
        bot: A bot that sends a message
        message: A text chunk that a bot needs to send
    """
    bot.send_message(chat_id=CHAT_ID, text=message)

def report_error(reporter, error_message: str) -> None:
    """ Makes an error_reporter to send message to a error reporting
    channel.
    
    Params
        reporter: A bot that sends a message
        error_message: A text chunk that a bot needs to send
    """
    reporter.send_message(chat_id=CHAT_ID_ERROR, text=error_message)


def send_photo(bot, img_url: str, caption: str) -> None:
    """ Makes a bot to send photo messge to a uoft news channel.
    
    Params
        bot: A bot that sends a photo message
        img_url: An URL to an image that a bot needs to send
        caption: A text chunk that a bot needs to send
    """
    bot.sendPhoto(chat_id=CHAT_ID, photo=img_url, caption=caption)

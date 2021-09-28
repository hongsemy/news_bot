import telegram

# =================== Global Variables ===================
CHAT_ID = '@uoft_news_bot_channel'
TOKEN = '1956707809:AAF7QQ2c6Wrcxy-iemmcF-zhF7cLzFjTIIg'


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
    """ Makes a bot to send photo messge to a uoft news channel.
    
    Params
        bot: A bot that sends a photo message
        img_url: An URL to an image that a bot needs to send
        caption: A text chunk that a bot needs to send
    """
    bot.sendPhoto(chat_id=CHAT_ID, photo=img_url, caption=caption)

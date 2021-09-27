import telegram

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

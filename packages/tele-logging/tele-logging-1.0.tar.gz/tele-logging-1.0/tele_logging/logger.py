from tele_logging.bot import Bot
import os


def send(token, text='test'):
    bot = Bot(token)
    bot.send_message(text=text)

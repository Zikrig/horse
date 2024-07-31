from aiogram import Bot, Dispatcher
from environs import Env

# def load_token(path):
#     env = Env()
#     env.read_env(path)
#     return env('TOKEN')

def load_token(path):
    f = open(path, 'r')
    r = f.read()
    f.close()
    return r

bot = Bot(token=load_token('env'))
dp = Dispatcher()

async def send_notification(id, text):
    await bot.send_message(chat_id=id, text=text, parse_mode='html')

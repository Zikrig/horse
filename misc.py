from aiogram import Bot, Dispatcher
from environs import Env
 

def load_config(path):
#     pgsdata = {
#     'dbname':"postgres",
#     'user':"postgres",
#     'password':'12345',
#     'host': 'localhost',
# #     'user':"root",
# #     'password':'bU9oR9zU7g',
#     'port':"5432"
# }
    env = Env()
    env.read_env(path)
    return {
        'token': env('TOKEN'),
        'dbname': env('DB_NAME'),
        'user': env('DB_USER'),
        'password': env('DB_PASSWORD'),
        'host': env('DB_HOST'),
        'port': env('DB_PORT')
        }
    


config = load_config('.env')
# print(config)

bot = Bot(token=config['token'])
dp = Dispatcher()

async def send_notification(id, text):
    await bot.send_message(chat_id=id, text=text, parse_mode='html')

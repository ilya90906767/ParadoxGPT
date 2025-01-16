import os 
from dotenv import load_dotenv
import time
from datetime import datetime
from telethon.sync import TelegramClient
from .parse import get_news_channels

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
client = TelegramClient('session_name', api_id, api_hash)

def main():
    client.start()
    print('Running main function')
    while True:
        print('Cycle')
        get_news_channels(client)
        print(f"Last update: {datetime.now().isoformat()}")
        time.sleep(120)



# import os 
# from dotenv import load_dotenv
# import time
# from datetime import datetime
# from telethon import TelegramClient
# from .parse import get_news_channels

# load_dotenv()
# api_id = os.getenv('api_id')
# api_hash = os.getenv('api_hash')
# client = TelegramClient('session_name', api_id, api_hash)
# phone_number = os.getenv('phone_number')

# def main():
#     client.start(phone=phone_number)
#     two_fa_code = input("Enter your 2FA code: ")
#     client.sign_in(code=two_fa_code)
#     while True:
#         get_news_channels(client)
#         print(f"Last update: {datetime.now().isoformat()}")
#         time.sleep(120)
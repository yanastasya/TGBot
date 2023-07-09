import os

from dotenv import load_dotenv

load_dotenv()

admins_chats_status: dict = {
    os.getenv('ADMINS_CHAT_1'): 'free',
    os.getenv('ADMINS_CHAT_2'): 'free'
}

users_dict: dict[int, dict[str, str | int | bool]] = {}

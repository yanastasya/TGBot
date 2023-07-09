import os

from aiogram.filters import BaseFilter
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()


class IsFromAdminsChat(BaseFilter):
    """Фильтр пропускает(=True) апдэйты, пришедшие
    из чата админов.
    """
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "group"


class AnswerForUser(BaseFilter):
    """Фильтр пропускает(=True) апдэйты, содержащие
    в себе сообщения - ответы админов пользователю.
    """
    async def __call__(self, message: Message) -> bool:
        if message.reply_to_message is not None:
            return (
                message.reply_to_message.from_user.id == (
                    int(os.getenv('BOT_ID'))
                )
            )
        else:
            return False

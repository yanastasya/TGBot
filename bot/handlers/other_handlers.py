from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router: Router = Router()


@router.message()
async def other_question(message: Message, state: FSMContext):
    print(message.json(indent=4, exclude_none=True))
    print(await state.get_data())
    await message.answer('')

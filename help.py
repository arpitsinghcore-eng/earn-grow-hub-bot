from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(F.text == "❓ Help")
async def show_help(message: types.Message):
    b = InlineKeyboardBuilder()
    b.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_home"))
    await message.answer("Need Help?\nContact Support: @savagearpit", reply_markup=b.as_markup())

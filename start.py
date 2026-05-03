from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject
from database import db
from utils.generator import generate_user_id
from keyboards.menu import main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, command: CommandObject):
    tg_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    user = db.get_user(tg_id)
    if not user:
        inviter_id = None
        args = command.args
        if args and args.isdigit():
            inviter_id = str(args)
        
        user_id = generate_user_id()
        db.add_user(tg_id, user_id, username, inviter_id)
        user = db.get_user(tg_id)

    if user["is_banned"]:
        return await message.answer("You are banned from using this bot.")

    curr = db.get_setting("currency")
    text = (
        "Welcome to Earn Grow Hub Bot 🎉\n\n"
        f"Your ID: {user['user_id']}\n"
        f"Balance: {curr}{user['balance']:.2f}\n\n"
        "Use menu below."
    )
    await message.answer(text, reply_markup=main_menu())

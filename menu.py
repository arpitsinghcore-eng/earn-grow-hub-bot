from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def main_menu():
    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="💰 Balance"), types.KeyboardButton(text="📝 Tasks"))
    kb.row(types.KeyboardButton(text="❓ Help"))
    return kb.as_markup(resize_keyboard=True)

def balance_markup():
    b = InlineKeyboardBuilder()
    b.row(types.InlineKeyboardButton(text="💸 Withdraw", callback_data="withdraw"))
    b.row(types.InlineKeyboardButton(text="📜 History", callback_data="history"))
    b.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_home"))
    return b.as_markup()

def withdraw_markup():
    b = InlineKeyboardBuilder()
    b.row(types.InlineKeyboardButton(text="🆔 UPI ID", callback_data="wd_upi"),
          types.InlineKeyboardButton(text="🖼️ QR Code", callback_data="wd_qr"))
    b.row(types.InlineKeyboardButton(text="🏦 Bank Transfer", callback_data="wd_bank"))
    b.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_balance"))
    return b.as_markup()

def tasks_markup():
    b = InlineKeyboardBuilder()
    b.row(types.InlineKeyboardButton(text="📧 Gmail Work", callback_data="task_gmail"))
    b.row(types.InlineKeyboardButton(text="⭐ Review Work", callback_data="task_review"))
    b.row(types.InlineKeyboardButton(text="👥 Refer & Earn", callback_data="task_refer"))
    b.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_home"))
    return b.as_markup()

def gmail_action_markup(task_id):
    b = InlineKeyboardBuilder()
    b.row(types.InlineKeyboardButton(text="✅ Complete Task", callback_data=f"gmail_done_{task_id}"))
    b.row(types.InlineKeyboardButton(text="❌ Cancel", callback_data="task_gmail"))
    return b.as_markup()

def review_action_markup(task_id):
    b = InlineKeyboardBuilder()
    b.row(types.InlineKeyboardButton(text="📤 Submit Screenshot", callback_data=f"review_done_{task_id}"))
    b.row(types.InlineKeyboardButton(text="❌ Cancel", callback_data="task_review"))
    return b.as_markup()

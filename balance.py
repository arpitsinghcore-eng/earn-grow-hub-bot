from aiogram import Router, types, F
from database import db
from keyboards.menu import balance_markup

router = Router()

@router.message(F.text == "💰 Balance")
async def show_balance(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user or user["is_banned"]: return
    
    curr = db.get_setting("currency")
    await message.answer(f"Your Balance / आपका बैलेंस: {curr}{user['balance']:.2f}", reply_markup=balance_markup())

@router.callback_query(F.data == "history")
async def show_history(callback: types.CallbackQuery):
    db.cursor.execute("SELECT amount, type, created_at FROM transactions WHERE tg_id = ? ORDER BY id DESC LIMIT 5", (callback.from_user.id,))
    txs = db.cursor.fetchall()
    
    if not txs:
         return await callback.answer("No recent transactions.", show_alert=True)
         
    curr = db.get_setting("currency")
    text = "Recent Transactions:\n\n"
    for tx in txs:
         text += f"[{tx[2]}] {tx[1].upper()}: {curr}{tx[0]}\n"
         
    await callback.message.edit_text(text, reply_markup=balance_markup())

@router.callback_query(F.data == "back_balance")
async def back_to_balance(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    curr = db.get_setting("currency")
    await callback.message.edit_text(f"Your Balance / आपका बैलेंस: {curr}{user['balance']:.2f}", reply_markup=balance_markup())

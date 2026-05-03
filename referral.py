from aiogram import Router, types, F
from database import db
from keyboards.menu import tasks_markup

router = Router()

@router.callback_query(F.data == "task_refer")
async def refer_earn(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    bot_info = await callback.bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={user['user_id']}"
    
    curr = db.get_setting("currency")
    reward = db.get_setting("ref_reward")
    
    db.cursor.execute("SELECT COUNT(*) FROM users WHERE inviter_id = ?", (user['user_id'],))
    ref_count = db.cursor.fetchone()[0]
    
    text = (
        "👥 Refer & Earn\n\n"
        f"Your Referral Link:\n`{ref_link}`\n\n"
        f"Reward: {curr}{reward} per active user.\n"
        f"Note: You get reward ONLY when they complete their first task.\n\n"
        f"Total Referrals: {ref_count}"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=tasks_markup())

def process_referral_reward(tg_id):
    user = db.get_user(tg_id)
    if user and user['inviter_id'] and not user['first_task_done']:
        # Give reward to inviter
        inviter_id_str = str(user['inviter_id'])
        db.cursor.execute("SELECT tg_id FROM users WHERE user_id = ?", (inviter_id_str,))
        inviter = db.cursor.fetchone()
        
        if inviter:
            reward = float(db.get_setting("ref_reward"))
            db.update_balance(inviter[0], reward)
            
        db.cursor.execute("UPDATE users SET first_task_done = 1 WHERE tg_id = ?", (tg_id,))
        db.conn.commit()

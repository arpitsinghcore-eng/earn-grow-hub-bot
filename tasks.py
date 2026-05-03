from aiogram import Router, types, F
from database import db
from keyboards.menu import tasks_markup, gmail_action_markup, review_action_markup

router = Router()

@router.message(F.text == "📝 Tasks")
async def show_tasks(message: types.Message):
    await message.answer("Select task type / टास्क प्रकार चुनें:", reply_markup=tasks_markup())

@router.callback_query(F.data == "task_gmail")
async def task_gmail(callback: types.CallbackQuery):
    tg_id = callback.from_user.id
    
    # Free up expired pending tasks (e.g., > 15 mins)
    db.cursor.execute("UPDATE gmail_tasks SET status = 'available', assigned_to = NULL, assigned_at = NULL WHERE status = 'assigned' AND assigned_at < datetime('now', '-15 minutes')")
    db.conn.commit()

    db.cursor.execute("SELECT id, email, password, reward, instructions FROM gmail_tasks WHERE assigned_to = ? AND status = 'assigned'", (tg_id,))
    task = db.cursor.fetchone()
    
    if not task:
        db.cursor.execute("SELECT id, email, password, reward, instructions FROM gmail_tasks WHERE status = 'available' LIMIT 1")
        task = db.cursor.fetchone()
        if not task:
            return await callback.answer("No Gmail tasks available currently.", show_alert=True)
            
        db.cursor.execute("UPDATE gmail_tasks SET status = 'assigned', assigned_to = ?, assigned_at = datetime('now') WHERE id = ?", (tg_id, task[0]))
        db.conn.commit()

    curr = db.get_setting("currency")
    text = (
        f"📧 Gmail Work\n\n"
        f"Email: {task[1]}\n"
        f"Password: {task[2]}\n"
        f"Reward: {curr}{task[3]}\n\n"
        f"Instructions: {task[4]}\n\n"
        "Click 'Complete Task' and upload screenshot proof."
    )
    await callback.message.edit_text(text, reply_markup=gmail_action_markup(task[0]))

@router.callback_query(F.data == "task_review")
async def task_review(callback: types.CallbackQuery):
    db.cursor.execute("SELECT id, link, place_name, required_stars, reward FROM review_tasks WHERE status = 'active' LIMIT 1")
    task = db.cursor.fetchone()
    
    if not task:
         return await callback.answer("No Review tasks available currently.", show_alert=True)
         
    curr = db.get_setting("currency")
    text = (
        f"⭐ Review Work\n\n"
        f"Review Link: {task[1]}\n"
        f"Place/App: {task[2]}\n"
        f"Stars Required: {task[3]}⭐\n"
        f"Reward: {curr}{task[4]}\n\n"
        "Click 'Submit Screenshot' and upload your review proof."
    )
    await callback.message.edit_text(text, reply_markup=review_action_markup(task[0]))

@router.callback_query(F.data.startswith("gmail_done_"))
async def gmail_done(callback: types.CallbackQuery):
    task_id = callback.data.split("_")[2]
    db.set_state(callback.from_user.id, "AWAITING_GMAIL_PROOF", {"task_id": task_id})
    await callback.message.answer("Please send the screenshot proof for Gmail task:")

@router.callback_query(F.data.startswith("review_done_"))
async def review_done(callback: types.CallbackQuery):
    task_id = callback.data.split("_")[2]
    db.set_state(callback.from_user.id, "AWAITING_REVIEW_PROOF", {"task_id": task_id})
    await callback.message.answer("Please send the screenshot proof for Review task:")

@router.callback_query(F.data == "back_tasks")
async def back_to_tasks(callback: types.CallbackQuery):
    await callback.message.edit_text("Select task type / टास्क प्रकार चुनें:", reply_markup=tasks_markup())

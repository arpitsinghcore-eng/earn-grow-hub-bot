import asyncio
import logging
import json
import os

from aiogram import Bot, Dispatcher, types, F

from config import TOKEN, ADMIN_ID
from database import db

# root files imports
import start
import balance
import tasks
import withdraw
import help
import admin
import referral

from menu import main_menu
from generator import generate_gmail
from verify import (
    get_image_hash,
    verify_gmail_screenshot,
    verify_review_screenshot
)

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # routers
    dp.include_router(start.router)
    dp.include_router(balance.router)
    dp.include_router(tasks.router)
    dp.include_router(withdraw.router)
    dp.include_router(referral.router)
    dp.include_router(help.router)
    dp.include_router(admin.router)

    @dp.callback_query(F.data == "back_home")
    async def back_home(callback: types.CallbackQuery):
        user = db.get_user(callback.from_user.id)
        curr = db.get_setting("currency")

        text = (
            "Welcome to Earn Grow Hub Bot 🎉\n\n"
            f"Your ID: {user['user_id']}\n"
            f"Balance: {curr}{user['balance']:.2f}\n\n"
            "Use menu below."
        )

        try:
            await callback.message.delete()
        except:
            pass

        await callback.message.answer(
            text,
            reply_markup=main_menu()
        )

    @dp.message(F.photo)
    async def handle_photo(message: types.Message):
        user = db.get_user(message.from_user.id)

        if not user or not user["state"]:
            return

        state = user["state"]
        data = json.loads(user["state_data"]) if user["state_data"] else {}

        # withdraw QR proof
        if state == "AWAITING_WD_DETAILS" and data.get("method") == "QR":
            file_id = message.photo[-1].file_id
            data["details"] = file_id

            db.set_state(
                message.from_user.id,
                "AWAITING_WD_AMOUNT",
                data
            )

            await message.answer(
                "Enter amount to withdraw / निकालने की राशि दर्ज करें:"
            )
            return

        # task proofs
        if state.startswith("AWAITING_") and "PROOF" in state:
            file_id = message.photo[-1].file_id
            file_info = await bot.get_file(file_id)

            os.makedirs("downloads", exist_ok=True)
            file_path = f"downloads/{file_id}.jpg"

            await bot.download_file(file_info.file_path, file_path)

            img_hash = get_image_hash(file_path)

            db.cursor.execute(
                "SELECT id FROM submissions WHERE image_hash=?",
                (img_hash,)
            )

            if db.cursor.fetchone():
                db.set_state(message.from_user.id, None)
                await message.answer(
                    "Duplicate screenshot detected! Rejected."
                )
                return

            task_id = data.get("task_id")
            auto_verify = int(db.get_setting("auto_verify")) == 1

            # Gmail task
            if state == "AWAITING_GMAIL_PROOF":
                db.cursor.execute(
                    """
                    SELECT email, reward, assigned_to
                    FROM gmail_tasks
                    WHERE id=?
                    """,
                    (task_id,)
                )

                t_data = db.cursor.fetchone()

                if not t_data:
                    return

                email, reward, assigned_to = t_data

                if assigned_to != message.from_user.id:
                    db.set_state(message.from_user.id, None)

                    await message.answer(
                        "Task expired and reassigned."
                    )
                    return

                db.cursor.execute(
                    """
                    INSERT INTO submissions
                    (tg_id, task_type, task_id, image_hash)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        message.from_user.id,
                        "gmail",
                        task_id,
                        img_hash
                    )
                )

                if auto_verify:
                    is_valid, msg = verify_gmail_screenshot(
                        file_path,
                        email
                    )

                    if is_valid:
                        db.update_balance(
                            message.from_user.id,
                            reward
                        )

                        db.cursor.execute(
                            """
                            UPDATE gmail_tasks
                            SET status='completed'
                            WHERE id=?
                            """,
                            (task_id,)
                        )

                        db.cursor.execute(
                            """
                            UPDATE submissions
                            SET status='approved'
                            WHERE image_hash=?
                            """,
                            (img_hash,)
                        )

                        referral.process_referral_reward(
                            message.from_user.id
                        )

                        await message.answer(
                            f"Task Auto Approved ✅ Reward added: "
                            f"{db.get_setting('currency')}{reward}"
                        )

                    else:
                        db.cursor.execute(
                            """
                            UPDATE gmail_tasks
                            SET status='available',
                            assigned_to=NULL
                            WHERE id=?
                            """,
                            (task_id,)
                        )

                        db.cursor.execute(
                            """
                            UPDATE submissions
                            SET status='rejected'
                            WHERE image_hash=?
                            """,
                            (img_hash,)
                        )

                        await message.answer(
                            f"Task Rejected ❌\nReason: {msg}"
                        )

                else:
                    await message.answer(
                        "Screenshot sent for manual verification."
                    )

                    await bot.send_photo(
                        ADMIN_ID,
                        file_id,
                        caption=(
                            f"Gmail Proof\n"
                            f"User: {message.from_user.id}\n"
                            f"Task ID: {task_id}"
                        )
                    )

            # Review task
            elif state == "AWAITING_REVIEW_PROOF":
                db.cursor.execute(
                    """
                    SELECT place_name, keywords, reward
                    FROM review_tasks
                    WHERE id=?
                    """,
                    (task_id,)
                )

                t_data = db.cursor.fetchone()

                if not t_data:
                    return

                place_name, keywords, reward = t_data

                db.cursor.execute(
                    """
                    INSERT INTO submissions
                    (tg_id, task_type, task_id, image_hash)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        message.from_user.id,
                        "review",
                        task_id,
                        img_hash
                    )
                )

                if auto_verify:
                    is_valid, msg = verify_review_screenshot(
                        file_path,
                        place_name,
                        keywords
                    )

                    if is_valid:
                        db.update_balance(
                            message.from_user.id,
                            reward
                        )

                        db.cursor.execute(
                            """
                            UPDATE submissions
                            SET status='approved'
                            WHERE image_hash=?
                            """,
                            (img_hash,)
                        )

                        referral.process_referral_reward(
                            message.from_user.id
                        )

                        await message.answer(
                            f"Task Auto Approved ✅ Reward added: "
                            f"{db.get_setting('currency')}{reward}"
                        )

                    else:
                        db.cursor.execute(
                            """
                            UPDATE submissions
                            SET status='rejected'
                            WHERE image_hash=?
                            """,
                            (img_hash,)
                        )

                        await message.answer(
                            f"Task Rejected ❌\nReason: {msg}"
                        )

                else:
                    await message.answer(
                        "Screenshot sent for manual verification."
                    )

                    await bot.send_photo(
                        ADMIN_ID,
                        file_id,
                        caption=(
                            f"Review Proof\n"
                            f"User: {message.from_user.id}\n"
                            f"Task ID: {task_id}"
                        )
                    )

            db.conn.commit()
            db.set_state(message.from_user.id, None)

            try:
                os.remove(file_path)
            except:
                pass

    @dp.message()
    async def handle_text(message: types.Message):
        user = db.get_user(message.from_user.id)

        if not user or not user["state"]:
            return

        state = user["state"]
        data = json.loads(user["state_data"]) if user["state_data"] else {}

        # withdraw details
        if state == "AWAITING_WD_DETAILS":
            data["details"] = message.text

            db.set_state(
                message.from_user.id,
                "AWAITING_WD_AMOUNT",
                data
            )

            await message.answer(
                "Enter amount to withdraw / निकालने की राशि दर्ज करें:"
            )

        elif state == "AWAITING_WD_AMOUNT":
            try:
                amount = float(message.text)
                min_wd = float(db.get_setting("min_withdraw"))

                if amount < min_wd:
                    await message.answer(
                        f"Minimum withdraw is {min_wd}"
                    )
                    return

                if amount > user["balance"]:
                    await message.answer(
                        "Insufficient balance!"
                    )
                    return

                db.cursor.execute(
                    """
                    INSERT INTO withdraws
                    (tg_id, amount, method, details)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        message.from_user.id,
                        amount,
                        data["method"],
                        data["details"]
                    )
                )

                db.conn.commit()
                db.set_state(message.from_user.id, None)

                await message.answer(
                    "Withdrawal request submitted!"
                )

                await bot.send_message(
                    ADMIN_ID,
                    f"New WD Request: {amount}"
                )

            except:
                await message.answer("Invalid amount.")

        # admin panel text states
        elif message.from_user.id == ADMIN_ID:

            if state == "ADM_GMAIL_QTY":
                data["qty"] = int(message.text)

                db.set_state(
                    ADMIN_ID,
                    "ADM_GMAIL_REWARD",
                    data
                )

                await message.answer(
                    "Enter reward amount:"
                )

            elif state == "ADM_GMAIL_REWARD":
                data["reward"] = float(message.text)

                db.set_state(
                    ADMIN_ID,
                    "ADM_GMAIL_PWD",
                    data
                )

                await message.answer(
                    "Enter password:"
                )

            elif state == "ADM_GMAIL_PWD":
                data["pwd"] = message.text

                db.set_state(
                    ADMIN_ID,
                    "ADM_GMAIL_INST",
                    data
                )

                await message.answer(
                    "Enter instructions:"
                )

            elif state == "ADM_GMAIL_INST":
                qty = data["qty"]
                reward = data["reward"]
                pwd = data["pwd"]
                inst = message.text

                emails = generate_gmail(qty)

                for email in emails:
                    db.cursor.execute(
                        """
                        INSERT INTO gmail_tasks
                        (email, password, reward, instructions)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            email,
                            pwd,
                            reward,
                            inst
                        )
                    )

                db.conn.commit()
                db.set_state(ADMIN_ID, None)

                await message.answer(
                    f"Added {qty} Gmail tasks!"
                )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

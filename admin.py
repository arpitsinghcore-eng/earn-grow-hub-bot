from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_markup():
    b = InlineKeyboardBuilder()
    b.add(
        types.InlineKeyboardButton(text="📊 Dashboard", callback_data="adm_dash"),
        types.InlineKeyboardButton(text="👥 Users", callback_data="adm_users"),
        types.InlineKeyboardButton(text="🗂 Tasks Manager", callback_data="adm_tasks"),
        types.InlineKeyboardButton(text="💸 Withdraw Req", callback_data="adm_wd"),
        types.InlineKeyboardButton(text="⭐ Review Proofs", callback_data="adm_proof_rev"),
        types.InlineKeyboardButton(text="📧 Gmail Proofs", callback_data="adm_proof_gml"),
        types.InlineKeyboardButton(text="📣 Broadcast", callback_data="adm_cast"),
        types.InlineKeyboardButton(text="➕ Add Bal", callback_data="adm_add_bal"),
        types.InlineKeyboardButton(text="➖ Rem Bal", callback_data="adm_rem_bal"),
        types.InlineKeyboardButton(text="🚫 Ban", callback_data="adm_ban"),
        types.InlineKeyboardButton(text="✅ Unban", callback_data="adm_unban"),
        types.InlineKeyboardButton(text="📥 Export", callback_data="adm_export"),
        types.InlineKeyboardButton(text="⚙️ Settings", callback_data="adm_settings"),
        types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_home")
    )
    b.adjust(2)
    return b.as_markup()

def admin_tasks_markup():
    b = InlineKeyboardBuilder()
    b.add(
        types.InlineKeyboardButton(text="➕ Add Gmail Task", callback_data="adm_t_add_gml"),
        types.InlineKeyboardButton(text="➕ Add Review Task", callback_data="adm_t_add_rev"),
        types.InlineKeyboardButton(text="🗑 Delete Task", callback_data="adm_t_del"),
        types.InlineKeyboardButton(text="⏸ Pause Task", callback_data="adm_t_pause"),
        types.InlineKeyboardButton(text="▶️ Resume Task", callback_data="adm_t_resume"),
        types.InlineKeyboardButton(text="📈 Task Stats", callback_data="adm_t_stats"),
        types.InlineKeyboardButton(text="⬅️ Back", callback_data="admin_home")
    )
    b.adjust(2)
    return b.as_markup()

def admin_settings_markup():
    b = InlineKeyboardBuilder()
    b.add(
        types.InlineKeyboardButton(text="💰 Min Withdraw", callback_data="adm_s_minwd"),
        types.InlineKeyboardButton(text="💱 Currency", callback_data="adm_s_curr"),
        types.InlineKeyboardButton(text="🤖 Auto Verify", callback_data="adm_s_auto"),
        types.InlineKeyboardButton(text="💵 Ref Reward", callback_data="adm_s_ref"),
        types.InlineKeyboardButton(text="⬅️ Back", callback_data="admin_home")
    )
    b.adjust(2)
    return b.as_markup()

def admin_withdraw_action(wd_id):
    b = InlineKeyboardBuilder()
    b.row(types.InlineKeyboardButton(text="✅ Confirm", callback_data=f"awd_conf_{wd_id}"))
    b.row(types.InlineKeyboardButton(text="❌ Cancel", callback_data=f"awd_canc_{wd_id}"))
    b.row(types.InlineKeyboardButton(text="⏸ Hold", callback_data=f"awd_hold_{wd_id}"))
    return b.as_markup()

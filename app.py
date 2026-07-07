#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Architect Advanced Key Bot v3.0 – Single File Edition
# يعمل على Python 3.8+، يدعم العربية والإنجليزية، صلاحيات، توليد أكواد، استخدام، إحصائيات

import logging
import sqlite3
import random
import string
import json
import os
import sys
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# ================== التوكن ومعرف المطور ==================
TOKEN = "8784870546:AAFvp4hFXShO14-5e1Kg_noFn03UpmDMUT8"
OWNER_ID = 6129372969  # ضع معرفك هنا (المطور الأساسي)

# ================== الترجمات مدمجة (لا حاجة لملف خارجي) ==================
TRANSLATIONS = {
    "ar": {
        "welcome": "مرحباً بك {username}!\nاختر من القائمة:",
        "gen_code": "🔑 توليد كود",
        "deactivate": "❌ تعطيل كود",
        "check_code": "✅ التحقق من كود",
        "my_codes": "📋 أكوادي",
        "add_user": "👥 إضافة مستخدم",
        "my_info": "ℹ️ معلوماتي",
        "stats": "📊 الإحصائيات",
        "lang": "🌐 اللغة",
        "use_code": "♻️ استخدام كود",
        "no_permission": "⛔ ليس لديك صلاحية لهذا الإجراء.",
        "enter_days": "📅 أدخل عدد الأيام لصلاحية الكود (رقم فقط):",
        "enter_code_to_deactivate": "✏️ أرسل الكود الذي تريد تعطيله:",
        "enter_code_to_check": "✏️ أرسل الكود للتحقق منه:",
        "enter_user_id": "✏️ أرسل معرف (ID) المستخدم الجديد (رقم فقط):",
        "enter_code_to_use": "✏️ أرسل الكود لاستخدامه (استهلاكه):",
        "code_generated": "✅ تم توليد الكود:\n`{code}`\nصلاحية {days} يوم.",
        "code_deactivated": "✅ تم تعطيل الكود `{code}`.",
        "code_not_found": "❌ الكود غير موجود.",
        "code_already_inactive": "❌ الكود معطل بالفعل.",
        "user_exists": "⚠️ هذا المستخدم موجود بالفعل.",
        "user_added": "✅ تم إضافة المستخدم بمعرف `{id}` كـ 'user'.",
        "no_codes": "📭 ليس لديك أي أكواد مضافة.",
        "my_codes_list": "📋 *أكوادي*\n\n",
        "code_info": "📌 *الكود:* `{code}`\n📅 المدة: {days} يوم\n📆 تاريخ الإنشاء: {created}\n🔰 الحالة: {status}\n👤 المستخدم: {used_by}\n⏱ تاريخ الاستخدام: {used_at}",
        "stats_msg": "📊 *الإحصائيات*\n\n📌 الأكواد:\n   الإجمالي: {total}\n   المستخدمة: {used}\n   غير المستخدمة: {unused}\n👥 المستخدمين:\n   الإجمالي: {users_total}\n   النشطاء: {active}",
        "lang_switched": "🌐 اللغة الحالية: العربية",
        "invalid_number": "⚠️ الرجاء إدخال عدد صحيح موجب.",
        "invalid_id": "⚠️ الرجاء إدخال رقم معرف صحيح.",
        "code_used_success": "✅ تم استخدام الكود `{code}` بنجاح!",
        "code_use_failed": "❌ لم يتمكن من استخدام الكود (قد يكون غير صحيح أو منتهي الصلاحية)."
    },
    "en": {
        "welcome": "Welcome {username}!\nChoose from the menu:",
        "gen_code": "🔑 Generate Code",
        "deactivate": "❌ Deactivate Code",
        "check_code": "✅ Check Code",
        "my_codes": "📋 My Codes",
        "add_user": "👥 Add User",
        "my_info": "ℹ️ My Info",
        "stats": "📊 Statistics",
        "lang": "🌐 Language",
        "use_code": "♻️ Use Code",
        "no_permission": "⛔ You do not have permission.",
        "enter_days": "📅 Enter number of days for code validity (only number):",
        "enter_code_to_deactivate": "✏️ Send the code to deactivate:",
        "enter_code_to_check": "✏️ Send the code to check:",
        "enter_user_id": "✏️ Send the new user ID (number only):",
        "enter_code_to_use": "✏️ Send the code to use (redeem):",
        "code_generated": "✅ Code generated:\n`{code}`\nValid for {days} days.",
        "code_deactivated": "✅ Code `{code}` deactivated.",
        "code_not_found": "❌ Code not found.",
        "code_already_inactive": "❌ Code is already inactive.",
        "user_exists": "⚠️ This user already exists.",
        "user_added": "✅ User with ID `{id}` added as 'user'.",
        "no_codes": "📭 You have no codes.",
        "my_codes_list": "📋 *My Codes*\n\n",
        "code_info": "📌 *Code:* `{code}`\n📅 Duration: {days} days\n📆 Created: {created}\n🔰 Status: {status}\n👤 Used by: {used_by}\n⏱ Used at: {used_at}",
        "stats_msg": "📊 *Statistics*\n\n📌 Codes:\n   Total: {total}\n   Used: {used}\n   Unused: {unused}\n👥 Users:\n   Total: {users_total}\n   Active: {active}",
        "lang_switched": "🌐 Current language: English",
        "invalid_number": "⚠️ Please enter a positive integer.",
        "invalid_id": "⚠️ Please enter a valid numeric ID.",
        "code_used_success": "✅ Code `{code}` used successfully!",
        "code_use_failed": "❌ Failed to use code (maybe invalid or expired)."
    }
}

# ================== قاعدة البيانات ==================
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        role TEXT DEFAULT 'user',
        added_by INTEGER,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        lang TEXT DEFAULT 'ar'
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS codes (
        code TEXT PRIMARY KEY,
        duration_days INTEGER,
        created_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        used_by INTEGER,
        used_at TIMESTAMP,
        is_active BOOLEAN DEFAULT 1
    )''')
    c.execute("INSERT OR IGNORE INTO users (user_id, username, role) VALUES (?, ?, 'owner')", (OWNER_ID, "owner"))
    conn.commit()
    conn.close()

init_db()

# ================== دوال مساعدة ==================
def get_user_role(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_user_lang(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 'ar'

def set_user_lang(user_id, lang):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
    conn.commit()
    conn.close()

def add_user(user_id, username, role='user', added_by=OWNER_ID):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, role, added_by) VALUES (?, ?, ?, ?)",
              (user_id, username, role, added_by))
    conn.commit()
    conn.close()

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def create_code(duration_days, created_by):
    code = generate_code()
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO codes (code, duration_days, created_by) VALUES (?, ?, ?)",
              (code, duration_days, created_by))
    conn.commit()
    conn.close()
    return code

def get_code_info(code):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''SELECT code, duration_days, created_at, used_by, used_at, is_active 
                 FROM codes WHERE code = ?''', (code,))
    row = c.fetchone()
    conn.close()
    return row

def deactivate_code(code):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE codes SET is_active = 0 WHERE code = ?", (code,))
    conn.commit()
    conn.close()

def use_code(code, user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE codes SET used_by = ?, used_at = CURRENT_TIMESTAMP, is_active = 0 WHERE code = ? AND is_active = 1",
              (user_id, code))
    affected = c.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def get_stats():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    total_codes = c.execute("SELECT COUNT(*) FROM codes").fetchone()[0]
    used_codes = c.execute("SELECT COUNT(*) FROM codes WHERE is_active = 0 AND used_by IS NOT NULL").fetchone()[0]
    unused_codes = c.execute("SELECT COUNT(*) FROM codes WHERE is_active = 1").fetchone()[0]
    total_users = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    active_users = c.execute("SELECT COUNT(*) FROM users WHERE role != 'owner'").fetchone()[0]
    conn.close()
    return total_codes, used_codes, unused_codes, total_users, active_users

def get_my_codes(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT code, duration_days, created_at, is_active FROM codes WHERE created_by = ? ORDER BY created_at DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

# ================== معالجات البوت ==================
SELECT_DAYS = 1
DEACTIVATE_CODE = 2
ADD_USER = 3
CHECK_CODE = 4
USE_CODE = 5

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name
    role = get_user_role(user_id)
    if not role:
        add_user(user_id, username, 'user')
        role = 'user'
    lang = get_user_lang(user_id)
    t = TRANSLATIONS[lang]

    keyboard = []
    if role in ['owner', 'admin']:
        keyboard.append([InlineKeyboardButton(t["gen_code"], callback_data="gen_code")])
        keyboard.append([InlineKeyboardButton(t["deactivate"], callback_data="deactivate_code")])
        keyboard.append([InlineKeyboardButton(t["my_codes"], callback_data="my_codes")])
        keyboard.append([InlineKeyboardButton(t["add_user"], callback_data="add_user")])
    keyboard.append([InlineKeyboardButton(t["check_code"], callback_data="check_code")])
    keyboard.append([InlineKeyboardButton(t["use_code"], callback_data="use_code")])
    keyboard.append([InlineKeyboardButton(t["my_info"], callback_data="my_info")])
    if role == 'owner':
        keyboard.append([InlineKeyboardButton(t["stats"], callback_data="stats")])
    keyboard.append([InlineKeyboardButton(t["lang"], callback_data="lang")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(t["welcome"].format(username=username), reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    role = get_user_role(user_id)
    lang = get_user_lang(user_id)
    t = TRANSLATIONS[lang]
    data = query.data

    if data == "gen_code":
        if role not in ['owner', 'admin']:
            await query.edit_message_text(t["no_permission"])
            return
        context.user_data['action'] = 'gen_code'
        await query.edit_message_text(t["enter_days"])
        return SELECT_DAYS

    elif data == "deactivate_code":
        if role not in ['owner', 'admin']:
            await query.edit_message_text(t["no_permission"])
            return
        context.user_data['action'] = 'deactivate_code'
        await query.edit_message_text(t["enter_code_to_deactivate"])
        return DEACTIVATE_CODE

    elif data == "check_code":
        context.user_data['action'] = 'check_code'
        await query.edit_message_text(t["enter_code_to_check"])
        return CHECK_CODE

    elif data == "use_code":
        context.user_data['action'] = 'use_code'
        await query.edit_message_text(t["enter_code_to_use"])
        return USE_CODE

    elif data == "my_codes":
        if role not in ['owner', 'admin']:
            await query.edit_message_text(t["no_permission"])
            return
        codes = get_my_codes(user_id)
        if not codes:
            await query.edit_message_text(t["no_codes"])
        else:
            msg = t["my_codes_list"]
            for c in codes:
                status = "✅ نشط" if c[3] else "❌ معطل"
                msg += f"• `{c[0]}` – {c[1]} يوم – {c[2][:10]} – {status}\n"
            await query.edit_message_text(msg, parse_mode='Markdown')
        return

    elif data == "add_user":
        if role != 'owner':
            await query.edit_message_text(t["no_permission"])
            return
        context.user_data['action'] = 'add_user'
        await query.edit_message_text(t["enter_user_id"])
        return ADD_USER

    elif data == "my_info":
        user = query.from_user
        msg = f"🆔 المعرف: `{user.id}`\n"
        msg += f"👤 الاسم: {user.first_name}\n"
        msg += f"🔰 الصلاحية: {role}\n"
        msg += f"🌐 اللغة: {lang}"
        await query.edit_message_text(msg, parse_mode='Markdown')
        return

    elif data == "stats":
        if role != 'owner':
            await query.edit_message_text(t["no_permission"])
            return
        total_codes, used_codes, unused_codes, total_users, active_users = get_stats()
        msg = t["stats_msg"].format(
            total=total_codes, used=used_codes, unused=unused_codes,
            users_total=total_users, active=active_users
        )
        await query.edit_message_text(msg, parse_mode='Markdown')
        return

    elif data == "lang":
        new_lang = 'en' if lang == 'ar' else 'ar'
        set_user_lang(user_id, new_lang)
        t_new = TRANSLATIONS[new_lang]
        await query.edit_message_text(t_new["lang_switched"])
        # إعادة عرض القائمة
        await start(update, context)
        return

    await query.edit_message_text("⚠️ خيار غير معروف.")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.effective_user.id
    role = get_user_role(user_id)
    lang = get_user_lang(user_id)
    t = TRANSLATIONS[lang]
    action = context.user_data.get('action')

    if action == 'gen_code':
        if role not in ['owner', 'admin']:
            await update.message.reply_text(t["no_permission"])
            return
        try:
            days = int(text)
            if days <= 0: raise ValueError
        except:
            await update.message.reply_text(t["invalid_number"])
            return
        code = create_code(days, user_id)
        await update.message.reply_text(t["code_generated"].format(code=code, days=days), parse_mode='Markdown')
        context.user_data['action'] = None
        return

    elif action == 'deactivate_code':
        if role not in ['owner', 'admin']:
            await update.message.reply_text(t["no_permission"])
            return
        code = text.upper()
        info = get_code_info(code)
        if not info:
            await update.message.reply_text(t["code_not_found"])
        elif not info[5]:
            await update.message.reply_text(t["code_already_inactive"])
        else:
            deactivate_code(code)
            await update.message.reply_text(t["code_deactivated"].format(code=code), parse_mode='Markdown')
        context.user_data['action'] = None
        return

    elif action == 'check_code':
        code = text.upper()
        info = get_code_info(code)
        if not info:
            await update.message.reply_text(t["code_not_found"])
        else:
            status = "✅ نشط" if info[5] else "❌ معطل"
            used_by = "لم يستخدم" if info[3] is None else f"مستخدم من معرف {info[3]}"
            used_at = info[4] if info[4] else "—"
            msg = t["code_info"].format(
                code=info[0], days=info[1], created=info[2][:10],
                status=status, used_by=used_by, used_at=used_at
            )
            await update.message.reply_text(msg, parse_mode='Markdown')
        context.user_data['action'] = None
        return

    elif action == 'use_code':
        code = text.upper()
        info = get_code_info(code)
        if not info:
            await update.message.reply_text(t["code_not_found"])
        elif not info[5]:
            await update.message.reply_text(t["code_already_inactive"])
        else:
            success = use_code(code, user_id)
            if success:
                await update.message.reply_text(t["code_used_success"].format(code=code), parse_mode='Markdown')
            else:
                await update.message.reply_text(t["code_use_failed"])
        context.user_data['action'] = None
        return

    elif action == 'add_user':
        if role != 'owner':
            await update.message.reply_text(t["no_permission"])
            return
        try:
            new_id = int(text)
        except:
            await update.message.reply_text(t["invalid_id"])
            return
        if get_user_role(new_id):
            await update.message.reply_text(t["user_exists"])
        else:
            add_user(new_id, f"user_{new_id}", 'user', OWNER_ID)
            await update.message.reply_text(t["user_added"].format(id=new_id), parse_mode='Markdown')
        context.user_data['action'] = None
        return

    else:
        await update.message.reply_text("⚠️ الرجاء استخدام الأزرار من القائمة.")

# ================== التشغيل الرئيسي ==================
def main():
    # تحذير من ملف ssl.py المتعارض
    if os.path.exists("/storage/emulated/0/ssl.py"):
        print("⚠️ تحذير: يوجد ملف ssl.py في /storage/emulated/0/ قد يسبب خطأ. قم بحذفه أو إعادة تسميته.")
        print("يمكنك تشغيل الأمر: rm /storage/emulated/0/ssl.py")
        sys.exit(1)

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler)],
        states={
            SELECT_DAYS: [MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)],
            DEACTIVATE_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)],
            ADD_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)],
            CHECK_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)],
            USE_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)],
        },
        fallbacks=[CommandHandler("start", start)]
    )
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("🤖 Architect Advanced Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

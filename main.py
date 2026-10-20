import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = "@jawischool"
CHANNEL_URL = "https://t.me/jawischool"

app = Flask(__name__)

@app.route("/")
def home():
    return "JAWI SCHOOL AI BOT is running! 🎓"

def start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_URL)],
        [InlineKeyboardButton("✅ I've Joined — Verify", callback_data="verify")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome = (
        f"💎✨ 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐉𝐀𝐖𝐈 𝐒𝐂𝐇𝐎𝐎𝐋 ✨💎\n\n"
        f"👋 Hello {user.first_name}!\n\n"
        "🎓 Your Smart Learning Partner\n"
        "🤖 AI Tutor • 📚 Lessons • 📝 Exercises\n"
        "🇪🇹 Ethiopian Students — Grades 1–12\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📢 ትምህርቶችን ለማግኘት መጀመሪያ ቻናላችንን Join አድርግ።\n"
        "ከዚያ Verify ተጫን።\n\n"
        "💙 Learn Smart. Grow Together!"
    )
    await update.message.reply_text(
        welcome,
        reply_markup=start_keyboard()
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL,
            user_id=query.from_user.id
        )

        if member.status in ("member", "administrator", "creator"):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎓 Grades 1–12", callback_data="grades")],
                [InlineKeyboardButton("🤖 Ask AI Tutor", callback_data="ai")],
            ])
            await query.edit_message_text(
                "✅ Verification Successful!\n\n"
                f"🎉 Welcome to JAWI SCHOOL, {query.from_user.first_name}!\n\n"
                "📚 ትምህርትህን ለመጀመር ከታች ምረጥ።",
                reply_markup=keyboard
            )
        else:
            await query.answer(
                "❌ መጀመሪያ @jawischool ቻናልን Join አድርግ!",
                show_alert=True
            )
    except Exception:
        await query.answer(
            "⚠️ ማረጋገጥ አልተቻለም። Botን በChannel ውስጥ Admin አድርግ።",
            show_alert=True
        )

async def show_grades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []
    for start in range(1, 13, 3):
        row = []
        for grade in range(start, min(start + 3, 13)):
            row.append(
                InlineKeyboardButton(
                    f"📘 Grade {grade}",
                    callback_data=f"grade_{grade}"
                )
            )
        keyboard.append(row)

    await query.edit_message_text(
        "🎓 ክፍልህን ምረጥ፦",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def grade_selected

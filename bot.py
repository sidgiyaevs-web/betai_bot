import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, WebAppInfo, InlineKeyboardMarkup,
    InlineKeyboardButton, MenuButtonWebApp
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://betaibot-production.up.railway.app")

if not BOT_TOKEN:
    logger.error("BOT_TOKEN не задан в переменных окружения!")
    raise SystemExit(1)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def main_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎮 Играть",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
        [
            InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
            InlineKeyboardButton(text="🏆 Топ", callback_data="top")
        ],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ])
    return kb


@dp.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    u = db.get_user(user.id)

    text = (
        f"👋 Привет, <b>{user.first_name}</b>!\n\n"
        f"🎁 Открывай кейсы, получай скины, апгрейди предметы!\n\n"
        f"💰 Твой баланс: <b>{u['stars']} ⭐</b>\n"
        f"📦 Открыто кейсов: <b>{u['total_opened']}</b>"
    )
    await message.answer(text, reply_markup=main_menu_kb())


@dp.message(Command("balance"))
async def cmd_balance(message: Message):
    user = message.from_user
    db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    u = db.get_user(user.id)
    await message.answer(
        f"💰 Баланс: <b>{u['stars']} ⭐</b>\n"
        f"💎 Кристаллы: <b>{u['crystals']}</b>\n\n"
        f"📊 Статистика:\n"
        f"• Открыто: <b>{u['total_opened']}</b>\n"
        f"• Потрачено: <b>{u['total_spent']} ⭐</b>\n"
        f"• Выиграно: <b>{u['total_won']} ⭐</b>",
        reply_markup=main_menu_kb()
    )


@dp.message(Command("play"))
async def cmd_play(message: Message):
    user = message.from_user
    db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    await message.answer(
        "🎮 Нажми кнопку ниже, чтобы открыть игру:",
        reply_markup=main_menu_kb()
    )
@dp.message(Command("give"))
async def cmd_give(message: Message):
    user = message.from_user
    db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    try:
        parts = message.text.split()
        amount = int(parts[1]) if len(parts) > 1 else 1000
    except:
        amount = 1000
    if amount > 1000000:
        amount = 1000000
    db.update_balance(user.id, stars_delta=amount)
    fresh = db.get_user(user.id)
    await message.answer(
        f"✅ Выдано <b>{amount} ⭐</b>\n\n"
        f"💰 Твой баланс: <b>{fresh['stars']} ⭐</b>",
        reply_markup=main_menu_kb()
    )

@dp.callback_query(F.data == "profile")
async def cb_profile(callback):
    user = callback.from_user
    db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    u = db.get_user(user.id)
    inv = db.get_inventory(user.id)
    text = (
        f"👤 <b>Профиль</b>\n\n"
        f"💰 Баланс: <b>{u['stars']} ⭐</b>\n"
        f"💎 Кристаллы: <b>{u['crystals']}</b>\n"
        f"📦 Предметов: <b>{len(inv)}</b>\n"
        f"🎁 Открыто кейсов: <b>{u['total_opened']}</b>"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@dp.callback_query(F.data == "top")
async def cb_top(callback):
    conn = db.get_conn()
    c = conn.cursor()
    c.execute("SELECT first_name, username, total_opened, total_won FROM users ORDER BY total_won DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    text = "🏆 <b>Топ-10 игроков</b>\n\n"
    medals = ["🥇", "🥈", "🥉"]
    for i, r in enumerate(rows):
        icon = medals[i] if i < 3 else f"{i+1}."
        name = r["first_name"] or r["username"] or "Игрок"
        text += f"{icon} <b>{name}</b> — {r['total_won']} ⭐ (открыто {r['total_opened']})\n"
    if not rows:
        text += "Пока пусто"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@dp.callback_query(F.data == "help")
async def cb_help(callback):
    text = (
        f"ℹ️ <b>Помощь</b>\n\n"
        f"🎁 <b>Кейсы</b> — открывай кейсы за звёзды, получай предметы\n"
        f"⚡ <b>Апгрейд</b> — обменяй предмет на более дорогой с шансом\n"
        f"💣 <b>Мины</b> — открой ячейки, не попав на мину\n"
        f"📈 <b>Краш</b> — забери выигрыш пока кэф не упал\n\n"
        f"Если что-то не работает — пиши админу."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@dp.callback_query(F.data == "back")
async def cb_back(callback):
    user = callback.from_user
    db.get_or_create_user(user.id, user.username or "", user.first_name or "")
    u = db.get_user(user.id)
    text = (
        f"👋 Привет, <b>{user.first_name}</b>!\n\n"
        f"🎁 Открывай кейсы, получай скины, апгрейди предметы!\n\n"
        f"💰 Твой баланс: <b>{u['stars']} ⭐</b>\n"
        f"📦 Открыто кейсов: <b>{u['total_opened']}</b>"
    )
    await callback.message.edit_text(text, reply_markup=main_menu_kb())
    await callback.answer()


async def set_menu_button():
    try:
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="🎮 Играть",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        )
        logger.info("Menu button set to: " + WEBAPP_URL)
    except Exception as e:
        logger.error(f"Ошибка установки меню: {e}")


async def main():
    logger.info("Запуск бота...")
    db.init_db()
    await set_menu_button()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

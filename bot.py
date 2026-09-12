# -*- coding: utf-8 -*-
# BET LIFE — экономическая игра в Telegram

import asyncio
import random
import json
import os
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ============================================
# ТОКЕН
# ============================================

TOKEN = "8960922268:AAEz_DK55WFN7IoCGSR6CYuMRDYB0xfhMWc"

# ============================================
# ДАННЫЕ ИГРЫ
# ============================================

START_MONEY = 10000
BONUS_30MIN = 2000
BONUS_DAILY = 50000

JOBS = [
    {"id": 1, "name": "🧹 Дворник", "emoji": "🧹", "income": (2000, 5000), "cd": 20, "req": None},
    {"id": 2, "name": "🚚 Курьер", "emoji": "🚚", "income": (5000, 12000), "cd": 20, "req": None},
    {"id": 3, "name": "🍔 Официант", "emoji": "🍔", "income": (10000, 20000), "cd": 25, "req": None},
    {"id": 4, "name": "🏪 Продавец", "emoji": "🏪", "income": (20000, 40000), "cd": 30, "req": None},
    {"id": 5, "name": "👨‍💻 Программист", "emoji": "👨‍💻", "income": (50000, 100000), "cd": 40, "req": None},
    {"id": 6, "name": "🧑‍⚕️ Врач", "emoji": "🧑‍⚕️", "income": (80000, 150000), "cd": 45, "req": None},
    {"id": 7, "name": "👨‍⚖️ Адвокат", "emoji": "👨‍⚖️", "income": (120000, 250000), "cd": 60, "req": None},
    {"id": 8, "name": "📊 Трейдер", "emoji": "📊", "income": (200000, 500000), "cd": 60, "req": None},
    {"id": 9, "name": "🎬 Режиссёр", "emoji": "🎬", "income": (400000, 800000), "cd": 90, "req": None},
    {"id": 10, "name": "💼 Бизнесмен", "emoji": "💼", "income": (800000, 2000000), "cd": 120, "req": None},
    {"id": 11, "name": "🏗 Олигарх", "emoji": "🏗", "income": (2000000, 5000000), "cd": 120, "req": None},
    {"id": 12, "name": "👑 Магнат", "emoji": "👑", "income": (5000000, 15000000), "cd": 180, "req": None}
]

CARS = [
    {"id": 1, "name": "🚗 Лада Гранта", "emoji": "🚗", "price": 100000, "speed": 170, "power": 106},
    {"id": 2, "name": "🚗 Hyundai Solaris", "emoji": "🚗", "price": 300000, "speed": 190, "power": 123},
    {"id": 3, "name": "🚙 Toyota Camry", "emoji": "🚙", "price": 800000, "speed": 210, "power": 200},
    {"id": 4, "name": "🚙 Kia Sportage", "emoji": "🚙", "price": 1200000, "speed": 200, "power": 180},
    {"id": 5, "name": "🚙 Volkswagen Tiguan", "emoji": "🚙", "price": 1800000, "speed": 210, "power": 220},
    {"id": 6, "name": "🚘 BMW 3-series", "emoji": "🚘", "price": 3000000, "speed": 250, "power": 258},
    {"id": 7, "name": "🚘 Audi A6", "emoji": "🚘", "price": 5000000, "speed": 250, "power": 340},
    {"id": 8, "name": "🚘 Mercedes E-class", "emoji": "🚘", "price": 8000000, "speed": 250, "power": 367},
    {"id": 9, "name": "🏎 BMW M5", "emoji": "🏎", "price": 15000000, "speed": 305, "power": 600},
    {"id": 10, "name": "🏎 Audi RS7", "emoji": "🏎", "price": 25000000, "speed": 305, "power": 605},
    {"id": 11, "name": "🏎 Mercedes AMG GT", "emoji": "🏎", "price": 40000000, "speed": 318, "power": 585},
    {"id": 12, "name": "🏎 Porsche 911", "emoji": "🏎", "price": 70000000, "speed": 330, "power": 650},
    {"id": 13, "name": "🏎 Ferrari F8", "emoji": "🏎", "price": 120000000, "speed": 340, "power": 720},
    {"id": 14, "name": "🏎 Lamborghini Huracan", "emoji": "🏎", "price": 200000000, "speed": 325, "power": 640},
    {"id": 15, "name": "🏎 McLaren 720S", "emoji": "🏎", "price": 300000000, "speed": 341, "power": 720},
    {"id": 16, "name": "🏎 Bugatti Chiron", "emoji": "🏎", "price": 500000000, "speed": 420, "power": 1500},
    {"id": 17, "name": "🏎 Koenigsegg Jesko", "emoji": "🏎", "price": 800000000, "speed": 480, "power": 1600},
    {"id": 18, "name": "🏎 Pagani Huayra", "emoji": "🏎", "price": 1200000000, "speed": 383, "power": 730},
    {"id": 19, "name": "🏎 Rolls-Royce Phantom", "emoji": "🏎", "price": 2000000000, "speed": 250, "power": 563},
    {"id": 20, "name": "🚀 Devel Sixteen", "emoji": "🚀", "price": 5000000000, "speed": 560, "power": 5000}
]

HOUSES = [
    {"id": 1, "name": "🏚 Комната", "emoji": "🏚", "price": 50000, "income": 500},
    {"id": 2, "name": "🏠 Студия", "emoji": "🏠", "price": 150000, "income": 2000},
    {"id": 3, "name": "🏠 Квартира 1к", "emoji": "🏠", "price": 400000, "income": 6000},
    {"id": 4, "name": "🏠 Квартира 3к", "emoji": "🏠", "price": 1000000, "income": 18000},
    {"id": 5, "name": "🏡 Дом", "emoji": "🏡", "price": 3000000, "income": 60000},
    {"id": 6, "name": "🏡 Коттедж", "emoji": "🏡", "price": 10000000, "income": 200000},
    {"id": 7, "name": "🏘 Особняк", "emoji": "🏘", "price": 30000000, "income": 700000},
    {"id": 8, "name": "🏰 Замок", "emoji": "🏰", "price": 100000000, "income": 2500000},
    {"id": 9, "name": "🏯 Резиденция", "emoji": "🏯", "price": 300000000, "income": 8000000},
    {"id": 10, "name": "🌆 Пентхаус", "emoji": "🌆", "price": 1000000000, "income": 30000000},
    {"id": 11, "name": "🏝 Остров", "emoji": "🏝", "price": 5000000000, "income": 150000000}
]

BUSINESSES = [
    {"id": 1, "name": "☕ Ларёк", "emoji": "☕", "price": 100000, "income": 1000},
    {"id": 2, "name": "🍔 Кафе", "emoji": "🍔", "price": 500000, "income": 8000},
    {"id": 3, "name": "🏪 Магазин", "emoji": "🏪", "price": 2000000, "income": 35000},
    {"id": 4, "name": "🏨 Отель", "emoji": "🏨", "price": 10000000, "income": 200000},
    {"id": 5, "name": "🏭 Завод", "emoji": "🏭", "price": 50000000, "income": 1200000},
    {"id": 6, "name": "🏢 Бизнес-центр", "emoji": "🏢", "price": 200000000, "income": 6000000},
    {"id": 7, "name": "🏦 Банк", "emoji": "🏦", "price": 1000000000, "income": 35000000},
    {"id": 8, "name": "📡 Оператор связи", "emoji": "📡", "price": 5000000000, "income": 200000000},
    {"id": 9, "name": "🚀 Космокомпания", "emoji": "🚀", "price": 50000000000, "income": 2500000000}
]

# ============================================
# ХРАНИЛИЩЕ
# ============================================

DATA_FILE = "users_data.json"
USERS = {}

def load_data():
    global USERS
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                USERS = json.load(f)
    except Exception:
        USERS = {}

def save_data():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(USERS, f, ensure_ascii=False)
    except Exception:
        pass

def get_user(uid: int) -> dict:
    uid_s = str(uid)
    if uid_s not in USERS:
        USERS[uid_s] = {
            'balance': START_MONEY,
            'job_id': 0,
            'last_work': 0,
            'last_bonus_30': 0,
            'last_bonus_day': 0,
            'cars': {},
            'houses': {},
            'businesses': {},
            'income_balance': 0,
            'total_earned': 0,
            'games_played': 0,
            'wins': 0
        }
        save_data()
    return USERS[uid_s]

def income_per_20min(user: dict) -> int:
    total = 0
    for hid, cnt in user.get('houses', {}).items():
        h = next((x for x in HOUSES if x['id'] == int(hid)), None)
        if h:
            total += h['income'] * cnt
    for bid, cnt in user.get('businesses', {}).items():
        b = next((x for x in BUSINESSES if x['id'] == int(bid)), None)
        if b:
            total += b['income'] * cnt
    return total

def fmt_money(n: int) -> str:
    if n >= 1e12:
        return f"{n/1e12:.2f}T $"
    if n >= 1e9:
        return f"{n/1e9:.2f}B $"
    if n >= 1e6:
        return f"{n/1e6:.2f}M $"
    if n >= 1e3:
        return f"{n/1e3:.1f}K $"
    return f"{n} $"
    
# ============================================
# КЛАВИАТУРЫ
# ============================================

def main_menu_kb():
    kb = [
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
         InlineKeyboardButton(text="💼 Работа", callback_data="work_menu")],
        [InlineKeyboardButton(text="🛒 Магазин", callback_data="shop"),
         InlineKeyboardButton(text="🎰 Казино", callback_data="casino")],
        [InlineKeyboardButton(text="🏆 Топ игроков", callback_data="top"),
         InlineKeyboardButton(text="🎁 Бонус", callback_data="bonus")],
        [InlineKeyboardButton(text="💸 Перевод", callback_data="transfer_info"),
         InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="menu")]])

def shop_kb():
    kb = [
        [InlineKeyboardButton(text="🚗 Машины", callback_data="shop_cars")],
        [InlineKeyboardButton(text="🏠 Дома", callback_data="shop_houses")],
        [InlineKeyboardButton(text="💼 Бизнесы", callback_data="shop_biz")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def shop_cars_kb():
    kb = []
    for c in CARS:
        kb.append([InlineKeyboardButton(
            text=f"{c['emoji']} {c['name']} — {fmt_money(c['price'])}",
            callback_data=f"buy_car_{c['id']}"
        )])
    kb.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="shop")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def shop_houses_kb():
    kb = []
    for h in HOUSES:
        kb.append([InlineKeyboardButton(
            text=f"{h['emoji']} {h['name']} — {fmt_money(h['price'])}",
            callback_data=f"buy_house_{h['id']}"
        )])
    kb.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="shop")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def shop_biz_kb():
    kb = []
    for b in BUSINESSES:
        kb.append([InlineKeyboardButton(
            text=f"{b['emoji']} {b['name']} — {fmt_money(b['price'])}",
            callback_data=f"buy_biz_{b['id']}"
        )])
    kb.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="shop")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def work_menu_kb(user):
    kb = []
    for job in JOBS:
        current = "✅ " if user.get('job_id') == job['id'] else ""
        kb.append([InlineKeyboardButton(
            text=f"{current}{job['name']} — до {fmt_money(job['income'][1])} ({job['cd']} мин)",
            callback_data=f"take_job_{job['id']}"
        )])
    kb.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def profile_kb():
    kb = [
        [InlineKeyboardButton(text="🚗 Мои машины", callback_data="my_cars")],
        [InlineKeyboardButton(text="🏠 Мои дома", callback_data="my_houses")],
        [InlineKeyboardButton(text="💼 Мои бизнесы", callback_data="my_biz")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def cars_list_kb():
    kb = [
        [InlineKeyboardButton(text="🚗 Машины", callback_data="shop_cars")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="profile")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def houses_list_kb():
    kb = [
        [InlineKeyboardButton(text="🏠 Дома", callback_data="shop_houses")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="profile")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def biz_list_kb():
    kb = [
        [InlineKeyboardButton(text="💼 Бизнесы", callback_data="shop_biz")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="profile")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def casino_kb():
    kb = [
        [InlineKeyboardButton(text="🎲 Кубик", callback_data="game_dice")],
        [InlineKeyboardButton(text="🎰 Спин", callback_data="game_spin")],
        [InlineKeyboardButton(text="📈 Трейд", callback_data="game_trade")],
        [InlineKeyboardButton(text="🎯 Дартс", callback_data="game_darts")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

# ============================================
# ФОРМАТИРОВАНИЕ
# ============================================

def format_profile(user, username: str) -> str:
    job_id = user.get('job_id', 0)
    job_name = "❌ Не выбрана"
    if job_id:
        job = next((j for j in JOBS if j['id'] == job_id), None)
        if job:
            job_name = job['name']
    
    cars_count = sum(user.get('cars', {}).values())
    houses_count = sum(user.get('houses', {}).values())
    biz_count = sum(user.get('businesses', {}).values())
    
    income = income_per_20min(user)
    
    text = f"👤 <b>Профиль</b>\n\n"
    text += f"🏷 Имя: <b>{username}</b>\n"
    text += f"💰 Баланс: <b>{fmt_money(user['balance'])}</b>\n"
    text += f"💼 Работа: {job_name}\n"
    text += f"📈 Доход (за 20 мин): <b>+{fmt_money(income)}</b>\n\n"
    text += f"━━━ ИМУЩЕСТВО ━━━\n"
    text += f"🚗 Машины: <b>{cars_count}</b>\n"
    text += f"🏠 Дома: <b>{houses_count}</b>\n"
    text += f"💼 Бизнесы: <b>{biz_count}</b>\n\n"
    text += f"━━━ СТАТИСТИКА ━━━\n"
    text += f"💵 Всего заработано: <b>{fmt_money(user.get('total_earned', 0))}</b>\n"
    text += f"🎮 Игр в казино: <b>{user.get('games_played', 0)}</b>\n"
    text += f"🏆 Побед: <b>{user.get('wins', 0)}</b>"
    
    return text

def format_my_cars(user) -> str:
    cars = user.get('cars', {})
    if not cars:
        return "🚗 <b>Мои машины</b>\n\nУ тебя нет машин.\n\n<i>Купи в магазине!</i>"
    text = "🚗 <b>Мои машины</b>\n\n"
    for cid, cnt in cars.items():
        c = next((x for x in CARS if x['id'] == int(cid)), None)
        if c:
            text += f"{c['emoji']} {c['name']} × {cnt}\n"
            text += f"   💵 {fmt_money(c['price'])} | ⚡ {c['speed']} км/ч | 🐎 {c['power']} л.с.\n\n"
    return text

def format_my_houses(user) -> str:
    houses = user.get('houses', {})
    if not houses:
        return "🏠 <b>Мои дома</b>\n\nУ тебя нет домов.\n\n<i>Купи в магазине!</i>"
    text = "🏠 <b>Мои дома</b>\n\n"
    for hid, cnt in houses.items():
        h = next((x for x in HOUSES if x['id'] == int(hid)), None)
        if h:
            text += f"{h['emoji']} {h['name']} × {cnt}\n"
            text += f"   💵 {fmt_money(h['price'])} | 📈 +{fmt_money(h['income'])}/20мин\n\n"
    return text

def format_my_biz(user) -> str:
    biz = user.get('businesses', {})
    if not biz:
        return "💼 <b>Мои бизнесы</b>\n\nУ тебя нет бизнесов.\n\n<i>Купи в магазине!</i>"
    text = "💼 <b>Мои бизнесы</b>\n\n"
    for bid, cnt in biz.items():
        b = next((x for x in BUSINESSES if x['id'] == int(bid)), None)
        if b:
            text += f"{b['emoji']} {b['name']} × {cnt}\n"
            text += f"   💵 {fmt_money(b['price'])} | 📈 +{fmt_money(b['income'])}/20мин\n\n"
    return text

def format_top() -> str:
    if not USERS:
        return "🏆 <b>Топ игроков</b>\n\nПока пусто."
    sorted_users = sorted(USERS.items(), key=lambda x: x[1]['balance'], reverse=True)[:10]
    text = "🏆 <b>Топ-10 богачей</b>\n\n"
    medals = ['🥇', '🥈', '🥉']
    for i, (uid, u) in enumerate(sorted_users, 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        text += f"{medal} <b>{fmt_money(u['balance'])}</b>\n"
    return text

# ============================================
# BOT
# ============================================

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def safe_edit(call, text, kb):
    try:
        await call.message.edit_text(text, parse_mode="HTML", reply_markup=kb)
    except Exception:
        try:
            await call.message.answer(text, parse_mode="HTML", reply_markup=kb)
        except Exception:
            pass

# ============================================
# КОМАНДЫ
# ============================================

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    load_data()
    user = get_user(message.from_user.id)
    text = "💵 <b>BET LIFE — экономическая игра</b>\n\n"
    text += f"Привет, <b>{message.from_user.first_name}</b>!\n\n"
    text += f"Твой стартовый капитал: <b>{fmt_money(START_MONEY)}</b>\n\n"
    text += "📌 Что можно делать:\n"
    text += "• 💼 Работать\n"
    text += "• 🚗 Покупать машины\n"
    text += "• 🏠 Покупать дома (пассивный доход)\n"
    text += "• 💼 Открывать бизнесы\n"
    text += "• 🎰 Играть в казино\n"
    text += "• 🏆 Стать топ-1\n\n"
    text += "Выбери действие 👇"
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu_kb())

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    text = "ℹ️ <b>Помощь</b>\n\n"
    text += "👤 <b>Профиль</b> — баланс и имущество\n"
    text += "💼 <b>Работа</b> — выбрать работу и заработать\n"
    text += "🛒 <b>Магазин</b> — купить машины, дома, бизнесы\n"
    text += "🎰 <b>Казино</b> — рискнуть деньгами\n"
    text += "🏆 <b>Топ</b> — рейтинг игроков\n"
    text += "🎁 <b>Бонус</b> — забрать бесплатные деньги\n"
    text += "💸 <b>Перевод</b> — отправить деньги другому\n\n"
    text += "📌 <b>Перевод:</b> <code>перевод @username сумма</code>"
    await message.answer(text, parse_mode="HTML", reply_markup=back_kb())

@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    load_data()
    user = get_user(message.from_user.id)
    text = format_profile(user, message.from_user.first_name)
    await message.answer(text, parse_mode="HTML", reply_markup=profile_kb())

@dp.message(Command("top"))
async def cmd_top(message: types.Message):
    load_data()
    await message.answer(format_top(), parse_mode="HTML", reply_markup=back_kb())

@dp.message(Command("работа"))
async def cmd_work_legacy(message: types.Message):
    load_data()
    user = get_user(message.from_user.id)
    await message.answer("💼 <b>Выбор работы</b>\n\nВыбери работу 👇", parse_mode="HTML", reply_markup=work_menu_kb(user))

@dp.message(Command("магазин"))
async def cmd_shop_legacy(message: types.Message):
    await message.answer("🛒 <b>Магазин</b>\n\nЧто покупаем?", parse_mode="HTML", reply_markup=shop_kb())

@dp.message(Command("бонус"))
async def cmd_bonus_legacy(message: types.Message):
    load_data()
    user = get_user(message.from_user.id)
    now = int(datetime.now().timestamp())
    
    last = user.get('last_bonus_30', 0)
    if now - last < 1800:
        wait = 1800 - (now - last)
        await message.answer(f"⏳ Бонус будет через {wait // 60} мин")
        return
    
    user['last_bonus_30'] = now
    user['balance'] += BONUS_30MIN
    user['total_earned'] = user.get('total_earned', 0) + BONUS_30MIN
    save_data()
    await message.answer(f"🎁 Бонус: +{fmt_money(BONUS_30MIN)}\n💰 Баланс: {fmt_money(user['balance'])}", parse_mode="HTML")

# ============================================
# CALLBACK — МЕНЮ
# ============================================

@dp.callback_query(lambda c: c.data == "menu")
async def cb_menu(call: types.CallbackQuery):
    await safe_edit(call, "🏠 <b>Главное меню</b>\n\nВыбери действие 👇", main_menu_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data == "help")
async def cb_help(call: types.CallbackQuery):
    text = "ℹ️ <b>Помощь</b>\n\n"
    text += "👤 Профиль — баланс и имущество\n"
    text += "💼 Работа — выбрать работу\n"
    text += "🛒 Магазин — купить имущество\n"
    text += "🎰 Казино — рискнуть\n"
    text += "🏆 Топ — рейтинг\n"
    text += "🎁 Бонус — деньги\n"
    text += "💸 Перевод — отправить\n\n"
    text += "📌 Перевод: <code>перевод @username сумма</code>"
    await safe_edit(call, text, back_kb())
    await call.answer()

# ============================================
# CALLBACK — ПРОФИЛЬ
# ============================================

@dp.callback_query(lambda c: c.data == "profile")
async def cb_profile(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = format_profile(user, call.from_user.first_name)
    await safe_edit(call, text, profile_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data == "my_cars")
async def cb_my_cars(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = format_my_cars(user)
    await safe_edit(call, text, cars_list_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data == "my_houses")
async def cb_my_houses(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = format_my_houses(user)
    await safe_edit(call, text, houses_list_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data == "my_biz")
async def cb_my_biz(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = format_my_biz(user)
    await safe_edit(call, text, biz_list_kb())
    await call.answer()

# ============================================
# CALLBACK — РАБОТА
# ============================================

@dp.callback_query(lambda c: c.data == "work_menu")
async def cb_work_menu(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = "💼 <b>Выбор работы</b>\n\n"
    text += "Текущая: "
    jid = user.get('job_id', 0)
    if jid:
        j = next((x for x in JOBS if x['id'] == jid), None)
        text += j['name'] if j else "—"
    else:
        text += "не выбрана"
    text += "\n\nВыбери работу 👇"
    await safe_edit(call, text, work_menu_kb(user))
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("take_job_"))
async def cb_take_job(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    job_id = int(call.data.split("_")[2])
    job = next((j for j in JOBS if j['id'] == job_id), None)
    if not job:
        await call.answer("Работа не найдена", show_alert=True)
        return
    
    now = int(datetime.now().timestamp())
    last = user.get('last_work', 0)
    cd_sec = job['cd'] * 60
    
    if now - last < cd_sec and user.get('job_id') == job_id:
        wait = cd_sec - (now - last)
        await call.answer(f"⏳ Работа доступна через {wait // 60} мин {wait % 60} сек", show_alert=True)
        return
    
    income = random.randint(job['income'][0], job['income'][1])
    user['balance'] += income
    user['total_earned'] = user.get('total_earned', 0) + income
    user['job_id'] = job_id
    user['last_work'] = now
    save_data()
    
    text = f"{job['emoji']} <b>{job['name']}</b>\n\n"
    text += f"💰 Заработал: <b>+{fmt_money(income)}</b>\n"
    text += f"💼 Баланс: <b>{fmt_money(user['balance'])}</b>\n\n"
    text += f"⏰ Следующая работа через {job['cd']} мин"
    
    await safe_edit(call, text, work_menu_kb(user))
    await call.answer(f"✅ +{fmt_money(income)}")

# ============================================
# CALLBACK — МАГАЗИН
# ============================================

@dp.callback_query(lambda c: c.data == "shop")
async def cb_shop(call: types.CallbackQuery):
    text = "🛒 <b>Магазин</b>\n\nЧто покупаем?"
    await safe_edit(call, text, shop_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data == "shop_cars")
async def cb_shop_cars(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = "🚗 <b>Машины</b>\n\n"
    text += f"💰 Твой баланс: <b>{fmt_money(user['balance'])}</b>\n\n"
    text += "Выбери машину 👇"
    await safe_edit(call, text, shop_cars_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data == "shop_houses")
async def cb_shop_houses(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = "🏠 <b>Дома</b>\n\n"
    text += f"💰 Твой баланс: <b>{fmt_money(user['balance'])}</b>\n\n"
    text += "📈 Дома дают пассивный доход каждые 20 минут\n\n"
    text += "Выбери дом 👇"
    await safe_edit(call, text, shop_houses_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data == "shop_biz")
async def cb_shop_biz(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = "💼 <b>Бизнесы</b>\n\n"
    text += f"💰 Твой баланс: <b>{fmt_money(user['balance'])}</b>\n\n"
    text += "📈 Бизнесы дают пассивный доход каждые 20 минут\n\n"
    text += "Выбери бизнес 👇"
    await safe_edit(call, text, shop_biz_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("buy_car_"))
async def cb_buy_car(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    cid = int(call.data.split("_")[2])
    car = next((c for c in CARS if c['id'] == cid), None)
    if not car:
        await call.answer("Не найдено", show_alert=True)
        return
    if user['balance'] < car['price']:
        await call.answer(f"❌ Не хватает {fmt_money(car['price'] - user['balance'])}", show_alert=True)
        return
    user['balance'] -= car['price']
    cars = user.get('cars', {})
    cars[str(cid)] = cars.get(str(cid), 0) + 1
    user['cars'] = cars
    save_data()
    await call.answer(f"✅ Куплено: {car['name']}", show_alert=True)
    text = f"✅ <b>Куплено!</b>\n\n{car['emoji']} <b>{car['name']}</b>\n"
    text += f"💵 Цена: {fmt_money(car['price'])}\n"
    text += f"⚡ Макс. скорость: {car['speed']} км/ч\n"
    text += f"🐎 Мощность: {car['power']} л.с.\n\n"
    text += f"💰 Баланс: <b>{fmt_money(user['balance'])}</b>"
    await safe_edit(call, text, shop_cars_kb())

@dp.callback_query(lambda c: c.data.startswith("buy_house_"))
async def cb_buy_house(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    hid = int(call.data.split("_")[2])
    h = next((x for x in HOUSES if x['id'] == hid), None)
    if not h:
        await call.answer("Не найдено", show_alert=True)
        return
    if user['balance'] < h['price']:
        await call.answer(f"❌ Не хватает {fmt_money(h['price'] - user['balance'])}", show_alert=True)
        return
    user['balance'] -= h['price']
    houses = user.get('houses', {})
    houses[str(hid)] = houses.get(str(hid), 0) + 1
    user['houses'] = houses
    save_data()
    await call.answer(f"✅ Куплено: {h['name']}", show_alert=True)
    text = f"✅ <b>Куплено!</b>\n\n{h['emoji']} <b>{h['name']}</b>\n"
    text += f"💵 Цена: {fmt_money(h['price'])}\n"
    text += f"📈 Доход: +{fmt_money(h['income'])}/20мин\n\n"
    text += f"💰 Баланс: <b>{fmt_money(user['balance'])}</b>"
    await safe_edit(call, text, shop_houses_kb())

@dp.callback_query(lambda c: c.data.startswith("buy_biz_"))
async def cb_buy_biz(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    bid = int(call.data.split("_")[2])
    b = next((x for x in BUSINESSES if x['id'] == bid), None)
    if not b:
        await call.answer("Не найдено", show_alert=True)
        return
    if user['balance'] < b['price']:
        await call.answer(f"❌ Не хватает {fmt_money(b['price'] - user['balance'])}", show_alert=True)
        return
    user['balance'] -= b['price']
    biz = user.get('businesses', {})
    biz[str(bid)] = biz.get(str(bid), 0) + 1
    user['businesses'] = biz
    save_data()
    await call.answer(f"✅ Куплено: {b['name']}", show_alert=True)
    text = f"✅ <b>Куплено!</b>\n\n{b['emoji']} <b>{b['name']}</b>\n"
    text += f"💵 Цена: {fmt_money(b['price'])}\n"
    text += f"📈 Доход: +{fmt_money(b['income'])}/20мин\n\n"
    text += f"💰 Баланс: <b>{fmt_money(user['balance'])}</b>"
    await safe_edit(call, text, shop_biz_kb())

# ============================================
# CALLBACK — БОНУС
# ============================================

@dp.callback_query(lambda c: c.data == "bonus")
async def cb_bonus(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    now = int(datetime.now().timestamp())
    
    msgs = []
    
    # 30-мин бонус
    last = user.get('last_bonus_30', 0)
    if now - last >= 1800:
        user['last_bonus_30'] = now
        user['balance'] += BONUS_30MIN
        user['total_earned'] = user.get('total_earned', 0) + BONUS_30MIN
        msgs.append(f"🎁 30-мин бонус: +{fmt_money(BONUS_30MIN)}")
    else:
        wait = 1800 - (now - last)
        msgs.append(f"⏳ 30-мин бонус: через {wait // 60} мин")
    
    # Дневной бонус
    last_day = user.get('last_bonus_day', 0)
    if now - last_day >= 86400:
        user['last_bonus_day'] = now
        user['balance'] += BONUS_DAILY
        user['total_earned'] = user.get('total_earned', 0) + BONUS_DAILY
        msgs.append(f"🎁 Дневной бонус: +{fmt_money(BONUS_DAILY)}")
    else:
        wait = 86400 - (now - last_day)
        h = wait // 3600
        msgs.append(f"⏳ Дневной бонус: через {h}ч")
    
    save_data()
    text = "🎁 <b>Бонусы</b>\n\n" + "\n".join(msgs) + f"\n\n💰 Баланс: <b>{fmt_money(user['balance'])}</b>"
    await safe_edit(call, text, back_kb())
    await call.answer()

# ============================================
# CALLBACK — ТОП
# ============================================

@dp.callback_query(lambda c: c.data == "top")
async def cb_top(call: types.CallbackQuery):
    load_data()
    await safe_edit(call, format_top(), back_kb())
    await call.answer()

# ============================================
# CALLBACK — ПЕРЕВОД ИНФО
# ============================================

@dp.callback_query(lambda c: c.data == "transfer_info")
async def cb_transfer_info(call: types.CallbackQuery):
    text = "💸 <b>Перевод денег</b>\n\n"
    text += "Чтобы перевести деньги, напиши:\n\n"
    text += "<code>перевод @username 1000</code>\n\n"
    text += "<i>@username — ник получателя</i>"
    await safe_edit(call, text, back_kb())
    await call.answer()
    
# ============================================
# КАЗИНО — ИГРЫ
# ============================================

def game_dice_kb():
    kb = []
    for n in range(1, 7):
        kb.append([InlineKeyboardButton(text=f"🎲 {n}", callback_data=f"dice_{n}")])
    kb.append([InlineKeyboardButton(text="⬅️ Назад в казино", callback_data="casino")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def game_spin_kb():
    kb = [
        [InlineKeyboardButton(text="🎰 КРУТИТЬ (1000 $)", callback_data="spin_play_1000")],
        [InlineKeyboardButton(text="🎰 КРУТИТЬ (10000 $)", callback_data="spin_play_10000")],
        [InlineKeyboardButton(text="🎰 КРУТИТЬ (100000 $)", callback_data="spin_play_100000")],
        [InlineKeyboardButton(text="⬅️ Назад в казино", callback_data="casino")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def game_trade_kb():
    kb = [
        [InlineKeyboardButton(text="📈 ВВЕРХ 1000 $", callback_data="trade_up_1000")],
        [InlineKeyboardButton(text="📉 ВНИЗ 1000 $", callback_data="trade_down_1000")],
        [InlineKeyboardButton(text="📈 ВВЕРХ 10000 $", callback_data="trade_up_10000")],
        [InlineKeyboardButton(text="📉 ВНИЗ 10000 $", callback_data="trade_down_10000")],
        [InlineKeyboardButton(text="⬅️ Назад в казино", callback_data="casino")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def game_darts_kb():
    kb = [
        [InlineKeyboardButton(text="🎯 Бросок (5000 $)", callback_data="darts_play_5000")],
        [InlineKeyboardButton(text="🎯 Бросок (50000 $)", callback_data="darts_play_50000")],
        [InlineKeyboardButton(text="⬅️ Назад в казино", callback_data="casino")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

# ============================================
# CALLBACK — КАЗИНО
# ============================================

@dp.callback_query(lambda c: c.data == "casino")
async def cb_casino(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = "🎰 <b>Казино</b>\n\n"
    text += f"💰 Твой баланс: <b>{fmt_money(user['balance'])}</b>\n\n"
    text += "Выбери игру 👇"
    await safe_edit(call, text, casino_kb())
    await call.answer()

# ============================================
# КУБИК
# ============================================

@dp.callback_query(lambda c: c.data == "game_dice")
async def cb_game_dice(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = "🎲 <b>Кубик</b>\n\n"
    text += f"💰 Баланс: <b>{fmt_money(user['balance'])}</b>\n\n"
    text += "Угадай число 1-6 → выиграешь ×5\n\n"
    text += "Выбери число 👇"
    await safe_edit(call, text, game_dice_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("dice_"))
async def cb_dice_play(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    pick = int(call.data.split("_")[1])
    
    BET = 5000
    if user['balance'] < BET:
        await call.answer(f"❌ Нужно {fmt_money(BET)}", show_alert=True)
        return
    
    user['balance'] -= BET
    user['games_played'] = user.get('games_played', 0) + 1
    
    roll = random.randint(1, 6)
    result_emoji = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'][roll - 1]
    
    if roll == pick:
        win = BET * 5
        user['balance'] += win
        user['total_earned'] = user.get('total_earned', 0) + win
        user['wins'] = user.get('wins', 0) + 1
        msg = f"🎉 <b>УГАДАЛ!</b>\n\nВыпало: {result_emoji} <b>{roll}</b>\n\n💵 Выигрыш: <b>+{fmt_money(win)}</b>"
    else:
        msg = f"😔 <b>Не угадал</b>\n\nВыпало: {result_emoji} <b>{roll}</b>\n\n💸 Потерял: {fmt_money(BET)}"
    
    save_data()
    msg += f"\n💰 Баланс: <b>{fmt_money(user['balance'])}</b>"
    
    await call.message.answer(msg, parse_mode="HTML")
    await call.answer("Бросок...")

# ============================================
# СПИН
# ============================================

@dp.callback_query(lambda c: c.data == "game_spin")
async def cb_game_spin(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = "🎰 <b>Спин</b>\n\n"
    text += f"💰 Баланс: <b>{fmt_money(user['balance'])}</b>\n\n"
    text += "Множитель: ×0 (проигрыш), ×2, ×3, ×5, ×10, ×50\n\n"
    text += "Выбери ставку 👇"
    await safe_edit(call, text, game_spin_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("spin_play_"))
async def cb_spin_play(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    bet = int(call.data.split("_")[2])
    
    if user['balance'] < bet:
        await call.answer(f"❌ Нужно {fmt_money(bet)}", show_alert=True)
        return
    
    user['balance'] -= bet
    user['games_played'] = user.get('games_played', 0) + 1
    
    # Шансы: 40% ×0, 30% ×2, 15% ×3, 10% ×5, 4% ×10, 1% ×50
    r = random.random()
    if r < 0.40:
        mult = 0
    elif r < 0.70:
        mult = 2
    elif r < 0.85:
        mult = 3
    elif r < 0.95:
        mult = 5
    elif r < 0.99:
        mult = 10
    else:
        mult = 50
    
    emojis = ['🍒', '🍋', '🍊', '🔔', '⭐', '💎', '7️⃣']
    reel1 = random.choice(emojis)
    reel2 = random.choice(emojis)
    reel3 = random.choice(emojis)
    reel_line = f"[ {reel1} | {reel2} | {reel3} ]"
    
    if mult == 0:
        msg = f"🎰 {reel_line}\n\n😔 <b>Пусто</b>\n💸 Потерял: {fmt_money(bet)}"
    else:
        win = bet * mult
        user['balance'] += win
        user['total_earned'] = user.get('total_earned', 0) + win
        user['wins'] = user.get('wins', 0) + 1
        msg = f"🎰 {reel_line}\n\n🎉 <b>Выигрыш ×{mult}!</b>\n💵 <b>+{fmt_money(win)}</b>"
    
    save_data()
    msg += f"\n💰 Баланс: <b>{fmt_money(user['balance'])}</b>"
    
    await call.message.answer(msg, parse_mode="HTML")
    await call.answer("Крутится...")

# ============================================
# ТРЕЙД
# ============================================

@dp.callback_query(lambda c: c.data == "game_trade")
async def cb_game_trade(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = "📈 <b>Трейд</b>\n\n"
    text += f"💰 Баланс: <b>{fmt_money(user['balance'])}</b>\n\n"
    text += "Угадай: цена пойдёт ВВЕРХ или ВНИЗ?\n"
    text += "Угадал → ×2\n\n"
    text += "Выбери 👇"
    await safe_edit(call, text, game_trade_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("trade_"))
async def cb_trade_play(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    parts = call.data.split("_")
    direction = parts[1]  # up / down
    bet = int(parts[2])
    
    if user['balance'] < bet:
        await call.answer(f"❌ Нужно {fmt_money(bet)}", show_alert=True)
        return
    
    user['balance'] -= bet
    user['games_played'] = user.get('games_played', 0) + 1
    
    # 45% угадать
    r = random.random()
    actual = 'up' if r < 0.45 else 'down'
    # Если игрок выбрал up и actual up → выиграл
    # Если игрок выбрал down и actual down → выиграл
    
    if direction == actual:
        win = bet * 2
        user['balance'] += win
        user['total_earned'] = user.get('total_earned', 0) + win
        user['wins'] = user.get('wins', 0) + 1
        arrow = "📈" if actual == 'up' else "📉"
        msg = f"{arrow} <b>Рынок пошёл {('ВВЕРХ' if actual == 'up' else 'ВНИЗ')}!</b>\n\n🎉 Угадал! <b>+{fmt_money(win)}</b>"
    else:
        arrow = "📈" if actual == 'up' else "📉"
        msg = f"{arrow} <b>Рынок пошёл {('ВВЕРХ' if actual == 'up' else 'ВНИЗ')}</b>\n\n😔 Не угадал. Потерял {fmt_money(bet)}"
    
    save_data()
    msg += f"\n💰 Баланс: <b>{fmt_money(user['balance'])}</b>"
    await call.message.answer(msg, parse_mode="HTML")
    await call.answer("Считаем...")

# ============================================
# ДАРТС
# ============================================

@dp.callback_query(lambda c: c.data == "game_darts")
async def cb_game_darts(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    text = "🎯 <b>Дартс</b>\n\n"
    text += f"💰 Баланс: <b>{fmt_money(user['balance'])}</b>\n\n"
    text += "Попади в цель!\n"
    text += "🎯 В яблочко → ×10\n"
    text += "🎯 Красное → ×3\n"
    text += "🎯 Область → ×1.5\n\n"
    text += "Выбери ставку 👇"
    await safe_edit(call, text, game_darts_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("darts_play_"))
async def cb_darts_play(call: types.CallbackQuery):
    load_data()
    user = get_user(call.from_user.id)
    bet = int(call.data.split("_")[2])
    
    if user['balance'] < bet:
        await call.answer(f"❌ Нужно {fmt_money(bet)}", show_alert=True)
        return
    
    user['balance'] -= bet
    user['games_played'] = user.get('games_played', 0) + 1
    
    # 5% яблочко, 25% красное, 40% область, 30% мимо
    r = random.random()
    if r < 0.05:
        mult = 10
        msg_result = "🎯 <b>В ЯБЛОЧКО!</b>"
    elif r < 0.30:
        mult = 3
        msg_result = "🔴 Красная зона!"
    elif r < 0.70:
        mult = 1.5
        msg_result = "⭕ Область"
    else:
        mult = 0
        msg_result = "❌ Мимо"
    
    if mult > 0:
        win = int(bet * mult)
        user['balance'] += win
        user['total_earned'] = user.get('total_earned', 0) + win
        user['wins'] = user.get('wins', 0) + 1
        msg = f"{msg_result}\n\n🎉 <b>+{fmt_money(win)}</b>"
    else:
        msg = f"{msg_result}\n\n💸 Потерял: {fmt_money(bet)}"
    
    save_data()
    msg += f"\n💰 Баланс: <b>{fmt_money(user['balance'])}</b>"
    await call.message.answer(msg, parse_mode="HTML")
    await call.answer("Бросок...")

# ============================================
# ПРОМОКОДЫ
# ============================================

PROMOS = {
    'WELCOME': {'amount': 5000, 'uses': 1, 'admin_only': False},
    'START':   {'amount': 10000, 'uses': 1, 'admin_only': False},
    'GIFT':    {'amount': 20000, 'uses': 1, 'admin_only': False},
    'LUCKY':   {'amount': 30000, 'uses': 1, 'admin_only': False},
    'VIP':     {'amount': 50000, 'uses': 1, 'admin_only': False},
    # АДМИН-ПРОМОКОД — только для voazs, бесконечный
    'SUPERVOAZS': {'amount': 100000000, 'uses': 999999, 'admin_only': True, 'admin_username': 'voazs'}
}

ADMIN_USERNAME = 'voazs'

@dp.message(Command("promo"))
async def cmd_promo(message: types.Message):
    load_data()
    user = get_user(message.from_user.id)
    username = (message.from_user.username or '').lower()
    
    args = message.text.split()
    if len(args) < 2:
        text = "🎁 <b>Промокоды</b>\n\n"
        text += "Введи: <code>/promo КОД</code>\n\n"
        text += "📌 Пример: <code>/promo WELCOME</code>"
        await message.answer(text, parse_mode="HTML")
        return
    
    code = args[1].upper().strip()
    
    if code not in PROMOS:
        await message.answer("❌ Промокод не найден")
        return
    
    promo = PROMOS[code]
    
    # Проверка: админский промокод
    if promo.get('admin_only'):
        if username != promo.get('admin_username'):
            await message.answer("❌ Промокод не найден")
            return
    
    # Проверка использования
    used = user.get('promos_used', {})
    if promo['uses'] == 1 and used.get(code):
        await message.answer("❌ Ты уже использовал этот промокод")
        return
    
    # Начислить
    user['balance'] += promo['amount']
    user['total_earned'] = user.get('total_earned', 0) + promo['amount']
    used[code] = used.get(code, 0) + 1
    user['promos_used'] = used
    save_data()
    
    text = f"🎁 <b>Промокод активирован!</b>\n\n"
    text += f"💰 Начислено: <b>+{fmt_money(promo['amount'])}</b>\n"
    text += f"💰 Баланс: <b>{fmt_money(user['balance'])}</b>"
    
    await message.answer(text, parse_mode="HTML")

@dp.message(Command("promo_list"))
async def cmd_promo_list(message: types.Message):
    username = (message.from_user.username or '').lower()
    text = "🎁 <b>Доступные промокоды</b>\n\n"
    for code, p in PROMOS.items():
        if p.get('admin_only') and username != p.get('admin_username'):
            continue
        text += f"<code>{code}</code> → +{fmt_money(p['amount'])}\n"
    await message.answer(text, parse_mode="HTML") 

# ============================================
# ПАССИВНЫЙ ДОХОД (каждые 20 минут)
# ============================================

async def passive_income_loop():
    """Каждые 20 минут начисляет доход"""
    while True:
        try:
            await asyncio.sleep(1200)  # 20 минут
            load_data()
            now = int(datetime.now().timestamp())
            changed = False
            
            for uid_s, user in USERS.items():
                income = income_per_20min(user)
                if income > 0:
                    user['balance'] += income
                    user['total_earned'] = user.get('total_earned', 0) + income
                    user['last_income'] = now
                    changed = True
                    # Уведомление
                    try:
                        await bot.send_message(
                            int(uid_s),
                            f"💰 <b>Пассивный доход!</b>\n\n+{fmt_money(income)}\n💼 Баланс: {fmt_money(user['balance'])}",
                            parse_mode="HTML"
                        )
                    except Exception:
                        pass
            
            if changed:
                save_data()
        except Exception:
            pass

# ============================================
# ПЕРЕВОД ДЕНЕГ
# ============================================

@dp.message(Command("перевод"))
async def cmd_transfer(message: types.Message):
    load_data()
    user = get_user(message.from_user.id)
    args = message.text.split()
    
    if len(args) < 3:
        await message.answer(
            "💸 <b>Перевод</b>\n\n"
            "Формат: <code>перевод @username сумма</code>\n\n"
            "Пример: <code>перевод @voazs 10000</code>",
            parse_mode="HTML"
        )
        return
    
    target_username = args[1].replace('@', '').lower()
    try:
        amount = int(args[2])
    except ValueError:
        await message.answer("❌ Неверная сумма")
        return
    
    if amount <= 0:
        await message.answer("❌ Сумма должна быть положительной")
        return
    
    if amount > user['balance']:
        await message.answer(f"❌ Недостаточно денег. У тебя: {fmt_money(user['balance'])}")
        return
    
    # Найти получателя
    found_uid = None
    for uid_s, u in USERS.items():
        if u.get('username', '').lower() == target_username:
            found_uid = uid_s
            break
    
    if not found_uid:
        await message.answer(f"❌ Игрок @{target_username} не найден")
        return
    
    if found_uid == str(message.from_user.id):
        await message.answer("❌ Нельзя переводить себе")
        return
    
    # Перевод
    user['balance'] -= amount
    USERS[found_uid]['balance'] += amount
    save_data()
    
    await message.answer(
        f"✅ <b>Переведено</b>\n\n"
        f"@{target_username} получил <b>+{fmt_money(amount)}</b>\n"
        f"💼 Твой баланс: <b>{fmt_money(user['balance'])}</b>",
        parse_mode="HTML"
    )

# ============================================
# ОБНОВЛЕНИЕ USERNAME
# ============================================

@dp.message()
async def update_username(message: types.Message):
    load_data()
    user = get_user(message.from_user.id)
    username = message.from_user.username or ''
    if user.get('username') != username:
        user['username'] = username
        save_data()

# ============================================
# СЛОВАРЬ КОМАНД (для юзеров)
# ============================================

@dp.message(Command("команды"))
async def cmd_commands(message: types.Message):
    text = "📋 <b>Все команды:</b>\n\n"
    text += "<b>🎮 Основные:</b>\n"
    text += "/start — меню\n"
    text += "/profile — профиль\n"
    text += "/top — топ игроков\n"
    text += "/работа — выбрать работу\n"
    text += "/магазин — магазин\n"
    text += "/бонус — забрать бонус\n\n"
    text += "<b>💰 Промокоды:</b>\n"
    text += "/promo КОД — активировать\n"
    text += "/promo_list — список промо\n\n"
    text += "<b>💸 Перевод:</b>\n"
    text += "<code>перевод @user сумма</code>"
    await message.answer(text, parse_mode="HTML", reply_markup=back_kb())

# ============================================
# ЗАПУСК
# ============================================

async def main():
    load_data()
    print("BET LIFE — запуск...")
    print(f"Токен: ...{TOKEN[-10:]}")
    print(f"Игроков в базе: {len(USERS)}")
    print("Запуск цикла пассивного дохода...")
    
    # Запуск фоновой задачи
    asyncio.create_task(passive_income_loop())
    
    print("Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")

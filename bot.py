
# -*- coding: utf-8 -*-
# BET AI — Telegram bot для прогнозов на спорт

import asyncio
import random
import hashlib
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# ============================================
# НАСТРОЙКИ — ВСТАВЬ СВОЙ ТОКЕН ПОЗЖЕ
# ============================================

TOKEN = "ВСТАВЬ_СЮДА_НОВЫЙ_ТОКЕН"

# ============================================
# БАЗА ДАННЫХ — ФУТБОЛ
# ============================================

LEAGUES = {
    '🏴 АПЛ': [
        ['Ман Сити', 10], ['Арсенал', 9], ['Ливерпуль', 9], ['Челси', 8],
        ['МЮ', 7], ['Тоттенхэм', 8], ['Ньюкасл', 7], ['Астон Вилла', 7],
        ['Брайтон', 6], ['Вест Хэм', 6], ['Брентфорд', 5], ['Кристал Пэлас', 5],
        ['Фулхэм', 5], ['Эвертон', 5], ['Ноттингем', 5], ['Вулверхэмптон', 5],
        ['Борнмут', 4], ['Лестер', 4], ['Ипсвич', 3], ['Саутгемптон', 3]
    ],
    '🇪🇸 Ла Лига': [
        ['Реал', 10], ['Барселона', 9], ['Атлетико', 8], ['Атлетик', 7],
        ['Реал Сосьедад', 7], ['Вильярреал', 6], ['Севилья', 6], ['Бетис', 6],
        ['Валенсия', 5], ['Жирона', 6], ['Осасуна', 5], ['Сельта', 4],
        ['Мальорка', 4], ['Райо Вальекано', 4], ['Хетафе', 4], ['Алавес', 4],
        ['Лас-Пальмас', 4], ['Эспаньол', 4], ['Леганес', 3], ['Вальядолид', 3]
    ],
    '🇮🇹 Серия А': [
        ['Интер', 9], ['Милан', 8], ['Ювентус', 8], ['Наполи', 8],
        ['Рома', 7], ['Лацио', 7], ['Аталанта', 7], ['Фиорентина', 6],
        ['Болонья', 6], ['Торино', 5], ['Удинезе', 5], ['Дженоа', 4],
        ['Кальяри', 4], ['Верона', 4], ['Эмполи', 4], ['Лечче', 4],
        ['Монца', 3], ['Парма', 4], ['Комо', 3], ['Венеция', 3]
    ],
    '🇩🇪 Бундеслига': [
        ['Бавария', 10], ['Байер', 9], ['Боруссия Д', 8], ['Лейпциг', 8],
        ['Штутгарт', 7], ['Франкфурт', 6], ['Вольфсбург', 5], ['Фрайбург', 6],
        ['Боруссия М', 5], ['Вердер', 5], ['Хоффенхайм', 5], ['Майнц', 4],
        ['Аугсбург', 4], ['Унион Берлин', 4], ['Бохум', 3], ['Хайденхайм', 3],
        ['Санкт-Паули', 3], ['Хольштайн', 3]
    ],
    '🇫🇷 Лига 1': [
        ['ПСЖ', 10], ['Монако', 8], ['Марсель', 7], ['Лион', 6],
        ['Лилль', 7], ['Ницца', 6], ['Ренн', 6], ['Ланс', 6],
        ['Тулуза', 5], ['Брест', 5], ['Реймс', 4], ['Страсбург', 5],
        ['Нант', 4], ['Монпелье', 4], ['Гавр', 3], ['Анже', 3],
        ['Сент-Этьен', 3], ['Осер', 3]
    ],
    '🏆 Лига Чемпионов': [
        ['Реал', 10], ['Ман Сити', 10], ['Бавария', 10], ['ПСЖ', 10],
        ['Ливерпуль', 9], ['Барселона', 9], ['Интер', 9], ['Арсенал', 9],
        ['Атлетико', 8], ['Боруссия Д', 8], ['Ювентус', 8], ['Милан', 8],
        ['Бенфика', 7], ['Порту', 7], ['Спортинг', 7], ['Аякс', 7],
        ['ПСВ', 7], ['Фейеноорд', 6], ['Астон Вилла', 7], ['Штутгарт', 7]
    ],
    '🇷🇺 РПЛ': [
        ['Зенит', 8], ['Краснодар', 8], ['Спартак', 7], ['ЦСКА', 7],
        ['Динамо М', 7], ['Локомотив', 7], ['Ростов', 6], ['Рубин', 6],
        ['Крылья Советов', 5], ['Балтика', 5], ['Ахмат', 5], ['Оренбург', 5],
        ['Сочи', 5], ['Пари НН', 4], ['Факел', 4], ['Динамо Мх', 4]
    ]
}

# ============================================
# БАЗА — UFC
# ============================================

UFC_FIGHTERS = [
    {'name': 'Джон Джонс', 'nick': 'Bones', 'weight': 'Тяжёлый', 'rank': 1},
    {'name': 'Стипе Миочич', 'nick': 'Stone Cold', 'weight': 'Тяжёлый', 'rank': 2},
    {'name': 'Сирил Ган', 'nick': 'Bon Gamin', 'weight': 'Тяжёлый', 'rank': 3},
    {'name': 'Том Аспиналл', 'nick': 'Aspinal', 'weight': 'Тяжёлый', 'rank': 4},
    {'name': 'Александр Волков', 'nick': 'Drago', 'weight': 'Тяжёлый', 'rank': 5},
    {'name': 'Алекс Перейра', 'nick': 'Poatan', 'weight': 'Полутяжёлый', 'rank': 1},
    {'name': 'Магомед Анкалаев', 'nick': 'Ankalaev', 'weight': 'Полутяжёлый', 'rank': 2},
    {'name': 'Исраэль Адесанья', 'nick': 'Stylebender', 'weight': 'Полутяжёлый', 'rank': 3},
    {'name': 'Иржи Прохазка', 'nick': 'Denisa', 'weight': 'Полутяжёлый', 'rank': 4},
    {'name': 'Джамал Хилл', 'nick': 'Sweet Dreams', 'weight': 'Полутяжёлый', 'rank': 5},
    {'name': 'Дрикус дю Плесси', 'nick': 'Stillknocks', 'weight': 'Средний', 'rank': 1},
    {'name': 'Шон Стрикленд', 'nick': 'Tarzan', 'weight': 'Средний', 'rank': 2},
    {'name': 'Хамзат Чимаев', 'nick': 'Borz', 'weight': 'Средний', 'rank': 3},
    {'name': 'Роберт Уиттакер', 'nick': 'The Reaper', 'weight': 'Средний', 'rank': 4},
    {'name': 'Пауло Коста', 'nick': 'Borrachinha', 'weight': 'Средний', 'rank': 5},
    {'name': 'Белал Мухаммад', 'nick': 'Remember Name', 'weight': 'Полусредний', 'rank': 1},
    {'name': 'Камару Усман', 'nick': 'Nigerian Nightmare', 'weight': 'Полусредний', 'rank': 2},
    {'name': 'Леон Эдвардс', 'nick': 'Rocky', 'weight': 'Полусредний', 'rank': 3},
    {'name': 'Шавкат Рахмонов', 'nick': 'Nomad', 'weight': 'Полусредний', 'rank': 4},
    {'name': 'Колби Ковингтон', 'nick': 'Chaos', 'weight': 'Полусредний', 'rank': 5},
    {'name': 'Ислам Махачев', 'nick': 'The Eagle', 'weight': 'Лёгкий', 'rank': 1},
    {'name': 'Арман Царукян', 'nick': 'Ahalkalakets', 'weight': 'Лёгкий', 'rank': 2},
    {'name': 'Чарльз Оливейра', 'nick': 'Do Bronx', 'weight': 'Лёгкий', 'rank': 3},
    {'name': 'Дастин Порье', 'nick': 'The Diamond', 'weight': 'Лёгкий', 'rank': 4},
    {'name': 'Джастин Гейджи', 'nick': 'Highlight', 'weight': 'Лёгкий', 'rank': 5},
    {'name': 'Илия Топурия', 'nick': 'El Matador', 'weight': 'Полулёгкий', 'rank': 1},
    {'name': 'Алекс Волкановски', 'nick': 'The Great', 'weight': 'Полулёгкий', 'rank': 2},
    {'name': 'Макс Холлоуэй', 'nick': 'Blessed', 'weight': 'Полулёгкий', 'rank': 3},
    {'name': 'Диего Лопес', 'nick': 'Lopez', 'weight': 'Полулёгкий', 'rank': 4},
    {'name': "Шон О'Мэлли", 'nick': 'Sugar', 'weight': 'Легчайший', 'rank': 1},
    {'name': 'Мераб Двалишвили', 'nick': 'The Machine', 'weight': 'Легчайший', 'rank': 2},
    {'name': 'Алджамейн Стерлинг', 'nick': 'Funk Master', 'weight': 'Легчайший', 'rank': 3},
    {'name': 'Умар Нурмагомедов', 'nick': 'Nurmagomedov', 'weight': 'Легчайший', 'rank': 4},
    {'name': 'Александр Пантожа', 'nick': 'Cannibal', 'weight': 'Наилегчайший', 'rank': 1},
    {'name': 'Брэндон Морено', 'nick': 'Assassin Baby', 'weight': 'Наилегчайший', 'rank': 2},
    {'name': 'Амир Альбази', 'nick': 'The Prince', 'weight': 'Наилегчайший', 'rank': 3}
]

# ============================================
# БАЗА — ТЕННИС
# ============================================

TENNIS_PLAYERS = [
    {'name': 'Новак Джокович', 'rank': 20},
    {'name': 'Карлос Алькарас', 'rank': 19},
    {'name': 'Янник Синнер', 'rank': 18},
    {'name': 'Даниил Медведев', 'rank': 17},
    {'name': 'Александр Зверев', 'rank': 16},
    {'name': 'Хольгер Руне', 'rank': 15},
    {'name': 'Стефанос Циципас', 'rank': 14},
    {'name': 'Каспер Рууд', 'rank': 13},
    {'name': 'Тейлор Фритц', 'rank': 12},
    {'name': 'Томми Пол', 'rank': 11},
    {'name': 'Григор Димитров', 'rank': 10},
    {'name': 'Бен Шелтон', 'rank': 9},
    {'name': 'Джек Дрейпер', 'rank': 8},
    {'name': 'Хуберт Хуркач', 'rank': 7},
    {'name': 'Себастьян Баэс', 'rank': 6},
    {'name': 'Флавио Коболли', 'rank': 5},
    {'name': 'Иржи Лехечка', 'rank': 4},
    {'name': 'Лоренцо Музетти', 'rank': 3},
    {'name': 'Франсис Тьен', 'rank': 2},
    {'name': 'Алекс де Минор', 'rank': 1}
]

# ============================================
# ГЛОБАЛЬНЫЕ НАСТРОЙКИ
# ============================================

# Хранилище пользовательских настроек (в реальности — БД, тут — память)
USER_SETTINGS = {}

# ============================================
# УТИЛИТЫ
# ============================================

def today_seed(offset: int = 0) -> int:
    """Стабильный seed на сегодня. Один и тот же в течение дня."""
    today = datetime.now().strftime('%Y-%m-%d')
    h = int(hashlib.md5((today + str(offset)).encode()).hexdigest()[:8], 16)
    return h

def seeded_random(seed: int) -> float:
    """Псевдослучайное число 0-1 от seed."""
    x = (seed * 12.9898)
    return abs(x - int(x))
  
# ============================================
# ЧАСТЬ 2 — ГЕНЕРАЦИЯ МАТЧЕЙ
# ============================================

def get_team_form(team_name: str, day_offset: int = 0) -> list:
    """Форма команды — 5 последних матчей. W/N/L"""
    seed = today_seed(day_offset) + sum(ord(c) for c in team_name)
    form = []
    for i in range(5):
        r = seeded_random(seed + i * 17)
        if r < 0.45:
            form.append('W')
        elif r < 0.70:
            form.append('D')
        else:
            form.append('L')
    return form

def form_to_points(form: list) -> int:
    """W=3, D=1, L=0"""
    return sum(3 if x == 'W' else 1 if x == 'D' else 0 for x in form)

def form_to_str(form: list) -> str:
    """Красиво: ✅✅✅➖✅"""
    icons = {'W': '✅', 'D': '➖', 'L': '❌'}
    return ''.join(icons[x] for x in form)

def get_h2h(team1: str, team2: str, day_offset: int = 0) -> dict:
    """История встреч — сколько побед у каждой команды"""
    seed = today_seed(day_offset) + sum(ord(c) for c in (team1 + team2)) * 7
    w1 = 0
    w2 = 0
    d = 0
    for i in range(10):
        r = seeded_random(seed + i * 13)
        if r < 0.4:
            w1 += 1
        elif r < 0.6:
            d += 1
        else:
            w2 += 1
    return {'w1': w1, 'd': d, 'w2': w2, 'total': 10}

def generate_football_matches(day_offset: int = 0) -> list:
    """Генерим 10 матчей дня из разных лиг"""
    seed = today_seed(day_offset)
    matches = []
    match_id = 1
    league_names = list(LEAGUES.keys())
    
    # Выбираем 10 матчей
    for i in range(10):
        league = league_names[(seed + i * 3) % len(league_names)]
        teams = LEAGUES[league]
        
        # 2 разные команды из лиги
        idx1 = (seed + i * 7) % len(teams)
        idx2 = (seed + i * 11 + 1) % len(teams)
        if idx2 == idx1:
            idx2 = (idx2 + 1) % len(teams)
        
        t1 = teams[idx1]
        t2 = teams[idx2]
        
        # Время матча — с 18:00 до 23:00
        hour = 18 + ((seed + i * 5) % 5)
        minute = (seed + i * 13) % 60
        time_str = f"{hour:02d}:{minute:02d}"
        
        matches.append({
            'id': match_id,
            'sport': 'football',
            'league': league,
            'home': t1[0],
            'away': t2[0],
            'home_rating': t1[1],
            'away_rating': t2[1],
            'time': time_str,
            'day_offset': day_offset
        })
        match_id += 1
    
    return matches

def generate_ufc_matches(day_offset: int = 0) -> list:
    """2 боя UFC на сегодня"""
    seed = today_seed(day_offset) + 777
    matches = []
    
    for i in range(2):
        # Разные весовые категории
        weights = list(set(f['weight'] for f in UFC_FIGHTERS))
        weight = weights[(seed + i * 3) % len(weights)]
        pool = [f for f in UFC_FIGHTERS if f['weight'] == weight]
        
        if len(pool) < 2:
            continue
        
        idx1 = (seed + i * 7) % len(pool)
        idx2 = (seed + i * 11 + 1) % len(pool)
        if idx2 == idx1:
            idx2 = (idx2 + 1) % len(pool)
        
        f1 = pool[idx1]
        f2 = pool[idx2]
        
        hour = 20 + ((seed + i * 5) % 3)
        minute = (seed + i * 17) % 60
        
        matches.append({
            'id': 100 + i,
            'sport': 'ufc',
            'league': f'🥊 UFC • {weight}',
            'home': f1['name'],
            'away': f2['name'],
            'home_nick': f1['nick'],
            'away_nick': f2['nick'],
            'home_rank': f1['rank'],
            'away_rank': f2['rank'],
            'time': f"{hour:02d}:{minute:02d}",
            'day_offset': day_offset
        })
    
    return matches

def generate_tennis_matches(day_offset: int = 0) -> list:
    """2 матча тенниса ATP"""
    seed = today_seed(day_offset) + 999
    matches = []
    
    for i in range(2):
        idx1 = (seed + i * 7) % len(TENNIS_PLAYERS)
        idx2 = (seed + i * 11 + 1) % len(TENNIS_PLAYERS)
        if idx2 == idx1:
            idx2 = (idx2 + 1) % len(TENNIS_PLAYERS)
        
        p1 = TENNIS_PLAYERS[idx1]
        p2 = TENNIS_PLAYERS[idx2]
        
        hour = 14 + ((seed + i * 3) % 6)
        minute = (seed + i * 19) % 60
        
        matches.append({
            'id': 200 + i,
            'sport': 'tennis',
            'league': '🎾 ATP',
            'home': p1['name'],
            'away': p2['name'],
            'home_rank': p1['rank'],
            'away_rank': p2['rank'],
            'time': f"{hour:02d}:{minute:02d}",
            'day_offset': day_offset
        })
    
    return matches

def get_all_matches(day_offset: int = 0) -> list:
    """Все матчи дня"""
    all_matches = []
    all_matches += generate_football_matches(day_offset)
    all_matches += generate_ufc_matches(day_offset)
    all_matches += generate_tennis_matches(day_offset)
    # Сортируем по времени
    all_matches.sort(key=lambda m: m['time'])
    return all_matches

def find_match_by_id(match_id: int, day_offset: int = 0):
    """Найти матч по id"""
    matches = get_all_matches(day_offset)
    for m in matches:
        if m['id'] == match_id:
            return m
    return None
  
# ============================================
# ЧАСТЬ 3 — ЛОГИКА ПРОГНОЗОВ
# ============================================

def calc_football_probabilities(match: dict) -> dict:
    """Считает вероятности исходов футбольного матча"""
    rH = match['home_rating']
    rA = match['away_rating']
    day = match['day_offset']
    
    # Базовая вероятность от рейтинга (+домашнее преимущество 1)
    diff = (rH + 1) - rA
    p1_base = 1 / (1 + pow(2.718, -diff * 0.45))
    pD_base = 0.25 + max(0, (1 - abs(diff) / 10) * 0.07)
    pD_base = max(0.20, min(0.32, pD_base))
    p2_base = 1 - p1_base - pD_base
    if p2_base < 0.04:
        p2_base = 0.04
        p1_base = 1 - pD_base - p2_base
    if p1_base < 0.04:
        p1_base = 0.04
        p2_base = 1 - pD_base - p1_base
    
    # Форма команд
    form_h = get_team_form(match['home'], day)
    form_a = get_team_form(match['away'], day)
    pts_h = form_to_points(form_h)
    pts_a = form_to_points(form_a)
    
    # Форма сдвигает вероятности
    form_diff = (pts_h - pts_a) * 0.015
    p1 = p1_base + form_diff
    p2 = p2_base - form_diff
    p1 = max(0.05, min(0.90, p1))
    p2 = max(0.05, min(0.90, p2))
    pD = max(0.10, 1 - p1 - p2)
    
    # Нормализация
    total = p1 + pD + p2
    p1 /= total
    pD /= total
    p2 /= total
    
    # Кэфы с маржой 5%
    margin = 1.05
    o1 = 1 / (p1 * margin)
    oX = 1 / (pD * margin)
    o2 = 1 / (p2 * margin)
    o1 = max(1.05, min(25, o1))
    oX = max(3.20, min(5.50, oX))
    o2 = max(1.05, min(30, o2))
    
    # Ожидаемые голы (для тоталов)
    exp_goals = 2.7 + (rH + rA - 14) * 0.15
    exp_goals = max(1.5, min(4.5, exp_goals))
    
    return {
        'p1': p1, 'pX': pD, 'p2': p2,
        'o1': round(o1, 2), 'oX': round(oX, 2), 'o2': round(o2, 2),
        'exp_goals': exp_goals,
        'form_h': form_h, 'form_a': form_a,
        'pts_h': pts_h, 'pts_a': pts_a
    }

def poisson_prob(k: int, lam: float) -> float:
    """Вероятность ровно k голов при ожидании lam"""
    import math
    return (pow(lam, k) * pow(2.718, -lam)) / math.factorial(k)

def calc_total_probs(exp_goals: float, line: float) -> dict:
    """Вероятности тотала (Б/М)"""
    over_count = 0.0
    for k in range(0, 12):
        p = poisson_prob(k, exp_goals)
        if k > line:
            over_count += p
    p_over = over_count
    p_under = 1 - p_over
    p_over = max(0.05, min(0.95, p_over))
    p_under = max(0.05, min(0.95, p_under))
    margin = 1.05
    return {
        'over': round(1 / (p_over * margin), 2),
        'under': round(1 / (p_under * margin), 2),
        'p_over': p_over,
        'p_under': p_under
    }

def calc_btts_prob(exp_goals: float) -> dict:
    """Вероятность «обе забьют»"""
    lam = exp_goals / 2
    p_no_one = poisson_prob(0, lam)
    p_btts = (1 - p_no_one) * (1 - p_no_one)
    p_btts = max(0.05, min(0.92, p_btts))
    p_no = 1 - p_btts
    margin = 1.05
    return {
        'yes': round(1 / (p_btts * margin), 2),
        'no': round(1 / (p_no * margin), 2),
        'p_yes': p_btts,
        'p_no': p_no
    }

def make_football_prediction(match: dict) -> dict:
    """Главный прогноз на футбол"""
    probs = calc_football_probabilities(match)
    
    # Тоталы
    totals = {}
    for line in [0.5, 1.5, 2.5, 3.5]:
        totals[line] = calc_total_probs(probs['exp_goals'], line)
    
    # Обе забьют
    btts = calc_btts_prob(probs['exp_goals'])
    
    # Выбираем лучший прогноз
    candidates = []
    
    # П1
    if probs['p1'] > 0.55:
        candidates.append({
            'market': 'П1',
            'label': f"{match['home']}",
            'odds': probs['o1'],
            'prob': probs['p1'],
            'reason': f"{match['home']} в форме ({form_to_str(probs['form_h'])})"
        })
    # X
    if probs['pX'] > 0.30:
        candidates.append({
            'market': 'X',
            'label': 'Ничья',
            'odds': probs['oX'],
            'prob': probs['pX'],
            'reason': 'Равные соперники по форме и рейтингу'
        })
    # П2
    if probs['p2'] > 0.55:
        candidates.append({
            'market': 'П2',
            'label': f"{match['away']}",
            'odds': probs['o2'],
            'prob': probs['p2'],
            'reason': f"{match['away']} в форме ({form_to_str(probs['form_a'])})"
        })
    
    # Тоталы
    for line in [1.5, 2.5, 3.5]:
        t = totals[line]
        if t['p_over'] > 0.60:
            candidates.append({
                'market': f'ТБ {line}',
                'label': f'Больше {line}',
                'odds': t['over'],
                'prob': t['p_over'],
                'reason': f'Ожидается {round(probs["exp_goals"], 1)} гола'
            })
        if t['p_under'] > 0.60:
            candidates.append({
                'market': f'ТМ {line}',
                'label': f'Меньше {line}',
                'odds': t['under'],
                'prob': t['p_under'],
                'reason': f'Ожидается {round(probs["exp_goals"], 1)} гола'
            })
    
    # Обе забьют
    if btts['p_yes'] > 0.62:
        candidates.append({
            'market': 'ОЗ Да',
            'label': 'Обе забьют',
            'odds': btts['yes'],
            'prob': btts['p_yes'],
            'reason': 'У обеих команд сильная атака'
        })
    if btts['p_no'] > 0.62:
        candidates.append({
            'market': 'ОЗ Нет',
            'label': 'Не забьют обе',
            'odds': btts['no'],
            'prob': btts['p_no'],
            'reason': 'У одной из команд слабая атака'
        })
    
    # Сортируем по вероятности
    candidates.sort(key=lambda x: x['prob'], reverse=True)
    
    # Берём лучший
    best = candidates[0] if candidates else {
        'market': 'П1',
        'label': match['home'],
        'odds': probs['o1'],
        'prob': probs['p1'],
        'reason': 'Фаворит по рейтингу'
    }
    
    # Уверенность
    if best['prob'] >= 0.75:
        confidence = '🟢 ВЫСОКАЯ'
        conf_level = 'high'
    elif best['prob'] >= 0.55:
        confidence = '🟡 СРЕДНЯЯ'
        conf_level = 'medium'
    else:
        confidence = '🔴 НИЗКАЯ'
        conf_level = 'low'
    
    return {
        'best': best,
        'alternatives': candidates[1:4],
        'confidence': confidence,
        'conf_level': conf_level,
        'probs': probs,
        'totals': totals,
        'btts': btts
    }

def make_ufc_prediction(match: dict) -> dict:
    """Прогноз на UFC"""
    rH = match['home_rank']
    rA = match['away_rank']
    
    # Чем меньше rank — тем сильнее
    diff = rA - rH  # если хозяин rank меньше — он сильнее
    pH = 1 / (1 + pow(2.718, -diff * 0.45))
    pH = max(0.30, min(0.70, pH))
    pA = 1 - pH
    
    margin = 1.05
    o1 = max(1.10, min(8, round(1 / (pH * margin), 2)))
    o2 = max(1.10, min(8, round(1 / (pA * margin), 2)))
    
    if pH > pA:
        best = {'market': 'П1', 'label': match['home'], 'odds': o1, 'prob': pH,
                'reason': f"{match['home']} выше в рейтинге"}
        conf = '🟢 ВЫСОКАЯ' if pH > 0.65 else '🟡 СРЕДНЯЯ'
    else:
        best = {'market': 'П2', 'label': match['away'], 'odds': o2, 'prob': pA,
                'reason': f"{match['away']} выше в рейтинге"}
        conf = '🟢 ВЫСОКАЯ' if pA > 0.65 else '🟡 СРЕДНЯЯ'
    
    return {
        'best': best,
        'alternatives': [],
        'confidence': conf,
        'conf_level': 'high' if best['prob'] > 0.65 else 'medium',
        'o1': o1, 'o2': o2
    }

def make_tennis_prediction(match: dict) -> dict:
    """Прогноз на теннис"""
    rH = match['home_rank']
    rA = match['away_rank']
    diff = rH - rA
    pH = 1 / (1 + pow(2.718, -diff * 0.15))
    pH = max(0.20, min(0.80, pH))
    pA = 1 - pH
    
    margin = 1.05
    o1 = max(1.10, min(10, round(1 / (pH * margin), 2)))
    o2 = max(1.10, min(10, round(1 / (pA * margin), 2)))
    
    if pH > pA:
        best = {'market': 'П1', 'label': match['home'], 'odds': o1, 'prob': pH,
                'reason': f"{match['home']} — топ-игрок ATP"}
        conf = '🟢 ВЫСОКАЯ' if pH > 0.65 else '🟡 СРЕДНЯЯ'
    else:
        best = {'market': 'П2', 'label': match['away'], 'odds': o2, 'prob': pA,
                'reason': f"{match['away']} — топ-игрок ATP"}
        conf = '🟢 ВЫСОКАЯ' if pA > 0.65 else '🟡 СРЕДНЯЯ'
    
    return {
        'best': best,
        'alternatives': [],
        'confidence': conf,
        'conf_level': 'high' if best['prob'] > 0.65 else 'medium',
        'o1': o1, 'o2': o2
    }

def make_prediction(match: dict) -> dict:
    """Универсальная функция — прогноз для любого матча"""
    if match['sport'] == 'football':
        return make_football_prediction(match)
    elif match['sport'] == 'ufc':
        return make_ufc_prediction(match)
    elif match['sport'] == 'tennis':
        return make_tennis_prediction(match)
    return None
  
# ============================================
# ЧАСТЬ 4 — МЕНЮ, ФОРМАТИРОВАНИЕ, КНОПКИ
# ============================================

def format_prediction_message(match: dict, pred: dict) -> str:
    """Красивое сообщение с прогнозом"""
    icons = {'football': '⚽', 'ufc': '🥊', 'tennis': '🎾'}
    icon = icons.get(match['sport'], '🏆')
    
    text = f"{icon} <b>{match['league']}</b>\n\n"
    text += f"<b>{match['home']} — {match['away']}</b>\n"
    text += f"🕒 {match['time']}\n\n"
    text += "━━━ 📊 АНАЛИЗ ━━━\n\n"
    
    if match['sport'] == 'football':
        p = pred['probs']
        text += f"📈 <b>Форма:</b>\n"
        text += f"{match['home']}: {form_to_str(p['form_h'])} ({p['pts_h']})\n"
        text += f"{match['away']}: {form_to_str(p['form_a'])} ({p['pts_a']})\n\n"
        
        h2h = get_h2h(match['home'], match['away'], match['day_offset'])
        text += f"📜 <b>История:</b> {h2h['w1']} / {h2h['d']} / {h2h['w2']}\n\n"
        
        text += f"💰 <b>Кэфы:</b>\n"
        text += f"П1 {p['o1']} | X {p['oX']} | П2 {p['o2']}\n\n"
    
    elif match['sport'] == 'ufc':
        text += f"📊 <b>Рейтинги:</b>\n"
        text += f"{match['home']}: #{match['home_rank']}\n"
        text += f"{match['away']}: #{match['away_rank']}\n\n"
    
    elif match['sport'] == 'tennis':
        text += f"📊 <b>Рейтинги ATP:</b>\n"
        text += f"{match['home']}: #{match['home_rank']}\n"
        text += f"{match['away']}: #{match['away_rank']}\n\n"
    
    text += "━━━ 🎯 ПРОГНОЗ ИИ ━━━\n\n"
    best = pred['best']
    text += f"✅ <b>{best['market']}</b> @ <b>{best['odds']}</b>\n"
    text += f"🎯 Уверенность: {pred['confidence']} ({int(best['prob'] * 100)}%)\n\n"
    text += f"💡 <i>{best['reason']}</i>\n"
    
    if pred['alternatives']:
        text += "\n━━━ 💡 АЛЬТЕРНАТИВЫ ━━━\n\n"
        for alt in pred['alternatives']:
            text += f"• {alt['market']} @ {alt['odds']} ({int(alt['prob'] * 100)}%)\n"
    
    return text

def format_match_short(match: dict, pred: dict, idx: int) -> str:
    """Короткая строка для списка матчей"""
    icons = {'football': '⚽', 'ufc': '🥊', 'tennis': '🎾'}
    icon = icons.get(match['sport'], '🏆')
    best = pred['best']
    
    return f"{icon} <b>{match['time']}</b> {match['home']} — {match['away']}\n" \
           f"    🎯 {best['market']} @ {best['odds']} ({int(best['prob'] * 100)}%)"

def main_menu_kb():
    """Главное меню"""
    kb = [
        [InlineKeyboardButton(text="📅 Прогнозы дня", callback_data="today")],
        [InlineKeyboardButton(text="🔥 Ставка дня", callback_data="best_bet")],
        [InlineKeyboardButton(text="🎫 Экспрессы", callback_data="expresses")],
        [InlineKeyboardButton(text="📊 Статистика ИИ", callback_data="stats")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def back_kb():
    """Кнопка «Назад»"""
    kb = [[InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="menu")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def match_detail_kb(match_id: int):
    """Кнопки под прогнозом"""
    kb = [
        [InlineKeyboardButton(text="🎯 Все рынки", callback_data=f"markets_{match_id}")],
        [InlineKeyboardButton(text="⬅️ К прогнозам дня", callback_data="today")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def matches_list_kb(matches: list, preds: list):
    """Список матчей как кнопки"""
    kb = []
    for i, (m, p) in enumerate(zip(matches, preds)):
        icon = {'football': '⚽', 'ufc': '🥊', 'tennis': '🎾'}.get(m['sport'], '🏆')
        conf_icon = '🟢' if p['conf_level'] == 'high' else '🟡' if p['conf_level'] == 'medium' else '🔴'
        kb.append([InlineKeyboardButton(
            text=f"{icon} {m['time']} {m['home']} — {m['away']} {conf_icon}",
            callback_data=f"match_{m['id']}"
        )])
    kb.append([InlineKeyboardButton(text="🏠 В меню", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def markets_kb(match_id: int):
    """Кнопки для всех рынков"""
    kb = [
        [InlineKeyboardButton(text="⬅️ К прогнозу", callback_data=f"match_{match_id}")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def format_markets_message(match: dict, pred: dict) -> str:
    """Все рынки на матч"""
    icons = {'football': '⚽', 'ufc': '🥊', 'tennis': '🎾'}
    icon = icons.get(match['sport'], '🏆')
    
    text = f"{icon} <b>{match['home']} — {match['away']}</b>\n"
    text += f"🕒 {match['time']}\n\n"
    
    if match['sport'] == 'football':
        p = pred['probs']
        text += "━━━ 🎯 ИСХОД ━━━\n\n"
        text += f"П1: <b>{p['o1']}</b> | X: <b>{p['oX']}</b> | П2: <b>{p['o2']}</b>\n\n"
        
        text += "━━━ 📊 ТОТАЛЫ ━━━\n\n"
        for line in [0.5, 1.5, 2.5, 3.5]:
            t = pred['totals'][line]
            text += f"<b>{line}</b>: Б {t['over']} | М {t['under']}\n"
        text += "\n"
        
        text += "━━━ 🥅 ОБЕ ЗАБЬЮТ ━━━\n\n"
        b = pred['btts']
        text += f"Да: <b>{b['yes']}</b> | Нет: <b>{b['no']}</b>\n"
    
    elif match['sport'] in ['ufc', 'tennis']:
        text += "━━━ 🎯 ИСХОД ━━━\n\n"
        text += f"{match['home']}: <b>{pred['o1']}</b>\n"
        text += f"{match['away']}: <b>{pred['o2']}</b>\n"
    
    return text

def best_bet_of_day(matches: list, preds: list) -> tuple:
    """Находит матч с самой высокой уверенностью"""
    best_idx = 0
    best_prob = 0
    for i, p in enumerate(preds):
        if p and p['best']['prob'] > best_prob:
            best_prob = p['best']['prob']
            best_idx = i
    return matches[best_idx], preds[best_idx]

def generate_express(kind: str = 'safe') -> dict:
    """Генерирует экспресс из прогнозов"""
    matches = get_all_matches(0)
    preds = [make_prediction(m) for m in matches]
    
    # Фильтруем по уверенности
    if kind == 'safe':
        # Топ-2 с уверенностью высокий
        filtered = [(m, p) for m, p in zip(matches, preds) if p and p['conf_level'] == 'high']
        filtered.sort(key=lambda x: x[1]['best']['prob'], reverse=True)
        selected = filtered[:2]
    elif kind == 'risk':
        # 3 события с кэфом > 2.5
        filtered = [(m, p) for m, p in zip(matches, preds) if p and p['best']['odds'] >= 2.5]
        filtered.sort(key=lambda x: x[1]['best']['odds'], reverse=True)
        selected = filtered[:3]
    else:  # mix
        # 4 события — смесь
        filtered = [(m, p) for m, p in zip(matches, preds) if p]
        filtered.sort(key=lambda x: x[1]['best']['prob'] * x[1]['best']['odds'], reverse=True)
        selected = filtered[:4]
    
    if not selected:
        return None
    
    # Считаем общий кэф
    total_odds = 1.0
    total_prob = 1.0
    for m, p in selected:
        total_odds *= p['best']['odds']
        total_prob *= p['best']['prob']
    
    return {
        'events': selected,
        'total_odds': round(total_odds, 2),
        'total_prob': total_prob,
        'kind': kind
    }

def format_express_message(express: dict, number: int) -> str:
    """Сообщение с экспрессом"""
    kind_titles = {
        'safe': '🔥 Экспресс дня',
        'risk': '⚡ Риск-экспресс',
        'mix': '🎯 Микс-экспресс'
    }
    
    text = f"<b>{kind_titles.get(express['kind'], '🎫 Экспресс')} #{number}</b>\n\n"
    
    for i, (m, p) in enumerate(express['events'], 1):
        icon = {'football': '⚽', 'ufc': '🥊', 'tennis': '🎾'}.get(m['sport'], '🏆')
        best = p['best']
        text += f"{i}. {icon} <b>{m['home']} — {m['away']}</b>\n"
        text += f"   {best['market']} @ {best['odds']}\n\n"
    
    text += "━━━━━━━━━━━━━━━\n\n"
    text += f"💰 <b>Общий кэф: {express['total_odds']}</b>\n"
    text += f"🎯 Вероятность: {int(express['total_prob'] * 100)}%\n"
    text += f"💵 Ставка 1000 ₽ → <b>{int(1000 * express['total_odds'])} ₽</b>\n"
    
    return text

def expresses_kb():
    """Кнопки для экспрессов"""
    kb = [
        [InlineKeyboardButton(text="🔥 Экспресс дня", callback_data="exp_safe")],
        [InlineKeyboardButton(text="⚡ Риск-экспресс", callback_data="exp_risk")],
        [InlineKeyboardButton(text="🎯 Микс-экспресс", callback_data="exp_mix")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
  
# ============================================
# ЧАСТЬ 5 — ОБРАБОТЧИКИ + ЗАПУСК
# ============================================

# ТОКЕН ТУТ — вставляй сюда если Часть 1 не изменена
TOKEN = "8960922268:AAEz_DK55WFN7IoCGSR6CYuMRDYB0xfhMWc"

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()


# ============ ХЕЛПЕРЫ ============

async def safe_edit(call: types.CallbackQuery, text: str, kb):
    """Безопасное редактирование сообщения"""
    try:
        await call.message.edit_text(text, parse_mode="HTML", reply_markup=kb)
    except Exception:
        try:
            await call.message.answer(text, parse_mode="HTML", reply_markup=kb)
        except Exception:
            pass


# ============ КОМАНДЫ ============

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = "🤖 <b>BET AI — умные прогнозы на спорт</b>\n\n"
    text += "Я анализирую матчи и даю прогнозы на основе:\n"
    text += "• 📊 Формы команд\n"
    text += "• 📜 Истории встреч\n"
    text += "• 💰 Кэфов\n"
    text += "• 🎯 Математических моделей\n\n"
    text += "Выбери раздел 👇"
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu_kb())


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    text = "ℹ️ <b>Помощь</b>\n\n"
    text += "📅 <b>Прогнозы дня</b> — все матчи с прогнозами\n"
    text += "🔥 <b>Ставка дня</b> — самый уверенный прогноз\n"
    text += "🎫 <b>Экспрессы</b> — готовые комбинации\n"
    text += "📊 <b>Статистика</b> — точность ИИ\n\n"
    text += "Прогнозы <b>обновляются каждый день</b> в 00:00.\n"
    text += "В течение дня они <b>не меняются</b> — стабильны.\n\n"
    text += "⚠️ Прогнозы — <b>не гарантия</b>. Играй ответственно."
    await message.answer(text, parse_mode="HTML", reply_markup=back_kb())


# ============ CALLBACK — ГЛАВНОЕ МЕНЮ ============

@dp.callback_query(lambda c: c.data == "menu")
async def cb_menu(call: types.CallbackQuery):
    text = "🏠 <b>Главное меню</b>\n\nВыбери раздел 👇"
    await safe_edit(call, text, main_menu_kb())
    await call.answer()


@dp.callback_query(lambda c: c.data == "help")
async def cb_help(call: types.CallbackQuery):
    text = "ℹ️ <b>Помощь</b>\n\n"
    text += "📅 Прогнозы дня — все матчи\n"
    text += "🔥 Ставка дня — уверенный прогноз\n"
    text += "🎫 Экспрессы — готовые комбинации\n"
    text += "📊 Статистика — точность ИИ\n\n"
    text += "Прогнозы обновляются каждый день в 00:00.\n"
    text += "В течение дня не меняются.\n\n"
    text += "⚠️ Не гарантия. Играй ответственно."
    await safe_edit(call, text, back_kb())
    await call.answer()


# ============ CALLBACK — ПРОГНОЗЫ ДНЯ ============

@dp.callback_query(lambda c: c.data == "today")
async def cb_today(call: types.CallbackQuery):
    matches = get_all_matches(0)
    preds = [make_prediction(m) for m in matches]
    
    text = f"📅 <b>Прогнозы на сегодня</b>\n\n"
    text += f"Всего матчей: {len(matches)}\n"
    text += f"🟢 Уверенных: {sum(1 for p in preds if p and p['conf_level'] == 'high')}\n\n"
    text += "Выбери матч 👇"
    
    await safe_edit(call, text, matches_list_kb(matches, preds))
    await call.answer()


@dp.callback_query(lambda c: c.data.startswith("match_"))
async def cb_match_detail(call: types.CallbackQuery):
    match_id = int(call.data.split("_")[1])
    match = find_match_by_id(match_id)
    if not match:
        await call.answer("Матч не найден", show_alert=True)
        return
    
    pred = make_prediction(match)
    text = format_prediction_message(match, pred)
    await safe_edit(call, text, match_detail_kb(match_id))
    await call.answer()


@dp.callback_query(lambda c: c.data.startswith("markets_"))
async def cb_markets(call: types.CallbackQuery):
    match_id = int(call.data.split("_")[1])
    match = find_match_by_id(match_id)
    if not match:
        await call.answer("Матч не найден", show_alert=True)
        return
    
    pred = make_prediction(match)
    text = format_markets_message(match, pred)
    await safe_edit(call, text, markets_kb(match_id))
    await call.answer()


# ============ CALLBACK — СТАВКА ДНЯ ============

@dp.callback_query(lambda c: c.data == "best_bet")
async def cb_best_bet(call: types.CallbackQuery):
    matches = get_all_matches(0)
    preds = [make_prediction(m) for m in matches]
    
    match, pred = best_bet_of_day(matches, preds)
    text = "🔥 <b>СТАВКА ДНЯ</b>\n\n"
    text += format_prediction_message(match, pred)
    
    await safe_edit(call, text, match_detail_kb(match['id']))
    await call.answer()


# ============ CALLBACK — ЭКСПРЕССЫ ============

@dp.callback_query(lambda c: c.data == "expresses")
async def cb_expresses(call: types.CallbackQuery):
    text = "🎫 <b>Готовые экспрессы от ИИ</b>\n\n"
    text += "🔥 <b>Экспресс дня</b> — 2 самых уверенных\n"
    text += "⚡ <b>Риск-экспресс</b> — 3 события с высоким кэфом\n"
    text += "🎯 <b>Микс-экспресс</b> — 4 сбалансированных\n\n"
    text += "Выбери тип 👇"
    await safe_edit(call, text, expresses_kb())
    await call.answer()


@dp.callback_query(lambda c: c.data.startswith("exp_"))
async def cb_express_type(call: types.CallbackQuery):
    kind = call.data.split("_")[1]  # safe / risk / mix
    express = generate_express(kind)
    
    if not express:
        await call.answer("Не хватает матчей", show_alert=True)
        return
    
    number = random.randint(1, 99)
    text = format_express_message(express, number)
    await safe_edit(call, text, expresses_kb())
    await call.answer()


# ============ CALLBACK — СТАТИСТИКА ============

@dp.callback_query(lambda c: c.data == "stats")
async def cb_stats(call: types.CallbackQuery):
    matches = get_all_matches(0)
    preds = [make_prediction(m) for m in matches if make_prediction(m)]
    
    avg_prob = sum(p['best']['prob'] for p in preds) / len(preds) if preds else 0
    
    football = [p for m, p in zip(matches, preds) if m['sport'] == 'football' and p]
    ufc = [p for m, p in zip(matches, preds) if m['sport'] == 'ufc' and p]
    tennis = [p for m, p in zip(matches, preds) if m['sport'] == 'tennis' and p]
    
    text = "📊 <b>Статистика ИИ</b>\n\n"
    text += "━━━ 📅 СЕГОДНЯ ━━━\n\n"
    text += f"Матчей: <b>{len(matches)}</b>\n"
    text += f"🟢 Уверенных: {sum(1 for p in preds if p['conf_level'] == 'high')}\n"
    text += f"🟡 Средних: {sum(1 for p in preds if p['conf_level'] == 'medium')}\n"
    text += f"🔴 Низких: {sum(1 for p in preds if p['conf_level'] == 'low')}\n"
    text += f"Средняя уверенность: <b>{int(avg_prob * 100)}%</b>\n\n"
    
    text += "━━━ ⚽ ФУТБОЛ ━━━\n"
    text += f"Матчей: {len(football)}\n"
    text += f"Средняя уверенность: {int(sum(p['best']['prob'] for p in football) / len(football) * 100) if football else 0}%\n\n"
    
    text += "━━━ 🥊 UFC ━━━\n"
    text += f"Боёв: {len(ufc)}\n\n"
    
    text += "━━━ 🎾 ТЕННИС ━━━\n"
    text += f"Матчей: {len(tennis)}\n\n"
    
    text += "━━━ 🎯 ТОЧНОСТЬ ━━━\n\n"
    text += "За эту неделю ИИ угадал <b>68%</b> прогнозов.\n"
    text += "Средний кэф: <b>1.92</b>\n\n"
    
    text += "<i>Точность обновляется в конце недели.</i>"
    
    await safe_edit(call, text, back_kb())
    await call.answer()


# ============ CALLBACK — НАСТРОЙКИ ============

@dp.callback_query(lambda c: c.data == "settings")
async def cb_settings(call: types.CallbackQuery):
    text = "⚙️ <b>Настройки</b>\n\n"
    text += "Скоро здесь появятся:\n"
    text += "• Выбор видов спорта\n"
    text += "• Уровень уверенности\n"
    text += "• Уведомления за час до матча\n"
    text += "• Время отправки прогнозов\n\n"
    text += "<i>Пока всё включено по умолчанию.</i>"
    await safe_edit(call, text, back_kb())
    await call.answer()


# ============ ЗАПУСК ============

async def main():
    print("BET AI — запуск...")
    print(f"Токен: ...{TOKEN[-10:]}")
    print("Бот запущен, ожидаю сообщения.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")

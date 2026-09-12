import os
import hmac
import hashlib
import json
from urllib.parse import parse_qsl
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import db
from cases import CASES, open_case, get_case_roll, RARITY_COLORS, RARITY_NAMES

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db.init_db()

# ==========================================
# TELEGRAM AUTH
# ==========================================
def validate_init_data(init_data: str) -> dict:
    """Проверка подписи Telegram WebApp initData."""
    try:
        parsed = dict(parse_qsl(init_data))
        if "hash" not in parsed:
            return None
        received_hash = parsed.pop("hash")
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
        secret_key = hmac.new(
            b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256
        ).digest()
        calculated_hash = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()
        if calculated_hash != received_hash:
            return None
        if "user" in parsed:
            parsed["user"] = json.loads(parsed["user"])
        return parsed
    except Exception:
        return None


def get_user_from_request(request: Request):
    init_data = request.headers.get("X-Init-Data", "")
    if not init_data:
        raise HTTPException(401, "no init data")
    data = validate_init_data(init_data)
    if not data or "user" not in data:
        raise HTTPException(401, "invalid auth")
    u = data["user"]
    return db.get_or_create_user(u["id"], u.get("username", ""), u.get("first_name", ""))


# ==========================================
# API
# ==========================================
class OpenCaseRequest(BaseModel):
    case_id: str


@app.get("/api/me")
async def api_me(request: Request):
    user = get_user_from_request(request)
    return {
        "id": user["user_id"],
        "username": user["username"],
        "first_name": user["first_name"],
        "stars": user["stars"],
        "crystals": user["crystals"],
        "total_opened": user["total_opened"],
        "total_spent": user["total_spent"],
        "total_won": user["total_won"],
    }


@app.get("/api/cases")
async def api_cases():
    result = []
    for cid, c in CASES.items():
        result.append({
            "id": cid,
            "name": c["name"],
            "emoji": c["emoji"],
            "price": c["price"],
            "color": c["color"],
            "item_count": len(c["items"]),
        })
    return result


@app.get("/api/case/{case_id}")
async def api_case(case_id: str):
    c = CASES.get(case_id)
    if not c:
        raise HTTPException(404, "case not found")
    return {
        "id": case_id,
        "name": c["name"],
        "emoji": c["emoji"],
        "price": c["price"],
        "color": c["color"],
        "items": c["items"],
    }


@app.post("/api/open")
async def api_open(req: OpenCaseRequest, request: Request):
    user = get_user_from_request(request)
    c = CASES.get(req.case_id)
    if not c:
        raise HTTPException(404, "case not found")

    price = c["price"]
    if price > 0 and user["stars"] < price:
        raise HTTPException(400, "not enough stars")

    item = open_case(req.case_id)
    if not item:
        raise HTTPException(500, "roll error")

    # Списание + запись
    if price > 0:
        db.update_balance(user["user_id"], stars_delta=-price)
    db.update_stats(user["user_id"], opened=1, spent=price, won=0)
    db.add_to_inventory(
        user["user_id"], item["name"], item["emoji"],
        item["value"], item["rarity"], req.case_id
    )
    db.add_history(
        user["user_id"], req.case_id, item["name"],
        item["emoji"], item["value"], price
    )

    # Рулетка (для анимации)
    roll = get_case_roll(req.case_id, win_index=35, length=50)

    fresh = db.get_user(user["user_id"])
    return {
        "item": item,
        "roll": roll,
        "newBalance": fresh["stars"],
        "rarity_color": RARITY_COLORS.get(item["rarity"], "#888"),
        "rarity_name": RARITY_NAMES.get(item["rarity"], item["rarity"]),
    }


@app.get("/api/inventory")
async def api_inventory(request: Request):
    user = get_user_from_request(request)
    inv = db.get_inventory(user["user_id"])
    return inv


class SellRequest(BaseModel):
    item_id: int


@app.post("/api/sell")
async def api_sell(req: SellRequest, request: Request):
    user = get_user_from_request(request)
    inv = db.get_inventory(user["user_id"])
    item = next((i for i in inv if i["id"] == req.item_id), None)
    if not item:
        raise HTTPException(404, "item not found")
    price = int(item["item_value"] * 0.7)
    db.remove_from_inventory(req.item_id, user["user_id"])
    db.update_balance(user["user_id"], stars_delta=price)
    fresh = db.get_user(user["user_id"])
    return {"sold_for": price, "newBalance": fresh["stars"]}


@app.get("/api/history")
async def api_history(request: Request):
    user = get_user_from_request(request)
    return db.get_history(user["user_id"], 50)


@app.get("/api/top")
async def api_top():
    conn = db.get_conn()
    c = conn.cursor()
    c.execute("SELECT first_name, username, total_opened, total_won FROM users ORDER BY total_won DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ==========================================
# SERVING WEBAPP
# ==========================================
WEBAPP_DIR = os.path.join(os.path.dirname(__file__), "webapp")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    path = os.path.join(WEBAPP_DIR, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/case", response_class=HTMLResponse)
async def serve_case():
    path = os.path.join(WEBAPP_DIR, "case.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/profile", response_class=HTMLResponse)
async def serve_profile():
    path = os.path.join(WEBAPP_DIR, "profile.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/style.css")
async def serve_css():
    path = os.path.join(WEBAPP_DIR, "style.css")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read(), media_type="text/css")


@app.get("/app.js")
async def serve_js():
    path = os.path.join(WEBAPP_DIR, "app.js")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read(), media_type="application/javascript")


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

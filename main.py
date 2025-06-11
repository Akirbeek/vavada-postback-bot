from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

# Telegram bot token и chat ID
TELEGRAM_BOT_TOKEN = "7709029811:AAE4E4IWEUDIj44R0ejCuPR6DMgaMW5WHvs"
CHAT_ID = "-1002444563051"

async def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, data=payload)

@app.get("/")
async def root():
    return {"message": "бот работает!"}

@app.post("/postback")
async def postback(request: Request):
    data = dict(request.query_params)
    click_id = data.get("click_id", "N/A")
    status = data.get("status", "unknown")
    payout = data.get("payout", "0")
    currency = data.get("currency", "")

    # Составляем текст в зависимости от события
    if status == "lead":
        text = f"📥 <b>Новая регистрация</b>
Click ID: <code>{click_id}</code>"
    elif status == "sale":
        text = f"💰 <b>Первый депозит</b>
Click ID: <code>{click_id}</code>"
    elif status == "reward":
        text = f"🏆 <b>Вознаграждение</b>
Click ID: <code>{click_id}</code>
Сумма: <b>{payout} {currency}</b>"
    else:
        text = f"ℹ️ <b>Неизвестное событие</b>
Click ID: <code>{click_id}</code>
Status: <code>{status}</code>"

    await send_telegram_message(text)
    return {"status": "ok"}

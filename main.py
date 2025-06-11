from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

BOT_TOKEN = "7709029811:AAE4E4IWEUDIj44R0ejCuPR6DMgaMW5WHvs"
CHANNEL_ID = "-1002444563051"

@app.get("/postback")
async def postback(request: Request):
    params = dict(request.query_params)
    click_id = params.get("click_id", "N/A")
    status = params.get("status", "N/A")
    payout = params.get("payout", "")
    currency = params.get("currency", "")

    if status == "lead":
        text = f"🔔<b>Новая регистрация</b>\nClick ID: {click_id}"
    elif status == "sale":
        text = f"💰<b>Прошел квалификацию</b>\nClick ID: {click_id}"
    elif status and payout:
        text = f"🏆<b>Вознаграждение</b>\nClick ID: {click_id}\nPayout: {payout} {currency}"
    else:
        text = f"📩<b>Неизвестный статус</b>\nClick ID: {click_id}\nStatus: {status}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    async with httpx.AsyncClient() as client:
        await client.post(url, data=payload)

    return {"message": "Postback received"}
from fastapi import FastAPI, Request
import httpx

app = FastAPI()

BOT_TOKEN = "ТВОЙ_BOT_TOKEN"
CHANNEL_ID = "-1002446543051"

async def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, data=data)

@app.get("/")
def root():
    return {"message": "бот работает!"}

@app.post("/postback")
@app.get("/postback")
async def handle_postback(request: Request):
    data = dict(request.query_params)

    click_id = data.get("subid", "не передан")
    status = data.get("status", "").lower()
    payout = data.get("payout")
    currency = data.get("currency")

    if status == "lead":
        tag = "📝 Регистрация"
    elif status == "sale":
        tag = "✅ Прохождение квалификации"
    elif payout:
        tag = f"💰 Выплата: {payout} {currency or ''}".strip()
    else:
        tag = f"❓ Статус: {status}"

    msg = (
        f"🔔 Новое событие от Vavada
"
        f"📌 <b>Click ID:</b> <code>{click_id}</code>
"
        f"📊 <b>Событие:</b> {tag}"
    )
    await send_to_telegram(msg)

    return {"status": "ok"}

import uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "бот работает!"}

@app.post("/postback")
async def postback(request: Request):
    data = await request.json()
    print("Получен postback:", data)
    return {"status": "ok"}

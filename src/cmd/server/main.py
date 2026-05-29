from fastapi import FastAPI
from src.modules.chat.adapter.http.rest import router as channel_account_router
from src.pkg.broker import broker

app = FastAPI(
    title="Facebook Webhook API",
    version="0.1.0"
)

@app.on_event("startup")
async def startup_event():
    await broker.startup()

@app.on_event("shutdown")
async def shutdown_event():
    await broker.shutdown()

app.include_router(channel_account_router)
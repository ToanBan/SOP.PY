from fastapi import FastAPI
from src.modules.chat.adapter.http.rest import router as channel_account_router
from src.pkg.broker import broker
from src.pkg.middleware.security_headers_middleware import SecurityHeadersMiddleware
from src.pkg.logger.config import configure_logging

configure_logging()

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

app.add_middleware(SecurityHeadersMiddleware)
app.include_router(channel_account_router)
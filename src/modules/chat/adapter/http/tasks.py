from src.pkg.broker import broker
from src.pkg.database.database import async_session_maker
from src.modules.chat.adapter.dependencies.channel_account import get_process_message_use_case

@broker.task
async def process_facebook_webhook(data: dict) -> None:
    async with async_session_maker() as session:
        try:
            use_case = get_process_message_use_case(session)
            await use_case.execute(data)
            await session.commit()
        except Exception as e:
            await session.rollback()
            print("Worker error:", e)
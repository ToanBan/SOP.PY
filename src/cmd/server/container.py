from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.chat.adapter.postgresql.repo.customer_repo import CustomerRepository
from src.modules.chat.adapter.postgresql.repo.conversation_repo import ConversationRepository
from src.modules.chat.adapter.postgresql.repo.message_repo import MessageRepository
from src.modules.chat.adapter.postgresql.repo.message_file_repo import MessageFileRepository
from src.modules.chat.adapter.postgresql.repo.channel_account_repo import ChannelAccountRepository
from src.modules.chat.adapter.http.facebook_client import FacebookClient

def provide_channel_account_repo(session: AsyncSession) -> ChannelAccountRepository:
    return ChannelAccountRepository(session)

def provide_customer_repo(session: AsyncSession) -> CustomerRepository:
    return CustomerRepository(session)

def provide_conversation_repo(session: AsyncSession) -> ConversationRepository:
    return ConversationRepository(session)

def provide_message_repo(session: AsyncSession) -> MessageRepository:
    return MessageRepository(session)

def provide_message_file_repo(session: AsyncSession) -> MessageFileRepository:
    return MessageFileRepository(session)

def provide_facebook_client() -> FacebookClient:
    return FacebookClient()
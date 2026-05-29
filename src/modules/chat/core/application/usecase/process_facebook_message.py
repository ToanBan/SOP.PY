import uuid
from src.modules.chat.core.domain.entity.customer import Customer
from src.modules.chat.core.application.port.output.i_conversation import ConversationRepositoryInterface
from src.modules.chat.core.application.port.output.i_message import MessageRepositoryInterface
from src.modules.chat.core.application.port.output.i_customer import CustomerRepositoryInterface
from src.modules.chat.core.application.port.output.i_message_file import MessageFileRepositoryInterface
from src.modules.chat.core.application.port.input.i_find_channel_byid import FindChannelByIdUseCaseInterface
from src.modules.chat.core.domain.entity.conversation import Conversation
from src.modules.chat.core.domain.entity.message import Message
from src.modules.chat.core.domain.entity.message_file import MessageFile
from src.modules.chat.adapter.redis.channel_account_cache import ChannelAccountCache
from src.modules.chat.adapter.redis.customer_cache import CustomerCache
from src.modules.chat.adapter.minio.file_storage import MinioFileStorage

class ProcessFacebookMessageUseCase:

    def __init__(
        self,
        conversation_repository: ConversationRepositoryInterface,
        message_repository: MessageRepositoryInterface,
        customer_repository: CustomerRepositoryInterface,
        message_file_repository: MessageFileRepositoryInterface,
        find_channel_by_id_use_case: FindChannelByIdUseCaseInterface,
    ):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
        self.customer_repository = customer_repository
        self.message_file_repository = message_file_repository
        self.find_channel_by_id_use_case = find_channel_by_id_use_case
        self.channel_account_cache = ChannelAccountCache()
        self.customer_cache = CustomerCache()
        self.file_storage = MinioFileStorage() 

    async def execute(self, payload: dict) -> None:
        for entry in payload.get("entry", []):
            for messaging in entry.get("messaging", []):

                if "message" not in messaging:
                    continue

                sender_id = messaging["sender"]["id"]
                page_id = messaging["recipient"]["id"]
                message_data = messaging.get("message", {})
                facebook_message_id = message_data.get("mid")
                text = message_data.get("text", "")
                attachments = message_data.get("attachments", [])

                channel_account = await self.channel_account_cache.get(page_id)
                if channel_account is None:
                    channel_account = await self.find_channel_by_id_use_case.execute(page_id)
                    if channel_account is None:
                        print(f"Channel account not found: {page_id}")
                        continue
                    await self.channel_account_cache.set(channel_account)

                customer = await self.customer_cache.get(sender_id)
                if customer is None:
                    customer = await self.customer_repository.find_by_psid(sender_id)
                    if customer is None:
                        customer = Customer(
                            id=str(uuid.uuid4()),
                            sender_id=sender_id,
                            page_id=page_id,
                            name="",
                        )
                        await self.customer_repository.save(customer)
                    await self.customer_cache.set(customer)

                conversation = await self.conversation_repository.find_by_customer_id(customer.id)
                if conversation is None:
                    conversation = Conversation(
                        page_id=page_id,
                        customer_id=customer.id,
                        status="open",
                    )
                    await self.conversation_repository.save(conversation)

                message_type = "text"
                if attachments:
                    message_type = attachments[0].get("type", "file")

                message = Message(
                    id=str(uuid.uuid4()),
                    conversation_id=conversation.id,
                    sender_id=sender_id,
                    message_id=facebook_message_id,
                    message_type=message_type,
                    text=text or "",
                    timestamp=messaging["timestamp"],
                )
                await self.message_repository.save(message)

                if attachments:
                    for attachment in attachments:
                        payload_data = attachment.get("payload", {})
                        url = payload_data.get("url")
                        if url is None:
                            continue

                        file_type = attachment.get("type", "file")
                        file_name = f"{message.id}_{uuid.uuid4()}.{file_type}"
                        
                        minio_url = await self.file_storage.upload_from_url(
                            file_url=url,
                            file_name=file_name,
                            content_type=f"{file_type}/octet-stream"
                        )

                        message_file = MessageFile(
                            id=str(uuid.uuid4()),
                            message_id=message.id,
                            file_url=minio_url, 
                            file_type=file_type,
                        )
                        await self.message_file_repository.save(message_file)
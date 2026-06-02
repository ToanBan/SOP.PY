
import uuid
from src.modules.chat.adapter.taskiq.tasks import process_facebook_webhook
from src.modules.chat.core.application.port.input.i_enqueue_facebook_webhook import (
    EnqueueFacebookWebhookUseCaseInterface
)
class EnqueueFacebookWebhookUseCase(
    EnqueueFacebookWebhookUseCaseInterface
):

    async def execute(self, payload: dict) -> str:
        request_id = str(uuid.uuid4())
        task = await process_facebook_webhook.kiq({
            "request_id": request_id,
            "payload": payload
        })
        return task.task_id
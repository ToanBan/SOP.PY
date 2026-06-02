from fastapi import APIRouter, Depends, Query, HTTPException, Request
from src.modules.chat.adapter.http.dtos.channel_account_schema import AddChannelAccountRequest
from src.modules.chat.core.application.port.input.i_save_token_usecase import SaveFacebookTokeUseCaseInterface
from src.modules.chat.core.application.dtos.save_facebook_token import SaveFacebookTokenDTO
from src.modules.chat.core.application.port.input.i_find_channel_byid import FindChannelByIdUseCaseInterface
from src.pkg.broker import broker
from src.modules.chat.adapter.dependencies.channel_account import get_save_facebook_token_use_case, get_find_channel_account_use_case, get_enqueue_facebook_webhook_use_case
from src.modules.chat.core.application.usecase.enqueue_facebook_webhook import EnqueueFacebookWebhookUseCase
from src.modules.chat.core.application.port.input.i_enqueue_facebook_webhook import EnqueueFacebookWebhookUseCaseInterface
router = APIRouter(prefix="/channel-accounts",tags=["Channel Accounts"])

@router.get("/webhooks/facebook")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == "123456":
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")

@router.post("/webhooks/facebook")
async def receive_webhook(request: Request, use_case: EnqueueFacebookWebhookUseCaseInterface = Depends(
        get_enqueue_facebook_webhook_use_case
    ),):
    data = await request.json()
    print("Webhook received:", data)
    await use_case.execute(data)
    return {"status": "ok"}


@router.get("/webhooks/task/{task_id}")
async def check_task(task_id: str):
    result = await broker.result_backend.get_result(task_id)
    
    if result is None:
        return {"status": "pending"} 
    if result.is_err:
        return {"status": "failed", "error": str(result.error)}

    return {"status": "success"}


@router.post("/")
async def add_channel_account(
    data: AddChannelAccountRequest,
    use_case: SaveFacebookTokeUseCaseInterface = Depends(get_save_facebook_token_use_case)
):
   
    dto = SaveFacebookTokenDTO(page_access_token=data.page_access_token)
    await use_case.execute(dto)
    return {"status": "created"}

@router.get("/{page_id}")
async def get_channel_account(
    page_id: str,
    use_case: FindChannelByIdUseCaseInterface = Depends(get_find_channel_account_use_case)
):
    channel_account = await use_case.execute(page_id)
    if channel_account is None:
        return {"error": "Channel account not found"}
    return {
        "page_id": channel_account.page_id,
        "page_name": channel_account.page_name,
        "page_access_token": channel_account.page_access_token,
        "is_active": channel_account.is_active,
    }
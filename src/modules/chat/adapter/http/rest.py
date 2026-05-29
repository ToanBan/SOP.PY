from fastapi import APIRouter, Depends, Query, HTTPException, Request
from src.modules.chat.adapter.http.dtos.channel_account_schema import AddChannelAccountRequest
from src.modules.chat.core.application.port.input.i_save_token_usecase import SaveFacebookTokeUseCaseInterface
from src.modules.chat.core.application.usecase.find_channel_account import FindChannelAccountByChannelAccountUseCase
from src.modules.chat.adapter.http.tasks import process_facebook_webhook
from src.modules.chat.core.application.dtos.save_facebook_token import SaveFacebookTokenDTO
from src.pkg.broker import broker
from src.modules.chat.adapter.dependencies.channel_account import get_save_facebook_token_use_case, get_find_channel_account_use_case
router = APIRouter(prefix="/channel-accounts", tags=["Channel Accounts"])

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
async def receive_webhook(request: Request):
    data = await request.json()
    print("Webhook received:", data)
    task = await process_facebook_webhook.kiq(data)
    return {"status": "ok", "task_id": task.task_id}


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
    use_case: FindChannelAccountByChannelAccountUseCase = Depends(get_find_channel_account_use_case)
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
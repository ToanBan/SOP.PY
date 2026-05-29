import httpx
from src.modules.chat.core.application.port.output.i_facebook_client import IFacebookClient


class FacebookClient(IFacebookClient):
    async def get_page_info(self, access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://graph.facebook.com/v21.0/me",
                params={
                    "access_token": access_token
                }
            )
            return response.json()
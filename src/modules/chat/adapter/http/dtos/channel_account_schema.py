from pydantic import BaseModel

class AddChannelAccountRequest(BaseModel):
    page_access_token: str
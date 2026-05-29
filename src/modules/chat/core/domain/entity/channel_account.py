from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ChannelAccount:
    page_id: str
    page_access_token: str
    page_name: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
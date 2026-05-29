from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class MessageFile:
    id: str
    message_id: str
    file_url: str
    file_type: str
    created_at: datetime = field(default_factory=datetime.utcnow)
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Message:
    id: str
    conversation_id: str
    sender_id: str
    message_id: str
    message_type: str
    text: str
    timestamp: int
    created_at: datetime = field(default_factory=datetime.utcnow)  
from dataclasses import dataclass, field
from datetime import datetime

@dataclass  
class Customer:
    id: str
    page_id: str
    sender_id: str
    name: str
    created_at: datetime = field(default_factory=datetime.utcnow) 
    updated_at: datetime = field(default_factory=datetime.utcnow) 
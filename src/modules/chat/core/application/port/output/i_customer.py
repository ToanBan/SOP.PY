from abc import ABC, abstractmethod
from src.modules.chat.core.domain.entity.customer import Customer

class CustomerRepositoryInterface(ABC):
    
    @abstractmethod 
    async def save(self, customer: Customer) -> None: ...

    @abstractmethod
    async def find_by_id(self, customer_id: str) -> Customer | None: ...

    @abstractmethod
    async def find_by_psid(self, sender_id: str) -> Customer | None: ...  
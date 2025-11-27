from typing import Any, Dict, List, Optional

from ..client import OctadeskClient
from ..models.contact import (
    ContactCreate, ContactResponse, ContactUpdate, ContactOverride
)


class ContactsService:
    def __init__(self, client: OctadeskClient):
        self.client = client

    def get(self, contact_id: str) -> ContactResponse:
        path = f"/contacts/{contact_id}"
        data = self.client.get(path)
        return ContactResponse.model_validate(data)

    def list(self, page: int = 1, limit: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[ContactResponse]:
        params = {"page": page, "limit": limit}
        
        if filters:
            params.update(self.client.parse_filters(filters))
        
        data = self.client.get("/contacts", params=params)
        items = data if isinstance(data, list) else data.get("items", [])
        return [ContactResponse.model_validate(i) for i in items]

    def create(self, contact: ContactCreate) -> ContactResponse:
        payload = contact.model_dump(exclude_none=True)
        data = self.client.post("/contacts", json=payload)
        return ContactResponse.model_validate(data)

    def update(self, contact: ContactUpdate) -> ContactResponse:
        payload = contact.model_dump(exclude_none=True)
        path = f"/contacts/{contact.id}"
        data = self.client.patch(path, json=payload)
        return ContactResponse.model_validate(data)
    
    def override(self, contact: ContactOverride) -> ContactResponse:
        payload = contact.model_dump(exclude_none=True)
        path = f"/contacts/{contact.id}"
        data = self.client.put(path, json=payload)
        return ContactResponse.model_validate(data)

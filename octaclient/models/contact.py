from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    emails: Optional[List[str]] = None
    phoneContacts: Optional[List[Dict[str, Any]]] = None
    organization: Optional[Dict[str, Any]] = None
    responsible: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    customFields: Optional[List[Dict[str, Any]]] = None

    class Config:
        extra = "allow"

    @property
    def customFieldsDict(self) -> Dict[str, Any]:
        if not self.customFields:
            return {}
        result = {}
        for item in self.customFields:
            if isinstance(item, dict) and "key" in item:
                result[item["key"]] = item.get("value")
        return result
    
    @staticmethod
    def custom_fields_from_dict(custom_fields: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{"key": k, "value": v} for k, v in custom_fields]



class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass

class ContactOverride(ContactBase):
    pass

class ContactResponse(ContactBase):
    pass

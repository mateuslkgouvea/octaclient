from typing import Any, Dict, List, Optional
from pydantic import BaseModel, field_validator


class PhoneContact(BaseModel):
    number: str
    countryCode: str = "55"


class CustomField(BaseModel):
    key: str
    value: Any = None


class Responsible(BaseModel):
    email: str

    class Config:
        extra = "allow"

class Organization(BaseModel):
    id: str
    name: Optional[str] = None
    

    class Config:
        extra = "allow"


class ContactBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phoneContacts: Optional[List[PhoneContact]] = None
    responsible: Optional[Responsible] = None
    customFields: Optional[List[CustomField]] = None

    class Config:
        extra = "allow"

    @field_validator("customFields", mode="before")
    def convert_custom_fields(cls, v):
        
        if v is None:
            return v
        
        if isinstance(v, dict):
            return [CustomField(key = k, value = val) for k, val in v.items()]
        
        return v

    @property
    def customFieldsDict(self) -> Dict[str, Any]:
        if not self.customFields:
            return {}
        result = {}
        for item in self.customFields:
            if isinstance(item, dict) and "key" in item:
                result[item["key"]] = item.get("value")
        return result


class ContactCreate(ContactBase):
    name: str
    email: str


class ContactResponse(ContactBase):
    id: str
    organization: Optional[Organization] = None


class ContactUpdate(ContactBase):
    id: str


class ContactOverride(ContactBase):
    id: str
    name: str
    email: str

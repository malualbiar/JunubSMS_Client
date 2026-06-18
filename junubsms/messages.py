from typing import List, Optional

from .base import BaseResource
from .models import (
    CreditInfo, Contact, ContactGroup,
    DeliveryStatus, IncomingMessage, SMSResult,
)

#All user-level API operations
class MessagesResource(BaseResource):
    #Send an SMS to one or more recipients.
    def send(
        self,
        to: str,
        msg: str,
        sender_id: str = "",
        message_type: str = "text",
        unicode: bool = False,
        schedule: str = "",
        footer: str = "",
    ) -> List[SMSResult]:

        data = self._get(
            "pv",
            to=to,
            msg=msg,
            **{"from": sender_id or None},
            type=message_type,
            unicode=1 if unicode else None,
            schedule=schedule or None,
            footer=footer or None,
        )
        return [SMSResult(**item) for item in data.get("data", [])]

    def outgoing(
        self,
        count: int = 10,
        last_id: str = "",
        dst: str = "",
    ) -> List[DeliveryStatus]:
        #List outgoing SMS and their delivery statuses
        data = self._get("ds", c=count, last=last_id or None, dst=dst or None)
        return [DeliveryStatus(**item) for item in data.get("data", [])]

    def incoming(self, count: int = 10, last_id: str = "") -> List[IncomingMessage]:
        #List incoming SMS
        data = self._get("in", c=count, last=last_id or None)
        return [IncomingMessage(**item) for item in data.get("data", [])]

    def inbox(self, count: int = 10, last_id: str = "") -> List[IncomingMessage]:
        #List SMS in the user's inbox
        data = self._get("ix", c=count, last=last_id or None)
        return [IncomingMessage(**item) for item in data.get("data", [])]

    def sandbox(self, count: int = 10, last_id: str = "") -> List[IncomingMessage]:
        #List unhandled incoming SMS (sandbox)
        data = self._get("sx", c=count, last=last_id or None)
        return [IncomingMessage(**item) for item in data.get("data", [])]

    def credit(self) -> CreditInfo:
        #Get the current user's credit balance
        data = self._get("cr")
        return CreditInfo(**data.get("data", {}))

    def set_token(self) -> str:
        #Rotate and return a new API token for the current user
        data = self._get("set_token")
        return data.get("data", {}).get("h", "")

    def get_contacts(self, keyword: str, count: int = 10) -> List[Contact]:
        #Search contacts by name, mobile number, or email
        data = self._get("get_contact", kwd=keyword, c=count)
        return [Contact(**item) for item in data.get("data", [])]

    def get_contact_groups(self, keyword: str, count: int = 10) -> List[ContactGroup]:
        #Search contact groups by name or code
        data = self._get("get_contact_group", kwd=keyword, c=count)
        return [ContactGroup(**item) for item in data.get("data", [])]

    def query(self) -> dict:
        #Query the server for user data, credit, and last SMS log IDs
        data = self._get("query")
        return data.get("data", {})
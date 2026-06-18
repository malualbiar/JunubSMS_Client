from dataclasses import dataclass, field
@dataclass
class SMSResult:
    """Result for a single recipient after sending a message."""
    status: str
    to: str
    smslog_id: str
    queue: str
    error: str = "0"

    @property
    def ok(self) -> bool:
        return self.status == "OK"


@dataclass
class DeliveryStatus:
    """Delivery status for a single outgoing SMS."""
    smslog_id: str
    src: str
    dst: str
    msg: str
    dt: str
    status: str
    queue: str = ""


@dataclass
class IncomingMessage:
    """A single incoming or inbox SMS."""
    id: str
    src: str
    dst: str
    msg: str
    dt: str
    status: str
    kwd: str = ""


@dataclass
class Contact:
    """A contact from the phonebook."""
    pid: str
    p_desc: str
    p_num: str
    email: str = ""
    gpid: str = ""
    group_name: str = ""
    code: str = ""


@dataclass
class ContactGroup:
    """A contact group."""
    gpid: str
    name: str
    code: str
    total: str = "0"


@dataclass
class CreditInfo:
    """User credit / balance information."""
    balance: str
    credit: str = ""

from pydantic import BaseModel, Field, AnyHttpUrl
from typing import Optional

from uzen.models.snapshots import SnapshotBaseModel


class ScanPayload(BaseModel):
    source: str = Field(
        None,
        title="YARA rule",
        description="String containing the rules code"
    )
    target: Optional[str] = Field(
        "body",
        title="Target to scan",
        description="Target field to scan (body, whois or certificate)"
    )


class OneshotPayload(ScanPayload):
    url: AnyHttpUrl


class OneshotResponse(BaseModel):
    snapshot: SnapshotBaseModel = Field(
        None,
        title="Snapshot model",
        description="Snapshot model without id & created_at fields"
    )
    matched: bool = Field(
        None,
        title="whether matched or not",
        description="whether matched or not"
    )

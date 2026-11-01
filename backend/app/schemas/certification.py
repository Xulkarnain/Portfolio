from datetime import date

from pydantic import BaseModel, ConfigDict


class CertificationPublicResponse(BaseModel):
    title: str
    issuing_organization: str
    issue_date: date
    expiry_date: date | None
    credential_id: str | None
    credential_url: str | None
    description: str | None
    display_order: int

    model_config = ConfigDict(from_attributes=True)
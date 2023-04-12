import enum
import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class TemplateForPaymentSchema(BaseModel):
    id: int = Field(..., description="templateID")
    name: str = Field(..., description="name")
    payee_name: str = Field(..., description="payee_name")
    payee_account_number: str = Field(..., description="payee_account_number")
    template_purpose_of_payment: str = Field(..., description="template_purpose_of_payment")
    BIC: str = Field(..., description="BIC")
    INN: str = Field(..., description="INN")

    class Config:
        orm_mode = True


class TemplateForExchangeRatesSchema(BaseModel):
    currency_from: str
    currency_to: str
    exchange_rate: float
    units: float


class TransferOrderSchema(BaseModel):
    id: int
    created_at: datetime
    transfer_type_id: int
    purpose: str
    remitter_card_number: str
    payee_id: int
    sum: Decimal
    sum_commission: Decimal
    completed_at: datetime
    status: enum.Enum
    authorization_code: str
    currency_exchange: Decimal
    is_favorite: bool
    start_date: datetime
    periodicity: enum.Enum
    client_id: uuid.UUID

    class Config:
        orm_mode = True

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
    id: int = Field(..., description="transfer_order_id")

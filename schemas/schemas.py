from pydantic import BaseModel, Field


class TemplateForPayment(BaseModel):
    id: int
    name: str = Field(..., max_length=255)
    payee_name: str = Field(..., max_length=255)
    payee_account_number: str = Field(..., max_length=30)
    template_purpose_of_payment: str = Field(..., max_length=255)
    BIC: str = Field(..., max_length=9)
    INN: str = Field(..., max_length=12)

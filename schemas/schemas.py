from pydantic import BaseModel, Field


class TemplateForPaymentSchema(BaseModel):
    id: int = Field(..., description="templateID")
    name: str = Field(..., description="name")
    payee_name: str = Field(..., description="payee_name")
    payee_account_number: str = Field(..., description="payee_account_number")
    template_purpose_of_payment: str = Field(..., description="template_purpose_of_payment")
    BIC: str = Field(..., description="BIC")
    INN: str = Field(..., description="INN")

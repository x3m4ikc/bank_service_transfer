import enum

from db.database import Base
from sqlalchemy import (
    DECIMAL,
    TIMESTAMP,
    UUID,
    Boolean,
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    func,
)
from sqlalchemy.orm import mapped_column, relationship

metadata = MetaData()


class TypePayee(enum.Enum):
    INDIVIDUALS = "INDIVIDUALS"
    INDIVIDUAL_ENTEPRENEURS = "NDIVIDUAL_ENTEPRENEURS"
    ORGANIZATIONS = "ORGANIZATIONS"


class Payee(Base):
    __tablename__ = "payee"
    __metadata__ = metadata
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(TypePayee), nullable=True)
    name = Column(String(length=255))
    INN = Column(String(length=12))
    BIC = Column(String(length=9), nullable=False)
    payee_account_number = Column(String(length=255), nullable=False)
    payee_card_number = Column(String(length=255))


class AdditionalParameteres(Base):
    __tablename__ = "additional_parameteres"
    __metadata__ = metadata

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(length=255), nullable=False)
    value = Column(String(length=255), nullable=False)
    description = Column(String(length=255))
    payee_id = mapped_column(ForeignKey("payee.id"))

    payee = relationship("Payee")


class TransfersTypes(enum.Enum):
    BETWEEN_CARDS = "BETWEEN_CARDS"
    TO_ANOTHER_CARD = "TO_ANOTHER_CARD"
    BY_PHONE_NUMBER = "BY_PHONE_NUMBER"
    BY_PAYEE_DETAILS = "BY_PAYEE_DETAILS"
    FAVORITES = "FAVORITES"
    AUTOPAYMENTS = "AUTOPAYMENTS"
    BANKING_SERVICES = "BANKING_SERVICES"
    INFO_SERVISES = "INFO_SERVISES"
    PAYMENT_FOR_SERVICES = "PAYMENT_FOR_SERVICES"
    UTILITIES = "UTILITIES"
    OTHER_PAYMENTS = "OTHER_PAYMENTS"


class TransferType(Base):
    __tablename__ = "transfer_type"
    __metadata__ = metadata
    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String(length=255), nullable=False)
    currency_code = Column(String, nullable=False)
    min_commission = Column(DECIMAL, nullable=False)
    max_commission = Column(DECIMAL, nullable=False)
    percent_commission = Column(DECIMAL, nullable=False)
    commission_fix = Column(DECIMAL, nullable=False)
    min_sum = Column(DECIMAL, nullable=False)
    max_sum = Column(DECIMAL, CheckConstraint("min_sum < max_sum"))


class TransferStatus(enum.Enum):
    DRAFT = "DRAFT"
    IN_PROGRESS = "IN_PROGRESS"
    PERFORMED = "PERFORMED"
    REJECTED = "REJECTED"


class TransferPeriod(enum.Enum):
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"


class TransferOrder(Base):
    __tablename__ = "transfer_order"
    __metadata__ = metadata
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    transfer_type_id = mapped_column(ForeignKey("transfer_type.id"))
    purpose = Column(String)
    remitter_card_number = Column(String(length=16), nullable=False)
    payee_id = mapped_column(ForeignKey("payee.id"))
    sum = Column(DECIMAL, nullable=False)
    sum_commission = Column(DECIMAL, nullable=False)
    completed_at = Column(TIMESTAMP(timezone=True), nullable=False, onupdate=func.now())
    status = Column(Enum(TransferStatus), nullable=False)
    authorization_code = Column(String(length=255), nullable=False)
    currency_exchange = Column(DECIMAL, nullable=False)
    is_favorite = Column(Boolean, nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    periodicity = Column(Enum(TransferPeriod), nullable=True)
    client_id = Column(UUID, nullable=False)

    payee = relationship("Payee")
    transfer_type = relationship("TransferType")


class TemplateForPayment(Base):
    __tablename__ = "template_for_payment"
    __metadata__ = metadata
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False)
    payee_name = Column(String(length=255), nullable=False)
    payee_account_number = Column(String(length=30), nullable=False)
    template_purpose_of_payment = Column(String(length=255), nullable=False)
    BIC = Column(String(length=9), nullable=False)
    INN = Column(String(length=12), nullable=False)

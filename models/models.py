import uuid
from datetime import date
from decimal import Decimal
from enum import Enum

from sqlalchemy import CheckConstraint, ForeignKey, Integer, MetaData, String
from sqlalchemy.orm import (Mapped, declarative_base, mapped_column,
                            relationship)

Base = declarative_base()
metadata = MetaData()


class TypePayee(Enum):
    INDIVIDUALS = "INDIVIDUALS"
    INDIVIDUAL_ENTEPRENEURS = "NDIVIDUAL_ENTEPRENEURS"
    ORGANIZATIONS = "ORGANIZATIONS"


class Payee(Base):
    __tablename__ = "payee"
    __metadata__ = metadata
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[TypePayee] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(String(255))
    INN: Mapped[str] = mapped_column(String(12))
    BIC: Mapped[str] = mapped_column(String(9), nullable=False)
    payee_account_number: Mapped[str] = mapped_column(String(255), nullable=False)
    payee_card_number: Mapped[str] = mapped_column(String(255))


class AdditionalParameteres(Base):
    __tablename__ = "additional_parameteres"
    __metadata__ = metadata

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255))
    payee_id: Mapped[uuid] = mapped_column(ForeignKey("payee.id"))

    payee: Mapped["Payee"] = relationship(back_populates="additional_parameteres")


class TransfersTypes(Enum):
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
    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[TransfersTypes] = mapped_column(String(255), nullable=False)
    currency_code: Mapped[str] = mapped_column(nullable=False)
    min_commission: Mapped[Decimal] = mapped_column(nullable=False)
    max_commission: Mapped[Decimal] = mapped_column(nullable=False)
    percent_commission: Mapped[Decimal] = mapped_column(nullable=True)
    commission_fix: Mapped[Decimal] = mapped_column(nullable=False)
    min_sum: Mapped[Decimal]
    max_sum: Mapped[Decimal] = mapped_column(CheckConstraint("min_sum < max_sum"))


class TransferStatus(Enum):
    DRAFT = "DRAFT"
    IN_PROGRESS = "IN_PROGRESS"
    PERFORMED = "PERFORMED"
    REJECTED = "REJECTED"


class TransferPeriod(Enum):
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"


class TransferOrder(Base):
    __tablename__ = "transfer_order"
    __metadata__ = metadata
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[date] = mapped_column(nullable=False)
    transfer_type_id: Mapped[Integer] = mapped_column(ForeignKey("transfer_type.id"))
    purpose: Mapped[str]
    remitter_card_number: Mapped[str] = mapped_column(String(16), nullable=False)
    payee_id: Mapped[uuid] = mapped_column(ForeignKey("payee.id"))
    sum: Mapped[Decimal] = mapped_column(nullable=False)
    sum_commission: Mapped[Decimal] = mapped_column(nullable=False)
    completed_at: Mapped[date]
    status: Mapped[TransferStatus] = mapped_column(nullable=False)
    authorization_code: Mapped[str] = mapped_column(String(255), nullable=False)
    currency_exchange: Mapped[Decimal] = mapped_column(nullable=False)
    is_favorite: Mapped[bool] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(String, nullable=True)
    periodicity: Mapped[TransferPeriod] = mapped_column(String, nullable=True)
    client_id: Mapped[uuid] = mapped_column(String, nullable=False)

    payee: Mapped["Payee"] = relationship(back_populates="TransferOrder")
    transfer_type: Mapped["TransferType"] = relationship(back_populates="TransferOrder")


class TemplateForPayment(Base):
    __tablename__ = "template_for_payment"
    __metadata__ = metadata
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    payee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    payee_account_number: Mapped[str] = mapped_column(String(30), nullable=False)
    template_purpose_of_payment: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    BIC: Mapped[str] = mapped_column(String(9), nullable=False)
    INN: Mapped[str] = mapped_column(String(12), nullable=False)

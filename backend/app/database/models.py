from typing import List
from typing import Optional
from sqlalchemy import (
    ForeignKey, Column, String, Integer, Numeric, Boolean, Date, DateTime,
    Index, UniqueConstraint
)
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime

Base = declarative_base()

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    asset_type = Column(String(20), nullable=False)
    source = Column(String(50), nullable=False)
    # is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    prices = relationship("AssetPrice", back_populates="asset")

    __table_args__ = (
        Index('idx_symbol_type', 'symbol', 'asset_type'),
    )

    def __repr__(self) -> str:
        return f"Asset(id={self.id}, symbol={self.symbol}, name={self.name}, asset_type={self.asset_type}, source={self.source}, is_active={self.is_active}, created_at={self.created_at})"


class AssetPrice(Base):
    __tablename__ = "asset_prices"

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    date = Column(Date, nullable=False)
    price = Column(Numeric(20, 8), nullable=False)
    market_cap = Column(Numeric(30, 8))
    volume = Column(Numeric(20, 8))
    source = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    asset = relationship("Asset", back_populates="prices")

    __table_args__ = (
        Index('idx_asset_date', 'asset_id', 'date'),
        UniqueConstraint('asset_id', 'date', 'source', name='uix_asset_date_source'),
    )

    def __repr__(self) -> str:
        return f"AssetPrice(id={self.id}, asset_id={self.asset_id}, date={self.date}, price={self.price}, volume={self.volume}, source={self.source}, created_at={self.created_at})"

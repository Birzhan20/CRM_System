from sqlalchemy import Column, Integer, DateTime, func, String, DECIMAL, Text
from sqlalchemy.orm import relationship

from core.database import Base


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    price = Column(DECIMAL, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    ad_campaigns = relationship("AdCampaign", back_populates="service")
    contracts = relationship("Contract", back_populates="service")

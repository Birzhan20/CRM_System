from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String, Boolean
from sqlalchemy.orm import relationship
from core.database import Base


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    email = Column(String(100), unique=True, nullable=True)
    ad_campaign_id = Column(Integer, ForeignKey('ad_campaigns.id'), nullable=True)
    is_active = Column(Boolean, default=False)  # False for potential, True for active
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    ad_campaign = relationship("AdCampaign", back_populates="clients")
    contract = relationship("Contract", back_populates="client", uselist=False)
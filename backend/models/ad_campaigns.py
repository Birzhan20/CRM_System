from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String, DECIMAL
from sqlalchemy.orm import relationship
from core.database import Base


class AdCampaign(Base):
    __tablename__ = 'ad_campaigns'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    channel = Column(String(100), nullable=False)
    budget = Column(DECIMAL, nullable=False)

    service = relationship("Service", back_populates="ad_campaigns")
    clients = relationship("Client", back_populates="ad_campaign")

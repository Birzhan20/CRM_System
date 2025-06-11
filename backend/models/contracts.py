from sqlalchemy import Column, Integer, ForeignKey, String, DECIMAL, Date, DateTime, func
from sqlalchemy.orm import relationship
from core.database import Base


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    document_file = Column(String(255))
    conclusion_date = Column(Date, nullable=False)
    duration = Column(Date, nullable=True)
    amount = Column(DECIMAL, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    service = relationship("Service", back_populates="contracts")
    client = relationship("Client", back_populates="contract")

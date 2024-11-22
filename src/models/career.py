#!/usr/bin/python3

from models.main import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, UUID, String


class Career(Base):
    __tablename__ = "careers"

    id = Column(UUID, nullable=False, primary_key=True)

    name = Column(String(256), nullable=False)

    roadmap = relationship("Roadmap", back_populates="career", uselist=False)

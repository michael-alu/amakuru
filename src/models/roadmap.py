#!/usr/bin/python3

from models.main import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, UUID, ForeignKey


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(UUID, nullable=False, primary_key=True)

    link = Column(String(256), nullable=False)

    video = Column(String(256), nullable=False)

    guide = Column(String(256), nullable=True)

    career_id = Column(UUID, ForeignKey("careers.id"), unique=True)

    career = relationship("Career", back_populates="roadmap")

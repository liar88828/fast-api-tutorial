from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class UserTable(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(500), nullable=True)
    password = Column(String(100), nullable=False)
    # Relationship to products
    products = relationship("ProductTable",# must be same with name class
                            back_populates="user"## must be same with name column
                            )


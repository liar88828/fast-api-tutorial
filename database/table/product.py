from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.table.user import Base


# Base = declarative_base()


# @dataclass

class ProductTable(Base):
    __tablename__ = 'products'

    # id: int
    # name: str
    # price: float
    # quantity: int
    # description: Union[str]

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    id_user = Column(Integer, ForeignKey("users.id"))

    # Relationship to user
    user = relationship("UserTable",# must be same with name class
                        back_populates="products"# must be same with name column
                        )

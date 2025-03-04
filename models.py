from sqlalchemy import Column, Integer, String
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    ciudad = Column(String, index=True)
    estado_civil = Column(String, index=True)
    cedula = Column(String, index=True)
from pydantic import BaseModel

class Cliente(BaseModel):
    id: int
    nombre: str
    ciudad: str
    estado_civil: str
    cedula: str

class ClienteUpdate(BaseModel):
    nombre: str
    ciudad: str
    estado_civil: str
    cedula: str
    
class ClienteResponse(BaseModel):
    id: int
    nombre: str
    ciudad: str
    estado_civil: str
    
    class Config:
        from_attributes = True
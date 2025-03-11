from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import database
import schemas
from database import engine, SessionLocal
from fastapi.responses import JSONResponse

# Crear todas las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

# Crea una instancia de FastAPI
app = FastAPI(
    title="API Clientes",
    description="API para gestionar clientes",
    version="1.0.0"
)

#obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()  #Crea una nueva sesión de base de datos
    try:
        yield db  #Devuelve la sesión al endpoint que la necesite
    finally:
        db.close()  #Cierra la sesión después de usarla


# Ruta raiz
@app.get("/")
def health_check():
    return{"status":"ok"}

# Obtener todos los clientes
@app.get(
    "/clientes", 
    response_model=list[schemas.ClienteResponse], 
    summary="Obtener todos los clientes", 
    description="Obtiene todos los clientes de la tabla",
    status_code=status.HTTP_200_OK
)
def get_clientes(db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).all()
    return clientes

# Obtener un cliente por ID
@app.get(
    "/clientes/by_id/{cliente_id}", 
    response_model=schemas.ClienteResponse, 
    summary="Obtener un cliente por ID", 
    description="Obtiene un cliente por su ID",
    status_code=status.HTTP_200_OK
)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


# Crear un nuevo cliente
@app.post(
    "/clientes/create", 
    response_model=schemas.ClienteResponse, 
    summary="Crear un nuevo cliente", 
    description="Crea un nuevo cliente en la tabla",
    status_code=status.HTTP_201_CREATED
)
def create_cliente(cliente: schemas.Cliente, db: Session = Depends(get_db)):
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)  
    return cliente


# Actualizar un cliente existente por su ID
@app.put(
    "/clientes/update/{cliente_id}", 
    response_model=schemas.ClienteResponse, 
    summary="Actualizar un cliente existente", 
    description="Actualiza un cliente existente en la tabla",
    status_code=status.HTTP_200_OK
)
def update_cliente(cliente_id: int, cliente: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db_cliente.nombre = cliente.nombre 
    db_cliente.ciudad = cliente.ciudad
    db_cliente.estado_civil = cliente.estado_civil
    db_cliente.cedula = cliente.cedula
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


# Eliminar un cliente existente por su ID
@app.delete(
    "/clientes/delete/{cliente_id}",
    summary="Eliminar un cliente existente", 
    description="Elimina un cliente existente de la tabla",
    status_code=status.HTTP_200_OK
)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_cliente)
    db.commit()
    return db_cliente
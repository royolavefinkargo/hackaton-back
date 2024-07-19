from fastapi import FastAPI, HTTPException
from db import get_db_connection
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()


# Define una lista de orígenes permitidos (por ejemplo, el frontend de tu aplicación)
origins = [
    "http://localhost:5173",  # Asegúrate de que este es el origen correcto para tu frontend
    "http://127.0.0.1:5173",
]

# Agrega el middleware CORS a tu aplicación FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Los orígenes que quieres permitir (puedes usar ["*"] para todos los orígenes)
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos
    allow_headers=["*"],  # Encabezados permitidos
)


class Usuario(BaseModel):
    nombre: str
    correo_electronico: str
    rol: str

class Ticket(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: str
    prioridad: str
    usuario_id: int




@app.get("/usuarios/", response_model=List[Usuario])
def obtener_usuarios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios;")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return usuarios

# Ruta para obtener un usuario específico por ID
@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = %s;", (usuario_id,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Ruta para obtener todos los tickets
@app.get("/tickets/", response_model=List[Ticket])
def obtener_tickets():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tickets;")
    tickets = cur.fetchall()
    cur.close()
    conn.close()
    return tickets

# Ruta para obtener un ticket específico por ID
@app.get("/tickets/{ticket_id}", response_model=Ticket)
def obtener_ticket(ticket_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tickets WHERE id = %s;", (ticket_id,))
    ticket = cur.fetchone()
    cur.close()
    conn.close()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket

# Ruta para agregar un nuevo usuario
@app.post("/usuarios/")
def agregar_usuario(usuario: Usuario):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (nombre, correo_electronico, rol) VALUES (%s, %s, %s) RETURNING id;",
                (usuario.nombre, usuario.correo_electronico, usuario.rol))
    user_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return {"id": user_id}

# Ruta para agregar un nuevo ticket
@app.post("/tickets/")
def agregar_ticket(ticket: Ticket):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tickets (titulo, descripcion, estado, prioridad, usuario_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                (ticket.titulo, ticket.descripcion, ticket.estado, ticket.prioridad, ticket.usuario_id))
    ticket_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return {"id": ticket_id}

# Ruta para modificar un ticket
@app.put("/tickets/{ticket_id}")
def modificar_ticket(ticket_id: int, ticket: Ticket):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tickets SET titulo=%s, descripcion=%s, estado=%s, prioridad=%s, usuario_id=%s WHERE id=%s;",
                (ticket.titulo, ticket.descripcion, ticket.estado, ticket.prioridad, ticket.usuario_id, ticket_id))
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return {"mensaje": "Ticket actualizado"}

# Ruta para eliminar un ticket
@app.delete("/tickets/{ticket_id}")
def eliminar_ticket(ticket_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tickets WHERE id=%s;", (ticket_id,))
    deleted_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return {"mensaje": "Ticket eliminado"}
import streamlit as st
import requests
import matplotlib.pyplot as plt

# URL base de la API de FastAPI
FASTAPI_BASE_URL = "http://localhost:8000"

# Función para obtener tickets desde FastAPI
def obtener_tickets():
    response = requests.get(f"{FASTAPI_BASE_URL}/tickets/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("No se pudieron obtener los tickets desde el backend.")
        return []

# Función para generar y mostrar una gráfica de la cantidad de tickets por estado
def mostrar_grafica_tickets(tickets):
    # Contar tickets por estado
    estados = {}
    for ticket in tickets:
        if ticket['estado'] in estados:
            estados[ticket['estado']] += 1
        else:
            estados[ticket['estado']] = 1
    
    # Crear la gráfica
    fig, ax = plt.subplots()
    ax.bar(estados.keys(), estados.values())
    ax.set_xlabel('Estado')
    ax.set_ylabel('Cantidad de Tickets')
    ax.set_title('Cantidad de Tickets por Estado')
    
    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)

# Mostrar tickets y la gráfica en la aplicación Streamlit
tickets = obtener_tickets()
if tickets:
    mostrar_grafica_tickets(tickets)
else:
    st.write("No hay tickets para mostrar.")
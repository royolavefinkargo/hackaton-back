# Usar una imagen base oficial de Python
FROM python:3.11

# Instalar supervisord
RUN apt-get update && apt-get install -y supervisor

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de la aplicación al directorio de trabajo
COPY . /app

# Instalar las dependencias del proyecto
# Asegúrate de tener un archivo requirements.txt en tu directorio proyecto_soporte que incluya todas las dependencias necesarias
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Configurar supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Exponer los puertos para FastAPI y Streamlit
EXPOSE 8000 8501

# Comando para ejecutar supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
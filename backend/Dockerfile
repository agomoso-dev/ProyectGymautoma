FROM python:3.12.2

# Crear usuario (opcional)
RUN addgroup --system app && adduser --system --group app -u 1000

# Crear directorio de trabajo
WORKDIR /app

# Copiar todo el código al contenedor
COPY . /app

# Instalar dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Script para esperar a que la base de datos esté lista
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copiar el script de arranque
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Comando de arranque
ENTRYPOINT ["sh", "/entrypoint.sh"]

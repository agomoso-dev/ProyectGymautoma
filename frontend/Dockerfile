#  Etapa de build
FROM node:23-alpine AS builder

# Crear directorio de trabajo
WORKDIR /app

# Copiar solo los archivos necesarios para instalar dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código de la app
COPY . .

# Compilar la app para producción
RUN npm run build

# Etapa de producción con Nginx
FROM nginx:stable-alpine AS runner


# Copiar archivos estáticos compilados desde la etapa de build
COPY --from=builder /app/build /usr/share/nginx/html

# Exponer el puerto
EXPOSE 80

# Comando de inicio de Nginx
CMD ["nginx", "-g", "daemon off;"]
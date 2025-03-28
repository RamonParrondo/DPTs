#!/bin/bash

# Script de instalación y configuración del Sistema de Gestión de DPTs
# Este script guiará al usuario a través del proceso de configuración inicial

echo "=================================================="
echo "  Instalación del Sistema de Gestión de DPTs"
echo "=================================================="
echo ""

# Verificar requisitos previos
echo "Verificando requisitos previos..."

# Verificar Docker
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✅ Docker y Docker Compose están instalados"
else
    echo "❌ Docker o Docker Compose no están instalados"
    echo "Por favor, instala Docker y Docker Compose antes de continuar:"
    echo "https://docs.docker.com/get-docker/"
    echo "https://docs.docker.com/compose/install/"
    exit 1
fi

# Crear directorios necesarios
echo ""
echo "Creando estructura de directorios..."
mkdir -p data/uploads data/reports

# Crear archivo .env
echo ""
echo "Configurando variables de entorno..."
echo ""

# Solicitar API key de Gemini
read -p "Ingresa tu API key de Google Gemini (deja en blanco para omitir): " GEMINI_API_KEY

# Solicitar token de GitHub
read -p "Ingresa tu token de GitHub (deja en blanco para omitir): " GITHUB_TOKEN

# Solicitar repositorio de GitHub
read -p "Ingresa el nombre de tu repositorio GitHub (formato: usuario/repo): " GITHUB_REPO

# Crear archivo .env
echo "GEMINI_API_KEY=$GEMINI_API_KEY" > .env
echo "GITHUB_TOKEN=$GITHUB_TOKEN" >> .env
echo "GITHUB_REPO=$GITHUB_REPO" >> .env

echo "✅ Archivo .env creado correctamente"

# Construir y levantar los contenedores
echo ""
echo "Construyendo y levantando contenedores Docker..."
docker-compose up -d --build

# Esperar a que la base de datos esté lista
echo ""
echo "Esperando a que la base de datos esté lista..."
sleep 10

# Inicializar los formatos de DPT
echo ""
echo "Inicializando formatos de DPT en la base de datos..."
docker-compose exec dpt-manager-app python init_formats.py

echo ""
echo "=================================================="
echo "  🎉 Instalación completada con éxito 🎉"
echo "=================================================="
echo ""
echo "Puedes acceder a la aplicación en: http://localhost:5000"
echo "Para acceder a pgAdmin: http://localhost:5050"
echo "  - Usuario: admin@example.com"
echo "  - Contraseña: admin"
echo ""
echo "Para detener la aplicación: docker-compose down"
echo "Para reiniciar la aplicación: docker-compose restart"
echo ""
echo "Gracias por instalar el Sistema de Gestión de DPTs"

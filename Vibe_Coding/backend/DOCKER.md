# 🐳 Guía de Despliegue con Docker - QuickTask API

Esta guía explica cómo desplegar QuickTask API usando **Docker** y **Docker Compose**.

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Archivos de Configuración](#archivos-de-configuración)
3. [Despliegue Rápido](#despliegue-rápido)
4. [Modos de Despliegue](#modos-de-despliegue)
5. [Comandos Docker](#comandos-docker)
6. [Gestión de Datos](#gestión-de-datos)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Requisitos Previos

### Software Necesario

```bash
# Verificar instalación de Docker
docker --version
# Docker version 24.0.0 o superior

# Verificar Docker Compose
docker-compose --version
# Docker Compose version 2.20.0 o superior
```

### Instalación de Docker

#### Linux (Ubuntu/Debian)
```bash
# Actualizar repositorios
sudo apt-get update

# Instalar Docker
sudo apt-get install docker.io docker-compose

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Reiniciar sesión o ejecutar
newgrp docker
```

#### macOS
```bash
# Instalar Docker Desktop desde:
# https://www.docker.com/products/docker-desktop
```

#### Windows
```bash
# Instalar Docker Desktop desde:
# https://www.docker.com/products/docker-desktop
# Habilitar WSL 2
```

---

## 📁 Archivos de Configuración

### Archivos Creados

```
backend/
├── Dockerfile                 # Dockerfile básico
├── Dockerfile.prod            # Dockerfile optimizado (producción)
├── docker-compose.yml         # Compose estándar
├── docker-compose.dev.yml     # Compose con hot-reload
├── docker-compose.prod.yml    # Compose de producción
├── .dockerignore              # Archivos a ignorar
└── docker.sh                  # Script de gestión
```

### Descripción de Archivos

| Archivo | Propósito |
|---------|-----------|
| `Dockerfile` | Imagen Docker básica para desarrollo |
| `Dockerfile.prod` | Imagen multi-stage optimizada |
| `docker-compose.yml` | Configuración estándar |
| `docker-compose.dev.yml` | Con auto-reload para desarrollo |
| `docker-compose.prod.yml` | Sin montaje de código (producción) |
| `.dockerignore` | Excluir archivos innecesarios |
| `docker.sh` | Script helper para gestión |

---

## 🚀 Despliegue Rápido

### Opción 1: Usando Docker Compose (Recomendado)

```bash
# 1. Navegar al directorio backend
cd backend

# 2. Levantar el contenedor
docker-compose up -d

# 3. Ver logs
docker-compose logs -f

# 4. Probar la API
curl http://localhost:8000/health
```

### Opción 2: Usando el Script Helper

```bash
# 1. Hacer ejecutable (primera vez)
chmod +x docker.sh

# 2. Levantar contenedor
./docker.sh up

# 3. Ver logs
./docker.sh logs

# 4. Ver estado
./docker.sh status
```

### Opción 3: Docker Manual

```bash
# 1. Construir imagen
docker build -t quicktask-api .

# 2. Ejecutar contenedor
docker run -d \
  --name quicktask-api \
  -p 8000:8000 \
  -v quicktask-data:/app/data \
  quicktask-api

# 3. Ver logs
docker logs -f quicktask-api
```

---

## 🎯 Modos de Despliegue

### 1. Modo Desarrollo (con Hot-Reload)

**Características:**
- ✅ Auto-reload cuando cambias código
- ✅ Código montado como volumen
- ✅ BD de desarrollo separada
- ✅ Debug habilitado

```bash
# Levantar
docker-compose -f docker-compose.dev.yml up -d

# Ver logs en tiempo real
docker-compose -f docker-compose.dev.yml logs -f

# Detener
docker-compose -f docker-compose.dev.yml down
```

**Ventajas:**
- 🚀 Cambios de código se reflejan inmediatamente
- 🐛 Fácil debugging
- 📝 No necesitas reconstruir la imagen

### 2. Modo Estándar

**Características:**
- ✅ Balance entre desarrollo y producción
- ✅ Código montado (opcional)
- ✅ Restart automático

```bash
# Levantar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### 3. Modo Producción

**Características:**
- ✅ Imagen optimizada multi-stage
- ✅ Usuario no-root (seguridad)
- ✅ Sin montaje de código
- ✅ Límites de recursos
- ✅ Health checks configurados

```bash
# Levantar
docker-compose -f docker-compose.prod.yml up -d

# Ver estado
docker-compose -f docker-compose.prod.yml ps

# Detener
docker-compose -f docker-compose.prod.yml down
```

---

## 🛠️ Comandos Docker

### Gestión de Contenedores

```bash
# Levantar contenedor en background
docker-compose up -d

# Levantar y ver logs
docker-compose up

# Detener contenedor
docker-compose down

# Reiniciar contenedor
docker-compose restart

# Ver estado
docker-compose ps

# Ver logs (últimas 100 líneas)
docker-compose logs --tail=100

# Seguir logs en tiempo real
docker-compose logs -f
```

### Construcción de Imágenes

```bash
# Construir imagen
docker-compose build

# Reconstruir sin caché
docker-compose build --no-cache

# Construir y levantar
docker-compose up --build -d
```

### Ejecución de Comandos

```bash
# Abrir shell en el contenedor
docker-compose exec quicktask-api /bin/bash

# Ejecutar comando específico
docker-compose exec quicktask-api python --version

# Ejecutar tests
docker-compose exec quicktask-api pytest -v

# Ver variables de entorno
docker-compose exec quicktask-api env
```

### Gestión de Volúmenes

```bash
# Listar volúmenes
docker volume ls

# Inspeccionar volumen
docker volume inspect quicktask-sqlite-data

# Eliminar volumen (¡CUIDADO! Borra datos)
docker volume rm quicktask-sqlite-data

# Backup de volumen
docker run --rm \
  -v quicktask-sqlite-data:/data \
  -v $(pwd):/backup \
  busybox tar czf /backup/quicktask-backup.tar.gz -C /data .
```

---

## 💾 Gestión de Datos

### Persistencia de la Base de Datos

La base de datos SQLite se almacena en un **volumen Docker nombrado**:

```yaml
volumes:
  quicktask-data:
    driver: local
    name: quicktask-sqlite-data
```

**Ubicación en el contenedor:** `/app/data/quicktask.db`

### Backup de Datos

#### Método 1: Backup Manual
```bash
# Crear backup
docker-compose exec quicktask-api cp /app/data/quicktask.db /app/data/quicktask-backup.db

# Copiar backup al host
docker cp quicktask-api:/app/data/quicktask-backup.db ./backup.db
```

#### Método 2: Backup de Volumen
```bash
# Crear backup comprimido
docker run --rm \
  -v quicktask-sqlite-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/db-backup-$(date +%Y%m%d).tar.gz -C /data .
```

### Restaurar Datos

```bash
# Desde archivo de backup
docker cp ./backup.db quicktask-api:/app/data/quicktask.db

# Reiniciar contenedor
docker-compose restart
```

### Limpiar Datos

```bash
# Detener y eliminar contenedor + volumen
docker-compose down -v

# Solo eliminar volumen (mantener contenedor)
docker volume rm quicktask-sqlite-data
```

---

## 🧪 Probar la API

### 1. Health Check

```bash
# Verificar que la API está funcionando
curl http://localhost:8000/health

# Respuesta esperada:
# {"status":"healthy","service":"QuickTask API"}
```

### 2. Documentación Interactiva

Abrir en el navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Crear una Tarea

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tarea desde Docker",
    "description": "Probando la API en contenedor",
    "completed": false
  }'
```

### 4. Listar Tareas

```bash
curl http://localhost:8000/tasks
```

### 5. Script de Test Completo

```bash
#!/bin/bash

echo "🧪 Probando QuickTask API en Docker..."

# 1. Health check
echo -e "\n1️⃣ Health Check:"
curl -s http://localhost:8000/health | jq

# 2. Crear tarea
echo -e "\n2️⃣ Crear tarea:"
TASK=$(curl -s -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Docker","description":"Tarea de prueba"}')
echo $TASK | jq

# 3. Obtener ID de la tarea
TASK_ID=$(echo $TASK | jq -r '.id')
echo "ID de tarea creada: $TASK_ID"

# 4. Listar tareas
echo -e "\n3️⃣ Listar tareas:"
curl -s http://localhost:8000/tasks | jq

# 5. Marcar como completada
echo -e "\n4️⃣ Marcar como completada:"
curl -s -X PATCH "http://localhost:8000/tasks/$TASK_ID" \
  -H "Content-Type: application/json" \
  -d '{"completed":true}' | jq

echo -e "\n✅ Test completado"
```

---

## 📊 Monitoreo

### Ver Recursos Usados

```bash
# Ver uso de CPU, memoria y red
docker stats quicktask-api

# Ver uso de forma continua
docker stats --no-stream quicktask-api
```

### Health Check Status

```bash
# Ver estado de health check
docker inspect --format='{{.State.Health.Status}}' quicktask-api

# Ver logs de health check
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' quicktask-api
```

### Logs Detallados

```bash
# Últimos 50 logs
docker-compose logs --tail=50 quicktask-api

# Solo errores
docker-compose logs quicktask-api | grep -i error

# Logs con timestamp
docker-compose logs -t quicktask-api
```

---

## 🐛 Troubleshooting

### Problema: Puerto 8000 ya en uso

```bash
# Ver qué proceso usa el puerto
sudo lsof -i :8000

# O cambiar el puerto en docker-compose.yml:
ports:
  - "8080:8000"  # Puerto host:contenedor
```

### Problema: Contenedor no inicia

```bash
# Ver logs de error
docker-compose logs quicktask-api

# Ver eventos
docker events --since 1h

# Inspeccionar contenedor
docker inspect quicktask-api
```

### Problema: Base de datos corrupta

```bash
# Detener contenedor
docker-compose down

# Eliminar volumen
docker volume rm quicktask-sqlite-data

# Volver a levantar
docker-compose up -d
```

### Problema: Cambios en código no se reflejan

```bash
# Reconstruir imagen
docker-compose up --build -d

# O usar modo desarrollo con hot-reload
docker-compose -f docker-compose.dev.yml up -d
```

### Problema: Permisos en Linux

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Reiniciar sesión
newgrp docker

# Verificar
docker ps
```

---

## 🎯 Comandos Usando el Script Helper

El script `docker.sh` simplifica la gestión:

```bash
# Ver ayuda
./docker.sh help

# Construir imagen
./docker.sh build

# Levantar (desarrollo)
./docker.sh up

# Levantar (producción)
./docker.sh up-prod

# Ver logs
./docker.sh logs

# Ver estado
./docker.sh status

# Abrir shell
./docker.sh shell

# Ejecutar tests
./docker.sh test

# Reiniciar
./docker.sh restart

# Detener
./docker.sh down

# Limpiar todo
./docker.sh clean
```

---

## 📝 Resumen de Pasos

### Despliegue Inicial

```bash
# 1. Clonar/navegar al proyecto
cd backend

# 2. Construir imagen
docker-compose build

# 3. Levantar contenedor
docker-compose up -d

# 4. Verificar
curl http://localhost:8000/health

# 5. Abrir documentación
open http://localhost:8000/docs
```

### Desarrollo Diario

```bash
# Levantar con hot-reload
docker-compose -f docker-compose.dev.yml up -d

# Ver logs
docker-compose logs -f

# Ejecutar tests
docker-compose exec quicktask-api pytest

# Detener
docker-compose down
```

### Despliegue a Producción

```bash
# 1. Construir imagen optimizada
docker-compose -f docker-compose.prod.yml build

# 2. Levantar
docker-compose -f docker-compose.prod.yml up -d

# 3. Verificar estado
docker-compose -f docker-compose.prod.yml ps

# 4. Monitorear
docker stats quicktask-api-prod
```

---

## 🌟 Mejores Prácticas

### Desarrollo
- ✅ Usar `docker-compose.dev.yml` con hot-reload
- ✅ Montar código como volumen
- ✅ Usar BD de desarrollo separada
- ✅ Ver logs en tiempo real

### Producción
- ✅ Usar `Dockerfile.prod` multi-stage
- ✅ No montar código
- ✅ Configurar health checks
- ✅ Establecer límites de recursos
- ✅ Usar usuario no-root
- ✅ Hacer backups regulares

### Seguridad
- ✅ No exponer puertos innecesarios
- ✅ Usar secrets para credenciales
- ✅ Mantener imágenes actualizadas
- ✅ Escanear vulnerabilidades

---

## 📚 Recursos Adicionales

- [Docker Docs](https://docs.docker.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [FastAPI Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**🐳 QuickTask API dockerizada y lista para desplegar!** 🚀

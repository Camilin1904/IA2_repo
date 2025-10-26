# 🚀 Cómo Ejecutar y Probar QuickTask con Docker

## 📋 Pasos Detallados para Despliegue Local

---

## 🔧 Paso 1: Verificar Requisitos Previos

### 1.1 Verificar Docker

```bash
# Verificar que Docker está instalado
docker --version

# Debe mostrar algo como:
# Docker version 24.0.0, build abc1234
```

### 1.2 Verificar Docker Compose

```bash
# Verificar Docker Compose
docker-compose --version

# Debe mostrar algo como:
# Docker Compose version v2.20.0
```

### 1.3 Si no están instalados

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker
```

**macOS/Windows:**
- Descargar Docker Desktop: https://www.docker.com/products/docker-desktop

---

## 📦 Paso 2: Preparar el Proyecto

### 2.1 Navegar al directorio

```bash
cd /home/camilin/Documents/Icesi/IA2/IA2_repo/Vibe_Coding/backend
```

### 2.2 Verificar archivos Docker

```bash
# Listar archivos de Docker
ls -la | grep -E "Dockerfile|docker-compose|\.dockerignore"

# Deberías ver:
# - Dockerfile
# - Dockerfile.prod
# - docker-compose.yml
# - docker-compose.dev.yml
# - docker-compose.prod.yml
# - .dockerignore
# - docker.sh
```

---

## 🚀 Paso 3: Opción A - Despliegue Estándar

### 3.1 Levantar el contenedor

```bash
# Construir y levantar en modo detached (background)
docker-compose up -d
```

**Salida esperada:**
```
Creating network "quicktask-network" with driver "bridge"
Creating volume "quicktask-sqlite-data" with driver "local"
Building quicktask-api
[+] Building 45.2s (12/12) FINISHED
Creating quicktask-api ... done
```

### 3.2 Verificar que está corriendo

```bash
# Ver estado del contenedor
docker-compose ps
```

**Salida esperada:**
```
      Name                Command           State           Ports
------------------------------------------------------------------------
quicktask-api   uvicorn main:app ...   Up      0.0.0.0:8000->8000/tcp
```

### 3.3 Ver logs

```bash
# Ver logs del contenedor
docker-compose logs -f
```

**Salida esperada:**
```
quicktask-api | INFO:     Started server process [1]
quicktask-api | INFO:     Waiting for application startup.
quicktask-api | INFO:     Application startup complete.
quicktask-api | INFO:     Uvicorn running on http://0.0.0.0:8000
```

Presiona `Ctrl+C` para salir de los logs.

---

## 🚀 Paso 4: Opción B - Despliegue con Hot-Reload (Desarrollo)

### 4.1 Levantar en modo desarrollo

```bash
# Levantar con auto-reload
docker-compose -f docker-compose.dev.yml up -d
```

### 4.2 Verificar

```bash
docker-compose -f docker-compose.dev.yml logs -f
```

**Ventaja:** Los cambios en el código se reflejan automáticamente sin reiniciar.

---

## 🚀 Paso 5: Opción C - Usando el Script Helper

### 5.1 Dar permisos (primera vez)

```bash
chmod +x docker.sh
```

### 5.2 Levantar con el script

```bash
./docker.sh up
```

**Salida esperada:**
```
╔════════════════════════════════════════╗
║     🐳 QuickTask Docker Manager       ║
╚════════════════════════════════════════╝

🚀 Levantando contenedor (desarrollo)...

Creating quicktask-api-dev ... done

✅ Contenedor levantado exitosamente
📡 API disponible en: http://localhost:8000
📚 Documentación en: http://localhost:8000/docs
```

---

## ✅ Paso 6: Verificar que la API Está Funcionando

### 6.1 Health Check

```bash
curl http://localhost:8000/health
```

**Salida esperada:**
```json
{
  "status": "healthy",
  "service": "QuickTask API"
}
```

### 6.2 Endpoint raíz

```bash
curl http://localhost:8000/
```

**Salida esperada:**
```json
{
  "message": "Bienvenido a QuickTask API",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

### 6.3 Documentación interactiva

Abrir en el navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🧪 Paso 7: Probar la API con Ejemplos

### 7.1 Crear una tarea

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primera tarea en Docker",
    "description": "Probando la API dockerizada",
    "due_date": "2025-10-30T10:00:00",
    "completed": false
  }'
```

**Salida esperada:**
```json
{
  "id": 1,
  "title": "Mi primera tarea en Docker",
  "description": "Probando la API dockerizada",
  "due_date": "2025-10-30T10:00:00",
  "completed": false,
  "created_at": "2025-10-26T15:30:00.123456"
}
```

### 7.2 Listar todas las tareas

```bash
curl http://localhost:8000/tasks
```

**Salida esperada:**
```json
{
  "total": 1,
  "tasks": [
    {
      "id": 1,
      "title": "Mi primera tarea en Docker",
      "description": "Probando la API dockerizada",
      "due_date": "2025-10-30T10:00:00",
      "completed": false,
      "created_at": "2025-10-26T15:30:00.123456"
    }
  ]
}
```

### 7.3 Obtener tarea por ID

```bash
curl http://localhost:8000/tasks/1
```

### 7.4 Marcar como completada

```bash
curl -X PATCH "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 7.5 Actualizar título

```bash
curl -X PATCH "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Tarea actualizada desde Docker"}'
```

### 7.6 Eliminar tarea

```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

**Respuesta esperada:** Status 204 (No Content)

---

## 🧪 Paso 8: Script de Test Completo

### 8.1 Crear script de test

```bash
cat > test_docker_api.sh << 'EOF'
#!/bin/bash

echo "🧪 Probando QuickTask API en Docker..."

# Health check
echo -e "\n1️⃣ Health Check:"
curl -s http://localhost:8000/health | jq

# Crear tarea
echo -e "\n2️⃣ Crear tarea:"
TASK=$(curl -s -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test desde script",
    "description": "Probando API dockerizada",
    "completed": false
  }')
echo $TASK | jq

# Extraer ID
TASK_ID=$(echo $TASK | jq -r '.id')
echo "📌 ID de tarea: $TASK_ID"

# Listar tareas
echo -e "\n3️⃣ Listar todas las tareas:"
curl -s http://localhost:8000/tasks | jq

# Actualizar tarea
echo -e "\n4️⃣ Marcar como completada:"
curl -s -X PATCH "http://localhost:8000/tasks/$TASK_ID" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}' | jq

# Filtrar completadas
echo -e "\n5️⃣ Listar solo completadas:"
curl -s "http://localhost:8000/tasks?completed=true" | jq

# Eliminar tarea
echo -e "\n6️⃣ Eliminar tarea:"
curl -s -X DELETE "http://localhost:8000/tasks/$TASK_ID"
echo "Tarea eliminada"

echo -e "\n✅ Test completado exitosamente"
EOF

chmod +x test_docker_api.sh
```

### 8.2 Ejecutar script

```bash
./test_docker_api.sh
```

---

## 📊 Paso 9: Monitoreo y Diagnóstico

### 9.1 Ver estado del contenedor

```bash
# Estado básico
docker-compose ps

# Estado detallado
./docker.sh status
```

### 9.2 Ver logs en tiempo real

```bash
# Con docker-compose
docker-compose logs -f

# Con el script
./docker.sh logs
```

### 9.3 Ver uso de recursos

```bash
# CPU, memoria, red
docker stats quicktask-api

# O con el script
./docker.sh status
```

### 9.4 Abrir shell en el contenedor

```bash
# Con docker-compose
docker-compose exec quicktask-api /bin/bash

# Con el script
./docker.sh shell
```

**Dentro del contenedor:**
```bash
# Ver archivos
ls -la

# Ver base de datos
ls -la data/

# Ejecutar Python
python --version

# Ejecutar tests
pytest -v

# Salir
exit
```

---

## 🧹 Paso 10: Gestión del Contenedor

### 10.1 Detener el contenedor

```bash
# Con docker-compose
docker-compose down

# Con el script
./docker.sh down
```

### 10.2 Reiniciar el contenedor

```bash
# Con docker-compose
docker-compose restart

# Con el script
./docker.sh restart
```

### 10.3 Ver logs históricos

```bash
# Últimas 50 líneas
docker-compose logs --tail=50

# Desde hace 1 hora
docker-compose logs --since 1h
```

### 10.4 Reconstruir imagen

```bash
# Sin caché (fuerza rebuild completo)
docker-compose build --no-cache

# Y levantar
docker-compose up -d --build
```

---

## 💾 Paso 11: Gestión de Datos

### 11.1 Ver volúmenes

```bash
# Listar volúmenes
docker volume ls | grep quicktask

# Inspeccionar volumen
docker volume inspect quicktask-sqlite-data
```

### 11.2 Backup de base de datos

```bash
# Método 1: Copiar archivo directamente
docker cp quicktask-api:/app/data/quicktask.db ./backup-$(date +%Y%m%d).db

# Método 2: Backup de volumen
docker run --rm \
  -v quicktask-sqlite-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/db-backup-$(date +%Y%m%d).tar.gz -C /data .
```

### 11.3 Restaurar backup

```bash
# Copiar backup al contenedor
docker cp ./backup-20251026.db quicktask-api:/app/data/quicktask.db

# Reiniciar
docker-compose restart
```

---

## 🐛 Paso 12: Troubleshooting

### 12.1 Contenedor no inicia

```bash
# Ver logs de error
docker-compose logs

# Ver eventos de Docker
docker events --since 10m

# Inspeccionar contenedor
docker inspect quicktask-api
```

### 12.2 Puerto 8000 ocupado

```bash
# Ver qué proceso usa el puerto
sudo lsof -i :8000

# O cambiar puerto en docker-compose.yml
ports:
  - "8080:8000"
```

### 12.3 Limpiar todo y empezar de nuevo

```bash
# Detener y eliminar todo
docker-compose down -v --rmi all

# O usar el script
./docker.sh clean

# Volver a construir
docker-compose build
docker-compose up -d
```

---

## ✅ Checklist de Verificación

Usa esta lista para verificar que todo funciona:

- [ ] ✅ Docker y Docker Compose instalados
- [ ] ✅ Contenedor levantado: `docker-compose ps`
- [ ] ✅ Health check responde: `curl http://localhost:8000/health`
- [ ] ✅ Endpoint raíz responde: `curl http://localhost:8000/`
- [ ] ✅ Swagger UI accesible: http://localhost:8000/docs
- [ ] ✅ Puedo crear una tarea
- [ ] ✅ Puedo listar tareas
- [ ] ✅ Puedo actualizar una tarea
- [ ] ✅ Puedo eliminar una tarea
- [ ] ✅ Los logs se ven sin errores
- [ ] ✅ La base de datos persiste después de reiniciar

---

## 🎓 Comandos de Referencia Rápida

```bash
# LEVANTAR
docker-compose up -d              # Estándar
docker-compose -f docker-compose.dev.yml up -d  # Desarrollo
./docker.sh up                    # Con script

# VER ESTADO
docker-compose ps                 # Estado
docker-compose logs -f            # Logs
./docker.sh status                # Con script

# INTERACTUAR
docker-compose exec quicktask-api /bin/bash  # Shell
./docker.sh shell                 # Con script

# TESTS
docker-compose exec quicktask-api pytest -v
./docker.sh test

# DETENER
docker-compose down               # Detener
docker-compose restart            # Reiniciar
./docker.sh down                  # Con script

# LIMPIAR
docker-compose down -v            # Con volúmenes
./docker.sh clean                 # Todo
```

---

## 🎉 ¡Listo!

Si completaste todos los pasos y el checklist, tu QuickTask API está:

```
╔═══════════════════════════════════════════════════╗
║                                                   ║
║     ✅  QUICKTASK API DOCKERIZADA                ║
║         FUNCIONANDO CORRECTAMENTE                ║
║                                                   ║
║     🐳 Docker │ 🚀 FastAPI │ 💾 SQLite           ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
```

**Endpoints disponibles:**
- 🏠 http://localhost:8000
- 📚 http://localhost:8000/docs
- 💚 http://localhost:8000/health

---

**¿Problemas?** Revisa la sección de [Troubleshooting](#-paso-12-troubleshooting) o consulta [DOCKER.md](DOCKER.md)

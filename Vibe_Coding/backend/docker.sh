#!/bin/bash

# Script para gestionar el despliegue de QuickTask con Docker
# Uso: ./docker.sh [comando]

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
show_banner() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║     🐳 QuickTask Docker Manager       ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Función de ayuda
show_help() {
    echo "Uso: ./docker.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  build         - Construir imagen Docker"
    echo "  up            - Levantar contenedor (desarrollo)"
    echo "  up-prod       - Levantar contenedor (producción)"
    echo "  down          - Detener y eliminar contenedor"
    echo "  restart       - Reiniciar contenedor"
    echo "  logs          - Ver logs del contenedor"
    echo "  shell         - Abrir shell en el contenedor"
    echo "  test          - Ejecutar tests en el contenedor"
    echo "  clean         - Limpiar contenedores, imágenes y volúmenes"
    echo "  status        - Ver estado del contenedor"
    echo "  help          - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  ./docker.sh build"
    echo "  ./docker.sh up"
    echo "  ./docker.sh logs"
}

# Verificar si Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker no está instalado${NC}"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose no está instalado${NC}"
        exit 1
    fi
}

# Construir imagen
build_image() {
    echo -e "${BLUE}🔨 Construyendo imagen Docker...${NC}\n"
    docker-compose build
    
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✅ Imagen construida exitosamente${NC}"
    else
        echo -e "\n${RED}❌ Error al construir la imagen${NC}"
        exit 1
    fi
}

# Levantar contenedor (desarrollo)
up_dev() {
    echo -e "${BLUE}🚀 Levantando contenedor (desarrollo)...${NC}\n"
    docker-compose -f docker-compose.dev.yml up -d
    
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✅ Contenedor levantado exitosamente${NC}"
        echo -e "${YELLOW}📡 API disponible en: http://localhost:8000${NC}"
        echo -e "${YELLOW}📚 Documentación en: http://localhost:8000/docs${NC}"
    else
        echo -e "\n${RED}❌ Error al levantar el contenedor${NC}"
        exit 1
    fi
}

# Levantar contenedor (producción)
up_prod() {
    echo -e "${BLUE}🚀 Levantando contenedor (producción)...${NC}\n"
    docker-compose -f docker-compose.prod.yml up -d
    
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✅ Contenedor en producción levantado${NC}"
        echo -e "${YELLOW}📡 API disponible en: http://localhost:8000${NC}"
    else
        echo -e "\n${RED}❌ Error al levantar el contenedor${NC}"
        exit 1
    fi
}

# Detener contenedor
down_container() {
    echo -e "${BLUE}🛑 Deteniendo contenedor...${NC}\n"
    docker-compose down
    
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✅ Contenedor detenido${NC}"
    fi
}

# Reiniciar contenedor
restart_container() {
    echo -e "${BLUE}🔄 Reiniciando contenedor...${NC}\n"
    docker-compose restart
    
    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✅ Contenedor reiniciado${NC}"
    fi
}

# Ver logs
show_logs() {
    echo -e "${BLUE}📋 Mostrando logs...${NC}\n"
    docker-compose logs -f --tail=100
}

# Abrir shell
open_shell() {
    echo -e "${BLUE}🐚 Abriendo shell en el contenedor...${NC}\n"
    docker-compose exec quicktask-api /bin/bash
}

# Ejecutar tests
run_tests() {
    echo -e "${BLUE}🧪 Ejecutando tests en el contenedor...${NC}\n"
    docker-compose exec quicktask-api pytest -v
}

# Limpiar todo
clean_all() {
    echo -e "${YELLOW}⚠️  Esto eliminará contenedores, imágenes y volúmenes${NC}"
    read -p "¿Estás seguro? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}🧹 Limpiando...${NC}\n"
        docker-compose down -v --rmi all
        echo -e "\n${GREEN}✅ Limpieza completada${NC}"
    else
        echo -e "${YELLOW}❌ Limpieza cancelada${NC}"
    fi
}

# Ver estado
show_status() {
    echo -e "${BLUE}📊 Estado de contenedores:${NC}\n"
    docker-compose ps
    
    echo -e "\n${BLUE}📊 Uso de recursos:${NC}"
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
}

# Main
show_banner
check_docker

case "${1:-help}" in
    build)
        build_image
        ;;
    up)
        up_dev
        ;;
    up-prod)
        up_prod
        ;;
    down)
        down_container
        ;;
    restart)
        restart_container
        ;;
    logs)
        show_logs
        ;;
    shell)
        open_shell
        ;;
    test)
        run_tests
        ;;
    clean)
        clean_all
        ;;
    status)
        show_status
        ;;
    help)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Comando no válido: $1${NC}\n"
        show_help
        exit 1
        ;;
esac

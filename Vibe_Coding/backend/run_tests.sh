#!/bin/bash

# Script para ejecutar tests de QuickTask API
# Uso: ./run_tests.sh [opciones]

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 QuickTask API - Test Runner${NC}\n"

# Verificar si pytest está instalado
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest no está instalado${NC}"
    echo "Instalando dependencias de testing..."
    pip install -r test_requirements.txt
fi

# Función para mostrar ayuda
show_help() {
    echo "Uso: ./run_tests.sh [opción]"
    echo ""
    echo "Opciones:"
    echo "  all          - Ejecutar todos los tests (por defecto)"
    echo "  unit         - Solo tests unitarios (CRUD + schemas)"
    echo "  integration  - Solo tests de integración (API)"
    echo "  coverage     - Ejecutar con reporte de cobertura"
    echo "  fast         - Ejecutar tests sin verbose"
    echo "  help         - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  ./run_tests.sh"
    echo "  ./run_tests.sh unit"
    echo "  ./run_tests.sh coverage"
}

# Procesar argumentos
case "${1:-all}" in
    all)
        echo -e "${GREEN}📋 Ejecutando todos los tests...${NC}\n"
        pytest -v
        ;;
    unit)
        echo -e "${GREEN}🔧 Ejecutando tests unitarios...${NC}\n"
        pytest test_crud.py test_schemas.py -v
        ;;
    integration)
        echo -e "${GREEN}🌐 Ejecutando tests de integración...${NC}\n"
        pytest test_api.py -v
        ;;
    coverage)
        echo -e "${GREEN}📊 Ejecutando con cobertura de código...${NC}\n"
        pytest --cov=. --cov-report=term-missing --cov-report=html
        echo -e "\n${BLUE}📁 Reporte HTML generado en: htmlcov/index.html${NC}"
        ;;
    fast)
        echo -e "${GREEN}⚡ Ejecutando tests (modo rápido)...${NC}\n"
        pytest -q
        ;;
    help)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Opción no válida: $1${NC}\n"
        show_help
        exit 1
        ;;
esac

# Mostrar resultado
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ Tests completados exitosamente${NC}"
else
    echo -e "\n${RED}❌ Algunos tests fallaron${NC}"
    exit 1
fi

# Análisis funcional y técnico — **QuickTask**
*(rol: arquitecto de software — tono analítico, buenas prácticas)*

---

## 1. Resumen funcional
**Qué hace la app:**  
QuickTask es un gestor de tareas personales que permite crear, editar, buscar, filtrar y marcar tareas como completadas. Soporta notificaciones/recordatorios, persistencia local y sincronización entre dispositivos (cuando el usuario se autentica).  

**Cómo interactúan los componentes (alto nivel):**
- **Cliente (móvil / web)**: UI para CRUD de tareas; persiste localmente y muestra/recibe notificaciones; envía/recibe cambios al backend cuando hay conectividad.
- **API (Backend)**: expone endpoints REST (o GraphQL) para CRUD de tareas, autenticación, sincronización, gestión de notificaciones y configuración del usuario.
- **Base de datos**: almacena usuarios, tareas, metadatos de sincronización y registros de notificaciones.
- **Servicio de sincronización / cola**: maneja reconciliación y entrega eventual (opcional).
- **Proveedor de notificaciones push**: FCM / APNs para notificaciones remotas; local notifications para recordatorios sin conexión.
- **Almacenamiento local en cliente**: (SQLite / Realm / IndexedDB) para experiencia offline y sincronización diferida.

---

## 2. Análisis de módulos / componentes

### Frontend (cliente)
- **Presentación / UI:** pantallas de lista, detalle, creación/edición, búsqueda, filtros, configuración.
- **Persistencia local:** base de datos local (SQLite / Realm) + cache en memoria.
- **Capa de sincronización:** colas locales, manejo de retries, backoff exponencial.
- **Notificaciones:** integración con Notificaciones locales y FCM/APNs.
- **Autenticación y sesión:** token JWT o tokens de largo plazo + refresh tokens.
- **Estado de la app:** manejo del estado (Zustand/Redux/Context).

### Backend / API
- **Controladores / Endpoints** para tareas, usuarios, sesiones, sync, settings.
- **Lógica de negocio**: validaciones, reglas de sincronización, generación de notificaciones programadas.
- **Persistencia:** capa de acceso a datos (repositorios/ORM).
- **Colas / Jobs:** ejecución de tareas programadas (recordatorios), reintentos, limpieza.
- **Observabilidad:** logging, métricas, trazas (opcional: Zipkin/Jaeger).

### Base de datos
- **Principal (producción):** PostgreSQL (relacional) o DynamoDB (NoSQL) según requisitos de consultas y escalado.
- **Cache (opcional):** Redis para session store, rate limiting, colas ligeras.
- **Esquema mínimo:** users, tasks, task_versions/audit, device_sessions, notification_jobs.

### Infraestructura / DevOps
- **Contenerización:** Docker.
- **Orquestación / Hosting:** Azure Web App / Azure Container Instances / Kubernetes / serverless (dependiendo del presupuesto).
- **CI/CD:** pipelines para pruebas, lint, builds y despliegue.
- **Backups / Monitoring:** backup DB, health checks, alertas.

---

## 3. Tecnologías recomendadas (stack propuesto)

> **Elección principal (recomendada por equilibrio entre rapidez, ecosistema y coherencia con historial del usuario):**
- **Frontend móvil:** React Native (Expo)
- **Frontend web (opcional PWA):** React + Vite / Next.js
- **Backend:** NestJS (Node.js + TypeScript)
- **ORM / DB access:** TypeORM o Prisma con PostgreSQL
- **Autenticación:** JWT + refresh tokens
- **Push Notifications:** Firebase Cloud Messaging (FCM) / APNs
- **Persistencia local:** SQLite (react-native-sqlite-storage) o Realm
- **Queue / Jobs:** BullMQ (Redis)
- **Observabilidad:** Sentry, Prometheus + Grafana, Zipkin/Jaeger
- **CI/CD / Infra:** Docker, GitHub Actions / Azure DevOps, Azure App Services

> **Alternativas válidas y cuándo elegirlas:**
- **FastAPI (Python)** si el equipo prefiere Python.
- **Flutter** si se prioriza UI rica y consistencia visual.
- **MongoDB** si los modelos son altamente flexibles.

---

## 4. Riesgos técnicos y mitigaciones

1. **Conflictos de sincronización:**  
   *Mitigación:* usar timestamps, versionado y política LWW (last-write-wins).
2. **Pérdida de datos offline:**  
   *Mitigación:* persistencia ACID local, colas y retries.
3. **Complejidad de notificaciones push:**  
   *Mitigación:* abstraer proveedor y usar FCM.
4. **Seguridad insuficiente:**  
   *Mitigación:* bcrypt/argon2, HTTPS, rate limiting.
5. **Escalabilidad:**  
   *Mitigación:* diseño stateless, Redis, read replicas.
6. **Fragmentación UI:**  
   *Mitigación:* componentes compartidos, testing E2E.
7. **Deuda técnica:**  
   *Mitigación:* CI/CD con pruebas y code reviews.

---

## 5. Mapa general de dependencias

```
[Cliente Móvil (React Native)]  <--->  [API Gateway / Backend (NestJS)]
      |  ^                                   |    ^
      |  |                                   |    |
      v  |                                   v    |
[Local DB (SQLite / Realm)]            [PostgreSQL DB]  <--- backups
      |                                        ^
      v                                        |
[Sync queue local]  --(sync)->  [Job Queue (Redis/Bull)] --(jobs)-> [Worker(s)]
                                                |
                                                v
                                        [Push Provider: FCM / APNs]
                                                |
                                                v
                                           [Delivery to devices]
```

---

## 6. Justificación técnica

### React Native vs Flutter
- RN permite reutilizar conocimientos JS/TS y usar Expo para prototipado rápido.
- Flutter ofrece mejor UI consistente pero mayor curva de aprendizaje.
- **Decisión:** React Native por coherencia tecnológica y velocidad.

### NestJS vs FastAPI
- NestJS ofrece DI, estructura modular y coherencia con TS/React.
- FastAPI destaca en rendimiento y sintaxis, pero rompe coherencia JS/TS.
- **Decisión:** NestJS por alinearse con la pila TypeScript.

### PostgreSQL vs MongoDB
- PostgreSQL favorece consultas relacionales y consistencia.
- MongoDB útil para esquemas flexibles.
- **Decisión:** PostgreSQL por estabilidad y soporte a filtros transaccionales.

### SQLite / Realm
- SQLite ligero y soportado ampliamente.
- Realm aporta sincronización y reactividad.
- **Decisión:** SQLite para MVP, Realm opcional en versiones avanzadas.

---

## Recomendaciones operativas

- Iniciar con MVP: React Native + NestJS + Postgres + FCM.
- Definir contrato de sincronización (timestamps, payload).
- Establecer CI/CD con pruebas unitarias y E2E.
- Documentar API con OpenAPI/Swagger.

---

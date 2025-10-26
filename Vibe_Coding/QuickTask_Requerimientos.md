# 📋 Especificación de Requerimientos del Sistema: **QuickTask**

## 1. Descripción general del sistema

**QuickTask** es una aplicación de gestión de tareas personales diseñada para ayudar a los usuarios a **crear, organizar, editar y completar tareas de manera rápida y sencilla**.  
El sistema busca ofrecer una experiencia fluida, accesible y multiplataforma, enfocada en la **simplicidad y productividad personal**.

## 2. Actores principales

| Actor | Descripción |
|-------|--------------|
| **Usuario** | Persona que utiliza la aplicación para gestionar sus tareas. Puede crear, editar, eliminar y marcar tareas como completadas. |
| **Sistema** | Componente que gestiona la lógica interna de QuickTask, incluyendo almacenamiento, notificaciones y sincronización de datos. |

---

## 3. Requerimientos funcionales

### 3.1 Gestión de tareas
1. El sistema debe permitir al usuario **crear una nueva tarea**, especificando al menos un título.  
2. El sistema debe permitir **añadir una descripción opcional** y una **fecha de vencimiento** a cada tarea.  
3. El sistema debe permitir **editar los datos** de una tarea existente.  
4. El sistema debe permitir **eliminar una tarea** seleccionada por el usuario.  
5. El sistema debe permitir **marcar una tarea como completada o pendiente**.  
6. El sistema debe mostrar **una lista de todas las tareas**, separadas por estado (pendientes/completadas).  
7. El sistema debe permitir **filtrar tareas** por fecha de vencimiento o estado.  
8. El sistema debe permitir **buscar tareas** por texto (título o descripción).  

### 3.2 Notificaciones y recordatorios
9. El sistema debe permitir que el usuario **reciba recordatorios** para las tareas con fecha de vencimiento próxima.  
10. El usuario debe poder **activar o desactivar las notificaciones** en la configuración de la aplicación.

### 3.3 Persistencia de datos
11. El sistema debe **guardar automáticamente las tareas** en el almacenamiento local del dispositivo o en la nube.  
12. El sistema debe permitir **sincronización de tareas entre dispositivos** si el usuario inicia sesión con una cuenta.

### 3.4 Autenticación (opcional)
13. El sistema debe permitir que el usuario **cree una cuenta** (correo y contraseña).  
14. El usuario debe poder **iniciar y cerrar sesión** en la aplicación.  
15. El sistema debe **mantener la sesión activa** hasta que el usuario decida cerrarla.

---

## 4. Requerimientos no funcionales

| Categoría | Requerimiento |
|------------|----------------|
| **Rendimiento** | El sistema debe cargar la lista de tareas en menos de 2 segundos para un usuario con hasta 500 tareas. |
| **Usabilidad** | La interfaz debe ser intuitiva, con íconos claros para crear, editar y marcar tareas. |
| **Disponibilidad** | El sistema debe estar disponible al menos el 99% del tiempo en condiciones normales. |
| **Compatibilidad** | La aplicación debe ser compatible con navegadores modernos y sistemas operativos móviles Android/iOS. |
| **Seguridad** | Las contraseñas deben almacenarse cifradas utilizando un algoritmo estándar (p. ej., bcrypt). |
| **Escalabilidad** | El sistema debe permitir integrar futuras funciones como listas compartidas o categorías sin rediseñar la arquitectura. |
| **Mantenibilidad** | El código debe estar documentado y seguir una estructura modular. |

---

## 5. Criterios de aceptación

### Función: Crear tarea
- Dado que el usuario está en la pantalla principal,  
  cuando presione el botón “Agregar tarea” y escriba un título,  
  entonces el sistema debe guardar la nueva tarea y mostrarla en la lista de tareas pendientes.

### Función: Marcar tarea como completada
- Dado que el usuario tiene una tarea pendiente,  
  cuando toque el ícono de completado,  
  entonces la tarea debe cambiar su estado a “completada” y aparecer en la sección correspondiente.

### Función: Editar tarea
- Dado que el usuario selecciona una tarea existente,  
  cuando edite su título o descripción y guarde los cambios,  
  entonces el sistema debe actualizar la tarea sin duplicarla y reflejar el cambio en la lista.

---

## 6. Suposiciones y restricciones

### Suposiciones
- Los usuarios tienen acceso a un dispositivo con conexión a internet.  
- Los usuarios gestionan sus propias tareas (no hay colaboración entre cuentas en esta versión).  
- Se prioriza la experiencia móvil, aunque puede existir versión web.

### Restricciones
- El desarrollo inicial se centrará en **una única cuenta por usuario**.  
- El sistema no integrará recordatorios por correo electrónico en la primera versión.  
- La aplicación debe desarrollarse con tecnologías multiplataforma (por ejemplo, Flutter o React Native).

---

## 7. Riesgos o ambigüedades a aclarar

1. ¿Las tareas deben tener subtareas o etiquetas?  
2. ¿Se requiere sincronización en tiempo real entre dispositivos?  
3. ¿Se implementará un modo sin conexión (offline)?  
4. ¿Habrá integración con servicios externos (como Google Calendar)?  
5. ¿Qué nivel de personalización se espera en las notificaciones (hora, frecuencia, tipo)?  

@startuml
actor Usuario as User

rectangle QuickTask {
    usecase "Registrar cuenta" as UC1
    usecase "Iniciar sesión" as UC2
    usecase "Crear tarea" as UC3
    usecase "Editar tarea" as UC4
    usecase "Eliminar tarea" as UC5
    usecase "Marcar tarea como completada" as UC6
    usecase "Ver lista de tareas" as UC7
}

User --> UC1
User --> UC2
User --> UC3
User --> UC4
User --> UC5
User --> UC6
User --> UC7
@enduml

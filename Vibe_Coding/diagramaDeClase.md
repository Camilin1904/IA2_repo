@startuml
class User {
    - id: int
    - name: string
    - email: string
    - password: string
    + register(): void
    + login(): boolean
}

class Task {
    - id: int
    - title: string
    - description: string
    - dueDate: Date
    - completed: boolean
    + markCompleted(): void
    + update(title: string, description: string, dueDate: Date): void
}

class TaskService {
    + createTask(userId: int, task: Task): Task
    + editTask(taskId: int, task: Task): Task
    + deleteTask(taskId: int): void
    + listTasks(userId: int): List<Task>
}

class AuthService {
    + register(user: User): User
    + login(email: string, password: string): boolean
}

User "1" --> "0..*" Task : "posee"
TaskService --> Task
AuthService --> User
@enduml

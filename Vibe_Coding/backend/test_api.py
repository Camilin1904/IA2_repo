"""
Tests de integración para los endpoints de la API.
Prueban el comportamiento completo de HTTP requests/responses.
"""
import pytest
from fastapi.testclient import TestClient


class TestRootEndpoint:
    """Tests para el endpoint raíz"""
    
    def test_root_endpoint(self, client: TestClient):
        """Verificar que el endpoint raíz responde correctamente"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "QuickTask" in data["message"]
    
    def test_health_check(self, client: TestClient):
        """Verificar endpoint de salud"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestCreateTaskEndpoint:
    """Tests para POST /tasks"""
    
    def test_create_task_success(self, client: TestClient):
        """Crear tarea exitosamente con todos los campos"""
        task_data = {
            "title": "Nueva tarea",
            "description": "Descripción de prueba",
            "due_date": "2025-10-30T10:00:00",
            "completed": False
        }
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Nueva tarea"
        assert data["description"] == "Descripción de prueba"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
    
    def test_create_task_minimal(self, client: TestClient):
        """Crear tarea solo con título"""
        task_data = {"title": "Tarea mínima"}
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Tarea mínima"
        assert data["completed"] is False
    
    def test_create_task_without_title(self, client: TestClient):
        """Intentar crear tarea sin título (debe fallar)"""
        task_data = {"description": "Sin título"}
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_create_task_empty_title(self, client: TestClient):
        """Intentar crear tarea con título vacío (debe fallar)"""
        task_data = {"title": ""}
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 422
    
    def test_create_task_invalid_date_format(self, client: TestClient):
        """Intentar crear tarea con fecha inválida"""
        task_data = {
            "title": "Tarea con fecha inválida",
            "due_date": "fecha-invalida"
        }
        
        response = client.post("/tasks", json=task_data)
        
        assert response.status_code == 422


class TestListTasksEndpoint:
    """Tests para GET /tasks"""
    
    def test_list_tasks_empty(self, client: TestClient):
        """Listar tareas cuando no hay ninguna"""
        response = client.get("/tasks")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["tasks"] == []
    
    def test_list_tasks_with_data(self, client: TestClient):
        """Listar tareas cuando existen varias"""
        # Crear 3 tareas
        for i in range(3):
            client.post("/tasks", json={"title": f"Tarea {i+1}"})
        
        response = client.get("/tasks")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["tasks"]) == 3
    
    def test_list_tasks_pagination(self, client: TestClient):
        """Probar paginación en listado"""
        # Crear 5 tareas
        for i in range(5):
            client.post("/tasks", json={"title": f"Tarea {i+1}"})
        
        # Obtener primeras 2
        response = client.get("/tasks?skip=0&limit=2")
        data = response.json()
        assert len(data["tasks"]) == 2
        assert data["total"] == 5
        
        # Obtener siguientes 2
        response = client.get("/tasks?skip=2&limit=2")
        data = response.json()
        assert len(data["tasks"]) == 2
    
    def test_filter_by_completed_status(self, client: TestClient):
        """Filtrar tareas por estado completado"""
        # Crear tareas con diferentes estados
        client.post("/tasks", json={"title": "Pendiente 1", "completed": False})
        client.post("/tasks", json={"title": "Completada 1", "completed": True})
        client.post("/tasks", json={"title": "Pendiente 2", "completed": False})
        
        # Filtrar pendientes
        response = client.get("/tasks?completed=false")
        data = response.json()
        assert data["total"] == 2
        assert all(not task["completed"] for task in data["tasks"])
        
        # Filtrar completadas
        response = client.get("/tasks?completed=true")
        data = response.json()
        assert data["total"] == 1
        assert all(task["completed"] for task in data["tasks"])
    
    def test_search_tasks(self, client: TestClient):
        """Buscar tareas por texto"""
        client.post("/tasks", json={"title": "Comprar víveres"})
        client.post("/tasks", json={"title": "Hacer ejercicio"})
        client.post("/tasks", json={"title": "Comprar medicamentos"})
        
        response = client.get("/tasks?search=comprar")
        data = response.json()
        
        assert data["total"] == 2
        assert all("comprar" in task["title"].lower() for task in data["tasks"])


class TestGetTaskByIdEndpoint:
    """Tests para GET /tasks/{id}"""
    
    def test_get_task_success(self, client: TestClient, create_sample_task):
        """Obtener tarea existente por ID"""
        task_id = create_sample_task["id"]
        
        response = client.get(f"/tasks/{task_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == create_sample_task["title"]
    
    def test_get_nonexistent_task(self, client: TestClient):
        """Intentar obtener tarea que no existe"""
        response = client.get("/tasks/9999")
        
        assert response.status_code == 404
        assert "no encontrada" in response.json()["detail"].lower()


class TestUpdateTaskEndpoint:
    """Tests para PUT y PATCH /tasks/{id}"""
    
    def test_update_task_full(self, client: TestClient, create_sample_task):
        """Actualizar tarea completa con PUT"""
        task_id = create_sample_task["id"]
        
        update_data = {
            "title": "Título actualizado",
            "description": "Nueva descripción",
            "due_date": "2025-11-01T15:00:00",
            "completed": True
        }
        
        response = client.put(f"/tasks/{task_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Título actualizado"
        assert data["description"] == "Nueva descripción"
        assert data["completed"] is True
    
    def test_update_task_partial(self, client: TestClient, create_sample_task):
        """Actualizar parcialmente con PATCH"""
        task_id = create_sample_task["id"]
        
        # Solo actualizar el estado
        update_data = {"completed": True}
        
        response = client.patch(f"/tasks/{task_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True
        assert data["title"] == create_sample_task["title"]  # No cambió
    
    def test_update_task_title_only(self, client: TestClient, create_sample_task):
        """Actualizar solo el título"""
        task_id = create_sample_task["id"]
        
        response = client.patch(f"/tasks/{task_id}", json={"title": "Nuevo título"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Nuevo título"
    
    def test_update_nonexistent_task(self, client: TestClient):
        """Intentar actualizar tarea que no existe"""
        update_data = {"title": "No existe"}
        
        response = client.put("/tasks/9999", json=update_data)
        
        assert response.status_code == 404
    
    def test_mark_task_as_completed(self, client: TestClient, create_sample_task):
        """Caso de uso: marcar tarea como completada"""
        task_id = create_sample_task["id"]
        
        # Verificar que está pendiente
        assert create_sample_task["completed"] is False
        
        # Marcar como completada
        response = client.patch(f"/tasks/{task_id}", json={"completed": True})
        
        assert response.status_code == 200
        assert response.json()["completed"] is True


class TestDeleteTaskEndpoint:
    """Tests para DELETE /tasks/{id}"""
    
    def test_delete_task_success(self, client: TestClient, create_sample_task):
        """Eliminar tarea existente"""
        task_id = create_sample_task["id"]
        
        response = client.delete(f"/tasks/{task_id}")
        
        assert response.status_code == 204
        
        # Verificar que ya no existe
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_task(self, client: TestClient):
        """Intentar eliminar tarea que no existe"""
        response = client.delete("/tasks/9999")
        
        assert response.status_code == 404
    
    def test_delete_and_list(self, client: TestClient):
        """Verificar que la lista se actualiza después de eliminar"""
        # Crear 3 tareas
        task1 = client.post("/tasks", json={"title": "Tarea 1"}).json()
        client.post("/tasks", json={"title": "Tarea 2"})
        client.post("/tasks", json={"title": "Tarea 3"})
        
        # Verificar que hay 3
        response = client.get("/tasks")
        assert response.json()["total"] == 3
        
        # Eliminar una
        client.delete(f"/tasks/{task1['id']}")
        
        # Verificar que quedan 2
        response = client.get("/tasks")
        assert response.json()["total"] == 2


class TestCompleteWorkflow:
    """Tests de flujo completo (end-to-end)"""
    
    def test_full_task_lifecycle(self, client: TestClient):
        """Probar ciclo de vida completo de una tarea"""
        # 1. Crear tarea
        create_response = client.post("/tasks", json={
            "title": "Estudiar pytest",
            "description": "Aprender testing en Python"
        })
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]
        
        # 2. Verificar que aparece en la lista
        list_response = client.get("/tasks")
        assert list_response.json()["total"] == 1
        
        # 3. Obtener por ID
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 200
        
        # 4. Actualizar descripción
        patch_response = client.patch(f"/tasks/{task_id}", json={
            "description": "Completar tutorial de pytest"
        })
        assert patch_response.json()["description"] == "Completar tutorial de pytest"
        
        # 5. Marcar como completada
        complete_response = client.patch(f"/tasks/{task_id}", json={"completed": True})
        assert complete_response.json()["completed"] is True
        
        # 6. Verificar en lista de completadas
        completed_list = client.get("/tasks?completed=true")
        assert completed_list.json()["total"] == 1
        
        # 7. Eliminar
        delete_response = client.delete(f"/tasks/{task_id}")
        assert delete_response.status_code == 204
        
        # 8. Verificar que no existe
        final_get = client.get(f"/tasks/{task_id}")
        assert final_get.status_code == 404
    
    def test_multiple_users_scenario(self, client: TestClient):
        """Simular múltiples tareas de diferentes usuarios"""
        # Usuario crea varias tareas
        tasks = []
        for i in range(5):
            response = client.post("/tasks", json={
                "title": f"Tarea del día {i+1}",
                "completed": i % 2 == 0  # Alternar completadas
            })
            tasks.append(response.json())
        
        # Listar todas
        all_tasks = client.get("/tasks").json()
        assert all_tasks["total"] == 5
        
        # Filtrar pendientes
        pending = client.get("/tasks?completed=false").json()
        assert pending["total"] == 2
        
        # Filtrar completadas
        completed = client.get("/tasks?completed=true").json()
        assert completed["total"] == 3
        
        # Buscar específica
        search_result = client.get("/tasks?search=día 3").json()
        assert search_result["total"] == 1

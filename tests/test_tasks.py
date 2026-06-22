from fastapi import status


# ─── FIXTURES DE DADOS ────────────────────────────────────────────

def create_task_payload(
    title: str = "Estudar FastAPI",
    description: str = "Estudar por 2 horas",
    priority: str = "medium",
) -> dict:
    return {
        "title": title,
        "description": description,
        "priority": priority,
    }


def create_task_in_db(client, **kwargs) -> dict:
    """Helper — cria uma tarefa e retorna o JSON."""
    payload = create_task_payload(**kwargs)
    response = client.post("/tasks/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    return response.json()


# ─── TESTES DE CREATE ─────────────────────────────────────────────

class TestCreateTask:

    def test_create_task_success(self, client):
        """Deve criar uma tarefa com sucesso."""
        payload = create_task_payload()
        response = client.post("/tasks/", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["description"] == payload["description"]
        assert data["priority"] == payload["priority"]
        assert data["completed"] == False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_without_description(self, client):
        """Deve criar tarefa sem descrição."""
        payload = {"title": "Tarefa sem descrição"}
        response = client.post("/tasks/", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["description"] is None

    def test_create_task_with_high_priority(self, client):
        """Deve criar tarefa com prioridade alta."""
        payload = create_task_payload(priority="high")
        response = client.post("/tasks/", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["priority"] == "high"

    def test_create_task_empty_title_fails(self, client):
        """Deve falhar com título vazio."""
        payload = {"title": ""}
        response = client.post("/tasks/", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_task_invalid_priority_fails(self, client):
        """Deve falhar com prioridade inválida."""
        payload = create_task_payload(priority="urgente")
        response = client.post("/tasks/", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_task_missing_title_fails(self, client):
        """Deve falhar sem título."""
        response = client.post("/tasks/", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ─── TESTES DE READ ───────────────────────────────────────────────

class TestReadTask:

    def test_list_tasks_empty(self, client):
        """Deve retornar lista vazia."""
        response = client.get("/tasks/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_tasks_with_data(self, client):
        """Deve retornar lista com tarefas criadas."""
        create_task_in_db(client, title="Tarefa 1")
        create_task_in_db(client, title="Tarefa 2")

        response = client.get("/tasks/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

    def test_list_tasks_pagination(self, client):
        """Deve respeitar skip e limit."""
        for i in range(5):
            create_task_in_db(client, title=f"Tarefa {i}")

        response = client.get("/tasks/?skip=2&limit=2")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

    def test_list_tasks_limit_above_max_fails(self, client):
        """Deve rejeitar limit acima de 100 (proteção contra DoS)."""
        response = client.get("/tasks/?limit=101")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_list_tasks_negative_skip_fails(self, client):
        """Deve rejeitar skip negativo."""
        response = client.get("/tasks/?skip=-1")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_list_tasks_filter_by_completed(self, client):
        """Deve filtrar tarefas por status de conclusão."""
        t = create_task_in_db(client, title="Pendente")
        client.put(f"/tasks/{t['id']}", json={"completed": True})
        create_task_in_db(client, title="Concluída")

        response = client.get("/tasks/?completed=false")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(not t["completed"] for t in data)

    def test_list_tasks_filter_by_priority(self, client):
        """Deve filtrar tarefas por prioridade."""
        create_task_in_db(client, title="Alta", priority="high")
        create_task_in_db(client, title="Baixa", priority="low")

        response = client.get("/tasks/?priority=high")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["priority"] == "high"

    def test_get_task_by_id_success(self, client):
        """Deve retornar tarefa pelo ID."""
        created = create_task_in_db(client)
        task_id = created["id"]

        response = client.get(f"/tasks/{task_id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == task_id

    def test_get_task_not_found(self, client):
        """Deve retornar 404 para ID inexistente."""
        response = client.get("/tasks/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["error"]["code"] == "NOT_FOUND"


# ─── TESTES DE UPDATE ─────────────────────────────────────────────

class TestUpdateTask:

    def test_update_task_title(self, client):
        """Deve atualizar o título da tarefa."""
        created = create_task_in_db(client)
        task_id = created["id"]

        response = client.put(
            f"/tasks/{task_id}",
            json={"title": "Título atualizado"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Título atualizado"

    def test_update_task_completed(self, client):
        """Deve marcar tarefa como concluída."""
        created = create_task_in_db(client)
        task_id = created["id"]

        response = client.put(
            f"/tasks/{task_id}",
            json={"completed": True},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["completed"] == True

    def test_update_task_partial(self, client):
        """Deve atualizar apenas os campos enviados."""
        created = create_task_in_db(client, priority="low")
        task_id = created["id"]

        response = client.put(
            f"/tasks/{task_id}",
            json={"priority": "high"},
        )

        data = response.json()
        assert data["priority"] == "high"
        assert data["title"] == created["title"]

    def test_update_task_not_found(self, client):
        """Deve retornar 404 ao atualizar ID inexistente."""
        response = client.put(
            "/tasks/999",
            json={"title": "Teste"},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


# ─── TESTES DE DELETE ─────────────────────────────────────────────

class TestDeleteTask:

    def test_delete_task_success(self, client):
        """Deve deletar tarefa com sucesso."""
        created = create_task_in_db(client)
        task_id = created["id"]

        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Confirma que foi removida
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task_not_found(self, client):
        """Deve retornar 404 ao deletar ID inexistente."""
        response = client.delete("/tasks/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND


# ─── TESTES DE HEALTH ─────────────────────────────────────────────

class TestHealthCheck:

    def test_root_returns_welcome(self, client):
        """Deve retornar mensagem de boas-vindas."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()

    def test_health_endpoint(self, client):
        """Deve retornar status ok."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "ok"
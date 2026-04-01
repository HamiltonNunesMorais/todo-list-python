import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"

def test_tentativa_xss_no_titulo():
    """Valida se a API aceita tags de script (risco de XSS)"""
    payload = {"title": "<script>alert('hack')</script>", "description": "XSS", "completed": False}
    response = requests.post(f"{BASE_URL}/todos/", json=payload)
    
    assert response.status_code == 200
    print(f"\n[LOG] Payload de script enviado. O QA deve validar se o Front-end vai renderizar isso!")
def test_listar_todos_vazio():
    """Valida se a lista inicial de tarefas está acessível"""
    response = requests.get(f"{BASE_URL}/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_criar_tarefa():
    """Valida a criação de uma nova tarefa (POST)"""
    payload = {
        "title": "Estudar para Bellinati",
        "description": "Praticar testes de API com Python",
        "completed": False
    }
    response = requests.post(f"{BASE_URL}/todos/", json=payload)
    
    assert response.status_code == 200 # FastAPI costuma retornar 200 ou 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data # Garante que o banco gerou um ID

def test_deletar_tarefa():
    """Cria uma tarefa e deleta em seguida para validar o DELETE"""
    # 1. Cria
    payload = {"title": "Tarefa para Deletar", "description": "Teste", "completed": False}
    post_res = requests.post(f"{BASE_URL}/todos/", json=payload)
    todo_id = post_res.json()["id"]

    # 2. Deleta
    del_res = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    assert del_res.status_code == 200

def test_criar_tarefa_sem_titulo_deve_falhar():
    """Valida se a API retorna erro 422 ao enviar dados incompletos"""
    payload = {"description": "Sem titulo"} # Faltando o campo 'title'
    response = requests.post(f"{BASE_URL}/todos/", json=payload)
    
    assert response.status_code == 422  # Erro de validação do FastAPI/Pydantic
    print("\n[LOG] API barrou corretamente a criação sem título!")

def test_buscar_tarefa_inexistente_deve_retornar_404():
    """Valida se a API retorna 404 ao buscar um ID que não está no banco"""
    id_inexistente = 9999
    response = requests.get(f"{BASE_URL}/todos/{id_inexistente}")
    
    assert response.status_code == 404
    
    # Validar se a mensagem de erro no JSON faz sentido
    data = response.json()
    assert "detail" in data  # FastAPI costuma usar a chave 'detail' para erros
    print(f"\n[LOG] API retornou 404 corretamente para o ID: {id_inexistente}")
    print(f"[LOG] Mensagem de erro: {data['detail']}")

def test_atualizar_status_tarefa():
    """Valida se a alteração de 'completed' de False para True persiste no banco"""
    # 1. Cria uma tarefa pendente
    payload = {"title": "Tarefa para Atualizar", "description": "Teste", "completed": False}
    post_res = requests.post(f"{BASE_URL}/todos/", json=payload)
    todo_id = post_res.json()["id"]

    # 2. Atualiza para concluída (True)
    update_payload = {"title": "Tarefa para Atualizar", "description": "Teste", "completed": True}
    put_res = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_payload)
    
    assert put_res.status_code == 200
    assert put_res.json()["completed"] is True
    print(f"\n[LOG] Tarefa {todo_id} atualizada para Concluída!")

def test_validar_incremento_na_lista():
    """Garante que após um POST, o tamanho da lista total aumenta em 1"""
    # Pega o tamanho antes
    inicial = len(requests.get(f"{BASE_URL}/todos/").json())

    # Cria nova
    requests.post(f"{BASE_URL}/todos/", json={"title": "Nova", "description": "X", "completed": False})

    # Pega o tamanho depois
    final = len(requests.get(f"{BASE_URL}/todos/").json())

    assert final == inicial + 1
    print(f"\n[LOG] Incremento de lista validado: {inicial} -> {final}")

def test_enviar_tipo_dado_invalido_deve_falhar():
    """Valida se a API barra quando enviamos um número no campo de título (string)"""
    payload = {"title": 12345, "description": "Tipo Errado", "completed": False}
    response = requests.post(f"{BASE_URL}/todos/", json=payload)
    
    # Se o FastAPI estiver bem configurado com Pydantic, ele deve retornar 422
    assert response.status_code == 422
    print("\n[LOG] API validou corretamente que o título deve ser string!")
import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"

def test_tentativa_xss_no_titulo():
    """Valida se a API aceita tags de script (risco de XSS)"""
    payload = {"title": "<script>alert('hack')</script>", "description": "XSS", "completed": False}
    response = requests.post(f"{BASE_URL}/todos/", json=payload)
    
    assert response.status_code == 200
    print(f"\n[LOG] Payload de script enviado. O QA deve validar se o Front-end vai renderizar isso!")
    

def test_tentativa_sql_injection_no_titulo():
    """Tenta injetar um comando SQL no campo de título para ver a reação da API"""
    
    # O payload contém uma aspa simples e um comando de comentário SQL
    # Isso tenta fechar a query original e ignorar o resto
    payload = {
        "title": "Tarefa'); DROP TABLE todos;--", 
        "description": "Tentativa de SQLi",
        "completed": False
    }
    
    response = requests.post(f"{BASE_URL}/todos/", json=payload)
    
    # Se a API aceitar isso como um texto comum (200/201), ela é vulnerável a nível de dados.
    # Se ela barrar ou sanitizar, ela é segura.
    print(f"\n[LOG] Status da API para tentativa de SQLi: {response.status_code}")
    
    # Em um sistema seguro, o input deveria ser sanitizado antes de chegar no banco.
    assert response.status_code in [200, 201] # Aqui validamos que a API não 'morreu' com o caractere especial
    print("[LOG] A API processou o texto, mas o QA deve validar se o banco executou o comando!")
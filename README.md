# Todo List Python

API de lista de tarefas construída em **Python** com **FastAPI**.

---

## Como iniciar a aplicação

### Criar ambiente virtual
```bash
python -m venv venv
```
### Ativar ambiente virtual
No Windows:

```bash
venv\Scripts\activate.bat
```
### Instalar dependências
```bash
pip install -r requirements.txt
```
### Executar servidor
```bash
uvicorn main:app --reload
```
### Documentação da API Swagger
```bash
http://127.0.0.1:8000/docs
```

### Para rodar os testes automatizados
```bash
pytest tests/test_todos.py -v -s
pytest tests/test_security.py -v -s

```
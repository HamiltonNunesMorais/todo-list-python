# todo-list-python

iniciar a aplicacao 

python -m venv venv

venv\Scripts\activate.bat

pip install -r requirements.txt

uvicorn main:app --reload


Swagger: http://127.0.0.1:8000/docs

pytest tests/test_todos.py -v -s
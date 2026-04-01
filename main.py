from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.database import Base, engine
from app.routers import todos

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todos.router)

# Handler para erros de validação
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"message": "Erro de validação", "errors": exc.errors()},
    )

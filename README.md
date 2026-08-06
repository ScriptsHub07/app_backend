Backend FastAPI para Jarvis Mobile

Esse backend fornece APIs mínimas para:
- memória de longo prazo (endpoints simples)
- OAuth (esqueleto para Google Calendar / Gmail)

Como rodar (local):

1. Crie um virtualenv e instale dependências:

   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt

2. Execute o servidor:

   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Arquivos importantes:
- app/main.py - instância do FastAPI
- app/routers/memory.py - endpoints de memória
- app/routers/auth.py - esqueleto de OAuth

Deploy no Render: criar um serviço web apontando para este repositório, usar Dockerfile ou comando de start com `uvicorn`.

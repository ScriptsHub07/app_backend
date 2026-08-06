Deploy no Render (passo a passo)

Pré-requisitos:
- Conta no Render (https://render.com)
- Repositório Git com este projeto (ou use GitHub/GitLab/Bitbucket)

1) Conectar repositório
- No painel do Render, clique em "New" → "Web Service".
- Conecte seu repo (GitHub/GitLab/Bitbucket) e selecione o diretório `mobile_backend` ou o repositório inteiro.

2) Criar banco de dados gerenciado
- No painel do Render, clique em "New" → "Postgres Database".
- Escolha um nome (ex: `jarvis-db`) e o plano desejado.
- Após criado, copie a connection string (ex: `postgres://user:pass@host:5432/dbname`).

3) Criar o Web Service
- Ao criar o Web Service, escolha `Docker` como environment (o repo já tem `Dockerfile`).
- Em `Environment` → `Environment Variables`, adicione as variáveis:
  - `DATABASE_URL` = <connection-string do banco>
  - `GOOGLE_CLIENT_ID` = <seu client id>
  - `GOOGLE_CLIENT_SECRET` = <seu client secret>
  - `GOOGLE_REDIRECT_URI` = https://<your-service>.onrender.com/auth/callback

4) Ajustar redirect URI no Google Cloud
- No console do Google Cloud (APIs & Credentials), adicione a `GOOGLE_REDIRECT_URI` fornecida pelo Render nas credenciais OAuth.

5) Deploy
- Render builda e deploya automaticamente quando o serviço for criado e quando você fizer push no repositório.

6) Testar
- Acesse `https://<your-service>.onrender.com/` e verifique resposta `{"status":"ok"}`.
- Teste endpoints: `/memory/`, `/auth/login` e `/google/create_event`.

Notas e dicas
- Use `render.yaml` (modelo neste diretório) para infra como código, ou configure via dashboard.
- Habilite backups e SSL no banco via painel do Render.
- Para produção, configure migrations com Alembic e não use SQLite.

SAPT - API de Análise de Transparência
Uma API em FastAPI que executa scripts de web scraping e é protegida por autenticação de usuário via token JWT, com persistência em banco de dados MySQL.

Pré-requisitos
Python 3.10+

Um servidor MySQL rodando localmente

Como Rodar o Projeto

Instale as dependências:
    pip install -r requirements.txt

Configure suas variáveis de ambiente:

Copie o arquivo de exemplo .env.example para um novo arquivo chamado .env.

# No Windows (usando PowerShell):
copy .env.example .env
# No macOS/Linux:
cp .env.example .env

Abra o arquivo .env e preencha os valores que estão em branco (como JWT_SECRET_KEY e DB_PASSWORD) com suas próprias configurações locais.

Crie o banco de dados no seu MySQL:
-Conecte-se ao seu MySQL e execute: CREATE DATABASE sapt_db;

Inicie a API:
->    uvicorn main:app --reload

A API estará rodando em http://127.0.0.1:8000.

Crie o primeiro usuário:

Abra um novo terminal (com o ambiente virtual ativado) e execute o script de criação de usuário:
->    python create_first_user.py

Siga as instruções para criar seu usuário administrador.

Agora você pode acessar a documentação interativa em http://127.0.0.1:8000/docs para fazer login e testar os endpoints.
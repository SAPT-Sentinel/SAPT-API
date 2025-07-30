# SAPT - API de Análise de Transparência

## 📦 Guia de Instalação e Execução

Siga os passos abaixo para configurar e rodar o projeto no seu ambiente local.

---

### ✅ Pré-requisitos

- Python 3.10 ou superior  
- Um servidor **MySQL** instalado e rodando na sua máquina

---

### ⚙️ Configuração do Ambiente

1. Crie e ative um ambiente virtual (altamente recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate    # Windows
   ```

2. Instale as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```

---

### 🔐 Configuração do Banco de Dados e Segredos

1. Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`:

   ```bash
   cp .env.example .env
   ```

2. Edite o arquivo `.env` com um editor de texto e preencha os valores em branco:

   - `JWT_SECRET_KEY`: Gere uma chave secreta forte (qualquer string longa e aleatória).
   - `DB_PASSWORD`: A senha do seu usuário do MySQL.

3. Crie o banco de dados no seu MySQL:

   ```sql
   CREATE DATABASE sapt_db;
   ```

---

### 🚀 Execução da Aplicação

1. Inicie o servidor da API (com o ambiente virtual ativado):

   ```bash
   uvicorn main:app --reload
   ```

2. A API estará rodando em:  
   👉 http://127.0.0.1:8000

---

### 👤 Crie o Primeiro Usuário Administrador

Para poder usar os endpoints protegidos, você precisa criar um usuário.  
Abra um novo terminal, ative o mesmo ambiente virtual e execute:

```bash
python create_first_user.py
```

Siga as instruções no terminal para definir:

- Nome de usuário
- E-mail
- Senha

---

### 🧪 Testando a API

Acesse a documentação interativa via Swagger:  
👉 http://127.0.0.1:8000/docs

Use o endpoint `POST /token` para login e então teste os demais endpoints da aplicação.

---
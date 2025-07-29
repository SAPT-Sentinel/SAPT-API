SAPT - API de Análise de Transparência
 

Guia de Instalação e Execução
Siga os passos abaixo para configurar e rodar o projeto no seu ambiente local.

1. Pré-requisitos
Python 3.10 ou superior.

Um servidor MySQL instalado e rodando na sua máquina.

2. Configuração do Ambiente

Crie e ative um ambiente virtual (altamente recomendado):


Instale as dependências do projeto:
pip install -r requirements.txt

3. Configuração do Banco de Dados e Segredos
Copie o arquivo de exemplo .env.example para um novo arquivo chamado .env:
Este arquivo guardará suas configurações locais e segredos.


Edite o arquivo .env:
Abra o arquivo .env com um editor de texto e preencha os valores em branco:

JWT_SECRET_KEY: Gere uma chave secreta forte. Pode ser qualquer string longa e aleatória.

DB_PASSWORD: A senha do seu usuário do MySQL.

Crie o banco de dados no seu MySQL:
Conecte-se ao seu servidor MySQL e execute o seguinte comando:

CREATE DATABASE sapt_db;

4. Execução da Aplicação
Inicie o servidor da API:
Com o ambiente virtual ativado, execute o comando:

uvicorn main:app --reload

A API estará rodando em http://127.0.0.1:8000.

Crie o primeiro usuário administrador:
Para poder usar os endpoints protegidos, você precisa criar um usuário. Abra um novo terminal, ative o mesmo ambiente virtual e execute o script:

python create_first_user.py

Siga as instruções no terminal para definir o nome de usuário, e-mail e senha.

5. Testando a API
Agora, você pode acessar a documentação interativa em http://127.0.0.1:8000/docs para fazer login (POST /token) e testar todos os outros endpoints da aplicação.
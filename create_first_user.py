# -*- coding: utf-8 -*-

import getpass
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import schemas

def main():
    """
    Script para criar o primeiro usuário administrador no sistema.
    """
    print("--- Criação do Primeiro Usuário ---")
    
    db: Session = SessionLocal()
    
    try:
        username = input("Digite o nome de usuário: ")
        
        # Verifica se o usuário já existe
        if crud.get_user(db, username=username):
            print(f"Erro: O usuário '{username}' já existe.")
            return

        email = input("Digite o e-mail: ")
        full_name = input("Digite o nome completo: ")
        # getpass esconde a senha enquanto é digitada no terminal
        password = getpass.getpass("Digite a senha: ")
        password_confirm = getpass.getpass("Confirme a senha: ")

        if password != password_confirm:
            print("Erro: As senhas não coincidem.")
            return

        user_in = schemas.UserCreate(
            username=username,
            email=email,
            full_name=full_name,
            password=password
        )
        
        user = crud.create_user(db, user=user_in)
        print(f"\nUsuário '{user.username}' criado com sucesso!")

    finally:
        db.close()

if __name__ == "__main__":
    main()

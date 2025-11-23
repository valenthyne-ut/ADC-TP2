"""
Este módulo carrega dados de pré-definição de um ficheiro localizado
em `data/data.json` a uma base de dados SQLite, e define meios para
que estes possam ser alterados.

.. warning::
    Este código **NÃO DEVERÁ** ser utilizado em produção sem validações
    e tratamento de exceções.

:Autores: Marino Nechifor e Valentim U. T.
"""
from typing import Literal
from app.database import initialize_database
from app.database.schema.ClientSchema import ClientSchema
from app.database.schema.ContactInfoSchema import ContactInfoSchema
from app.database.schema.ServiceSchema import ServiceSchema
from app.database.schema.TechnicianSchema import TechnicianSchema
from app.database.schema.UserSchema import UserSchema

from app.criacao_perfis import carregar_dados

def load_default_data() -> None:
    """
    Uma função que carrega os dados base do ficheiro
    `app/data/data.json`.

    :return: Nada.
    :rtype: None
    :raises ValueError: Se não for encontrada especialização de um técnico.
    """
    dados = carregar_dados()

    for user in dados.get("Utilizadores"):
        if user is not None:
            db_user = UserSchema.instance.create_one(
                alias=user["Email"],
                full_name=user["Nome"]
            )
    
            db_contact_info = ContactInfoSchema.instance.create_one(
                email=db_user.alias,
                address=user["Morada"],
                phone_num=user["Contacto"]
            )
    
            ClientSchema.instance.create_one(
                db_user.id,
                db_contact_info.id
            )
    
    for service in dados.get("Serviços"):
        if service is not None:
            ServiceSchema.instance.create_one(
                name=service["Nome"],
                price=service["Preço"],
                duration_mins=service["Duração"]
            )
    
    for technician in dados.get("Técnicos"):
        if technician is not None:
            db_user = UserSchema.instance.create_one(
                alias=technician["Email"],
                full_name=technician["Nome"]
            )
    
            db_contact_info = ContactInfoSchema.instance.create_one(
                email=db_user.alias,
                address=technician["Morada"],
                phone_num=technician["Contacto"]
            )
    
            specialization = technician["Especialização"]
    
            db_technician_specialization = ServiceSchema.instance.find_one(
                name=specialization
            )
    
            if db_technician_specialization is None:
                raise ValueError(f"Não foi encontrada '{specialization}' a especialização para o técnico '{db_user.full_name}'!")
            else:
                TechnicianSchema.instance.create_one(
                    user_id=db_user.id,
                    contact_id=db_contact_info.id,
                    specialization_id=db_technician_specialization.id
                )

def main():
    """
    Esta função inicia a base de dados, carrega os dados base para a mesma
    e define um menu de utilização simples da base de dados.

    :return: Nada.
    :rtype: None
    """
    initialize_database()
    
    response = input("\nDeseja carregar dados de exemplo? S/n\n> ").lower()
        
    if response in ("s", "y", "sim", "yes"):
        load_default_data()
        print("Dados de exemplo foram carregados.")
    elif response in ("n", "não", "nao", "no"):
        print("Dados de exemplo não serão carregados.")
    else:
        print("Resposta inválida.")
        exit(-1)
    print()

    while True:
        raw_input = input("\nInsira um comando (H para ajuda.)\n> ")
        if raw_input == "H":
            print("\n".join([
                "Comandos disponíveis: READ, CREATE, DELETE",
                "Tabelas disponíveis: SERVICE, CLIENT, TECHNICIAN, APPOINTMENT",
                "Qualquer texto inserido a seguir da tabela é tratado como argumento de filtro.",
                "O caractér '_' é substituído por um espaço nos argumentos."
                "Exemplos de estrutura de um comando completo:",
                "",
                "READ CONTACT_INFO L2000 -- Lê informações de contacto com um limite de resultados de 2000.",
                "CREATE SERVICE Limpeza_de_piscina 200 120 -- Cria um serviço com o nome 'Limpeza de piscina' com um custo de 200€ e uma duração de 120 minutos."
            ]))
            continue

        try:
            command, table, *arguments = raw_input.split(" ")
        except ValueError:
            print("Input inválido.")
            continue

        print(command, table, len(arguments))
        print(arguments)
             

if __name__ == "__main__":
    main()
# criacao de perfies para serem utilizados pelos clientes/utilizadores e ficar mais organizado

import json
import os

from app.database.schema.UserSchema import UserSchema

FICHEIRO = "app/data/users.json"

def carregar_dados() -> dict:
    if not os.path.exists(FICHEIRO):
        raise FileNotFoundError("O ficheiro data/users.json não existe.")
    with open(FICHEIRO, "r", encoding="utf-8") as f:
        return json.load(f)
    

def guardar_dados(dados):
    with open(FICHEIRO, "w", encoding="utf-8") as f: json.dump(dados, f, indent=4, ensure_ascii=False)


def criar_perfil(tipo, **campos):
    dados = carregar_dados()

    if tipo not in dados:
        raise ValueError("Tipo inválido. Use 'Utilizadores' ou 'Técnicos'.")

    dados[tipo].append(campos)
    guardar_dados(dados)

    print(f"Perfil criado com sucesso em '{tipo}'!")

def procurar_perfil(nome=None, email=None):
    dados = carregar_dados()
    resultados = []

    for tipo in ["Utilizadores", "Técnicos"]:
        for perfil in dados.get(tipo, []):
            if nome and nome.lower() in perfil.get("Nome", "").lower():
                resultados.append((tipo, perfil))
            elif email and perfil.get("Email", "").lower() == email.lower():
                resultados.append((tipo, perfil))

    return resultados

def editar_perfil(nome, **novos_campos):
    dados = carregar_dados()
    alterado = False

    for tipo in ["Utilizadores", "Técnicos"]:
        for perfil in dados.get(tipo, []):
            if nome.lower() == perfil.get("Nome", "").lower():
                for chave, valor in novos_campos.items():
                    if valor is not None:
                        perfil[chave] = valor
                alterado = True

    if alterado:
        guardar_dados(dados)
        print("Perfil atualizado com sucesso!")
    else:
        print("Perfil não encontrado.")
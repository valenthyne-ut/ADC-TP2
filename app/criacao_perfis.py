# criacao de perfies para serem utilizados pelos clientes/utilizadores e ficar mais organizado

import json
import os

from app.database.schema.UserSchema import UserSchema

FICHEIRO = "app/data/users.json"

w
def carregar_dados() -> dict:
    """
    Carrega os dados do ficheiro JSON
    Lê o ficheiro users.json e devolve o seu conteudo com um dicionario
    :raises FileNotFoundError: Se o ficheiro (data/users.json) nao existir 
    :return : Dicionario contem as listas(Utilizadores e Tecnicos)
    :rtype: dict
    """
    if not os.path.exists(FICHEIRO):
        raise FileNotFoundError("O ficheiro data/users.json não existe.")
    with open(FICHEIRO, "r", encoding="utf-8") as f:
        return json.load(f)
    


def guardar_dados(dados):
    """
    Guarda os perfies no ficheiro JSON e substitui o conteudo anterior pelo dicionario fornecido
    :param dict dados: Estrutura contem os perfis que vao ser guardados
    :return: None 
    """
    with open(FICHEIRO, "w", encoding="utf-8") as f: json.dump(dados, f, indent=4, ensure_ascii=False)



def criar_perfil(tipo, **campos):
    """
    Cria um novo perfil e adiciona ao tipo correspondente('Utilizadores' ou 'Técnicos')
    :param str tipo : Categoria do perfil
    :param campos: Campos do perfil(Nome,Email,etc...)
    :raises ValueError: Se o tipo for invalido
    :return: None
    """
    dados = carregar_dados()

    if tipo not in dados:
        raise ValueError("Tipo inválido. Use 'Utilizadores' ou 'Técnicos'.")

    dados[tipo].append(campos)
    guardar_dados(dados)

    print(f"Perfil criado com sucesso em '{tipo}'!")


def procurar_perfil(nome=None, email=None):
    """
    Procura os perfies pelo nomme ou pelo email
    :param str email: Email exato do perfil
    :param str nome: Nome a procurar
    :return : Lista de tuplos(tipo, perfil) correspondentes aos resultados
    :rtype: list
    """
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
    """ 
    Edita um perfil existente , atualizado apenas os campo fornecidos 
    :param str nome: Nome do perfil a editar 
    :param novos campos : Campos a atualizar
    :return :None
    """
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

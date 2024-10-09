import oracledb
import pandas as pd
from tabulate import tabulate

def conectar_banco():
    try:
        connection = oracledb.connect(user="SEU_RM", password="SUA_SENHA", dsn="oracle.fiap.com.br:1521/orcl")
        print("Conexão estabelecida com sucesso.")
        return connection
    except oracledb.DatabaseError as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        return None

def validar_tabelas(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) 
        FROM user_tables 
        WHERE table_name = 'PAVILHOES'
    """)
    pavilhoes_exists = cursor.fetchone()[0]
    
    if pavilhoes_exists == 0:
        print("Criando a tabela 'pavilhoes'...")
        cursor.execute("""
            CREATE TABLE pavilhoes (
                id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                nome VARCHAR2(100),
                capacidade DECIMAL(10,2),
                localizacao VARCHAR2(100),
                disponivel NUMBER(1),
                ativo NUMBER(1)
            )
        """)
        print("Tabela 'pavilhoes' criada com sucesso.")
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM user_tables 
        WHERE table_name = 'MOVIMENTACOES'
    """)
    movimentacoes_exists = cursor.fetchone()[0]
    
    if movimentacoes_exists == 0:
        print("Criando a tabela 'movimentacoes'...")
        cursor.execute("""
            CREATE TABLE movimentacoes (
                id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                tipo_movimentacao VARCHAR2(50),
                tipo_grao VARCHAR2(50),
                quantidade DECIMAL(10,2),
                ativa NUMBER,
                pavilhao_id NUMBER,
                CONSTRAINT fk_pavilhao 
                    FOREIGN KEY (pavilhao_id) 
                    REFERENCES pavilhoes(id)
            )
        """)
        print("Tabela 'movimentacoes' criada com sucesso.")
    
    connection.commit()
    cursor.close()

def limpar_tabelas(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM MOVIMENTACOES")
    cursor.execute("DELETE FROM PAVILHOES")
    connection.commit()
    cursor.close()
    print("Dados de ambas as tabelas excluídos com sucesso.")

def validar_inteiro(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print("Erro: Digite um número inteiro válido.")

def validar_decimal(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("Erro: Digite um número decimal válido.")

def validar_texto(mensagem):
    while True:
        valor = input(mensagem)
        if valor.strip() != "":
            return valor
        else:
            print("Erro: O texto não pode estar vazio.")


def cadastrar_pavilhao(connection):
    cursor = connection.cursor()
    nome = validar_texto("Digite o nome do pavilhão: ")
    capacidade = validar_decimal("Digite a capacidade (toneladas): ")
    localizacao = validar_texto("Digite a localização: ")

    query = """INSERT INTO pavilhoes (nome, capacidade, localizacao, disponivel, ativo) 
               VALUES (:nome, :capacidade, :localizacao, :disponivel, :ativo)"""
    
    cursor.execute(query, {'nome': nome, 'capacidade': capacidade, 'localizacao': localizacao, 'disponivel': True, 'ativo': True})
    connection.commit()
    cursor.close()
    print("Pavilhão cadastrado com sucesso.")

def inativar_pavilhao(connection):
    cursor = connection.cursor()
    
    pavilhao_id = listar_pavilhoes_disponiveis(connection, disponivel=(1))
    
    if pavilhao_id is not None:
        query = "UPDATE pavilhoes SET ativo = :ativo WHERE id = :pavilhao_id"
        cursor.execute(query, {'ativo': False, 'pavilhao_id': pavilhao_id})
        connection.commit()
        cursor.close()
        print(f"Pavilhão com ID {pavilhao_id} foi inativado com sucesso.")
    else:
        return

def listar_pavilhoes_disponiveis(connection, disponivel=(0, 1)):
    cursor = connection.cursor()
    
    query = f"""
        SELECT id, nome, capacidade, localizacao, disponivel 
        FROM pavilhoes 
        WHERE disponivel in {disponivel} AND ativo = 1
    """
    
    cursor.execute(query)
    pavilhoes = cursor.fetchall()

    df = pd.DataFrame(pavilhoes, columns=['ID', 'Nome', 'Capacidade', 'Localização', 'Disponível'])

    pavilhao_id = None
    cursor.close()

    if not df.empty:
        print("\nLista de Pavilhões")
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        print('')
        pavilhao_id = validar_inteiro("Digite o ID do pavilhão: ")
    else:
        print("Nenhum pavilhão ativo e indisponível no momento.")

    return pavilhao_id

def movimentar_estoque(connection):
    cursor = connection.cursor()
    
    tipo_movimentacao = validar_texto("Tipo de movimentação (entrada/saida): ").lower()
    
    if tipo_movimentacao == "entrada":
        pavilhao_id = listar_pavilhoes_disponiveis(connection, disponivel=(1))
        tipo_grao = validar_texto("Digite o tipo de grão: ")
        quantidade = validar_decimal("Quantidade de grãos (toneladas): ")

        cursor.execute("UPDATE pavilhoes SET disponivel = 0 WHERE id = :pavilhao_id", {'pavilhao_id': pavilhao_id})
        cursor.execute(
            """
                INSERT INTO movimentacoes (tipo_movimentacao, tipo_grao, quantidade, ativa, pavilhao_id)
                VALUES (:tipo_movimentacao, :tipo_grao, :quantidade, :ativa, :pavilhao_id)
            """,
            {'tipo_movimentacao': tipo_movimentacao, 'tipo_grao': tipo_grao, 'quantidade': quantidade, 'ativa': 1, 'pavilhao_id': pavilhao_id}
        )

    elif tipo_movimentacao == "saida":
        listar_estoque(connection, disponivel=(0), ativos=True)
        pavilhao_id = validar_inteiro("Digite o ID do pavilhão: ")
        cursor.execute("UPDATE pavilhoes SET disponivel = 1 WHERE id = :pavilhao_id", {'pavilhao_id': pavilhao_id})
        cursor.execute("UPDATE movimentacoes SET ativa = 0 WHERE id = :pavilhao_id", {'pavilhao_id': pavilhao_id})
    
    else:
        print("Tipo de movimentação inválido.")
        return

    connection.commit()
    cursor.close()
    print("Movimentação de estoque registrada com sucesso.")

def listar_estoque(connection, disponivel=(0, 1), ativos=False):
    cursor = connection.cursor()

    where_ativo = "m.ativa != 1"
    if ativos:
        where_ativo = "m.ativa = 1"

    query = f"""
        SELECT p.id, p.nome, p.localizacao, p.capacidade, m.tipo_grao, m.quantidade, p.disponivel
        FROM pavilhoes p
        LEFT JOIN movimentacoes m ON p.id = m.pavilhao_id
        WHERE p.ativo = 1 AND p.disponivel in {disponivel} AND {where_ativo}
    """
    
    cursor.execute(query)
    estoque = cursor.fetchall()

    df = pd.DataFrame(estoque, columns=['ID', 'Nome', 'Localização', 'Capacidade', 'Tipo de Grão', 'Quantidade', 'Disponível'])
    
    if not df.empty:
        print("Lista de Pavilhões")
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    else:
        print("Nenhum pavilhão ativo e indisponível no momento.")

    cursor.close()

def menu_principal(connection):
    while True:
        print("\nMenu Principal:")
        print("1. Cadastrar Pavilhão")
        print("2. Desativar Pavilhão")
        print("3. Movimentar Estoque")
        print("4. Exibir Estoque")
        print("5. Sair\n")

        opcao = validar_texto("Escolha uma opção: ")
        
        if opcao == '1':
            cadastrar_pavilhao(connection)

        elif opcao == '2':
            inativar_pavilhao(connection)

        elif opcao == '3':
            movimentar_estoque(connection)
   
        elif opcao == '4':
            listar_estoque(connection, disponivel=(0), ativos=True)

        elif opcao == '5':
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    connection = conectar_banco()

    # Caso precise limpar as tabelas
    #limpar_tabelas(connection)

    if connection is not None:
        validar_tabelas(connection)
        menu_principal(connection)

        connection.close()
        print("Conexão com o banco de dados encerrada.")
    else:
        print("Falha ao estabelecer a conexão com o banco de dados.")
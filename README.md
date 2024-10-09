# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto
Cap 6 - Python e além

## Nome do grupo
Grupo 32

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/">Ana Beatriz Duarte Domingues</a>
- <a href="https://www.linkedin.com/in/jrsilva051/">Junior Rodrigues da Silva</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Lucas Gomes Moreira</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">André Godoi Chiovato</a>


## 📜 Descrição

*Este projeto refere-se a um software de gestão de aluguel de pavilhões, onde o operador pode realizar as seguintes tarefas:*

- Cadastrar os pavilhões disponíveis para locação.
- Inativar pavilhões que estavam disponíveis para locação, mas não estão mais.
- Realizar movimentação de estoque sempre que um pavilhão for alugado ou desocupado.
- Monitorar o estoque.


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

### Pré-requisitos
Antes de executar o projeto, certifique-se de ter os seguintes pré-requisitos:

- **Python**: Certifique-se de ter o Python instalado. Recomenda-se a versão 3.8 ou superior. Você pode baixar o Python [aqui](https://www.python.org/downloads/).
  
- **Bibliotecas Python**:
  - `oracledb`: Biblioteca para conexão com o banco de dados Oracle.
  - `pandas`: Biblioteca para manipulação de dados.
  - `tabulate`: Biblioteca para formatação de tabelas no console.

  Você pode instalar essas bibliotecas usando `pip`. Execute o seguinte comando no terminal:
  ```bash
  pip install oracledb pandas tabulate

1 - Instalando o Projeto
 Clone o repositório (ou faça o download do código): git clone <URL_DO_REPOSITORIO>

2 - Configure as credenciais do banco de dados
 No arquivo Python, ajuste as credenciais de conexão no método conectar_banco(): connection = oracledb.connect(user="SEU_USUARIO", password="SUA_SENHA", dsn="oracle.fiap.com.br:1521/orcl")

3 - Executando o Código
 a - Abra o terminal.
 b - Navegue até o diretório do projeto.
 c - Execute o script Python: python crud.py


### Funcionalidades
Conexão com o Banco de Dados: O sistema estabelece uma conexão com o banco de dados Oracle.

Validação e Criação de Tabelas: O sistema valida se as tabelas necessárias (pavilhoes e movimentacoes) existem, e as cria caso contrário.

Cadastro de Pavilhão: Permite cadastrar novos pavilhões informando o nome, capacidade e localização.

Inativação de Pavilhão: Permite inativar um pavilhão existente.

Movimentação de Estoque: Registra movimentações de entrada e saída de grãos nos pavilhões.

Listagem de Estoque: Exibe a lista de pavilhões disponíveis e suas movimentações.

Menu Interativo: O sistema possui um menu interativo para facilitar a navegação entre as opções.


## 🗃 Histórico de lançamentos

* 0.1.0 - 09/10/2024
    *

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
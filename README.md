# 🏋️‍♂️ Gerenciador de Treinos - Academia

Sistema simples para gerenciamento de alunos, check-ins de treinos e fila de atendimento presencial em terminal Python integrado com banco de dados MySQL.

## 🚀 Funcionalidades

- **Gestão de Alunos:** Cadastro, listagem de alunos ativos, atualização de status (`Ativo`, `Suspenso`, `Cancelado`), filtragem por modalidade e exclusão.
- **Registro de Treinos:** Check-in de sessões com duração e data/hora atual.
- **Histórico:** Visualização de sessões por aluno em ordem cronológica reversa (LIFO).
- **Fila Presencial:** Gerenciamento de atendimento em ordem de chegada (FIFO).

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **MySQL**
- **mysql-connector-python**

## 📂 Estrutura do Projeto

├── main.py             # Menu principal e fluxo de navegação do sistema

├── alunos.py           # Regras de negócio, manipulação do banco e controle dos alunos

├── banco_de_dados.py   # Script de conexão e criação do banco/tabelas

├── dados.py            # Declaração das variáveis globais, filas e listas estáticas

└── utils.py            # Funções utilitárias de formatação e interface

## 🗄️ Estrutura do Banco de Dados

O banco de dados academia_db é criado e estruturado automaticamente pelo script banco_de_dados.py:

Tabela alunos:

id (INT, Primary Key, Auto Increment) 

nome (VARCHAR) 

modalidade (VARCHAR) 

dias_semana (VARCHAR) 

objetivo (VARCHAR) 

status (VARCHAR) 

Tabela sessoes:

id (INT, Primary Key, Auto Increment)

aluno_id (INT, Foreign Key apontando para alunos(id) em efeito CASCADE)

data (VARCHAR)  

modalidade (VARCHAR)  

duracao (VARCHAR)  

## 🔧 Como Executar o Projeto1. 

1. Pré-requisitos

Certifique-se de ter instalado em sua máquina:

Python 3.8+
MySQL Server / MySQL Workbench2. 

2. Clonar o Repositório

git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio

3. Instalar a Biblioteca do MySQL
Instale o conector do MySQL para Python:

pip install mysql-connector-python

4. Configurar as Credenciais

Abra o arquivo banco_de_dados.py e altere a constante DB_CONFIG com a sua senha e usuário do MySQL:  

DB_CONFIG = {
    'host': 'localhost',
    'user': 'seu_usuario',     # Ex: root
    'password': 'sua_senha',   # Ex: 123456
    'database': 'academia_db'
}

5. Inicializar e ExecutarVocê pode inicializar a estrutura do banco rodando o script de banco de dados e em seguida iniciar a aplicação:

# Para criar a base de dados e tabelas automaticamente:
python banco_de_dados.py

# Para abrir o menu do sistema:
python main.py

## 📄 Licença
Este projeto é totalmente livre para fins acadêmicos, de estudo e aprendizado.

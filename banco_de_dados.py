import mysql.connector

# Configurações de acesso ao MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',        # Altere para seu usuário do MySQL
    'password': 'sua_senha',# Altere para sua senha do MySQL Workbench
    'database': 'academia_db'
}

def conectar():
    """Cria e retorna a conexão com o banco MySQL."""
    return mysql.connector.connect(**DB_CONFIG)

def inicializar_banco():
    """Cria o banco de dados e as tabelas se não existirem."""
    # Conexão inicial sem especificar banco para poder criar o DATABASE
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cursor = conn.cursor()
    
    # Cria o banco de dados
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    cursor.close()
    conn.close()

    # Conecta no banco criado para criar as tabelas
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de Alunos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            modalidade VARCHAR(50) NOT NULL,
            dias_semana VARCHAR(20) NOT NULL,
            objetivo VARCHAR(100) NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'Ativo'
        )
    ''')

    # Tabela de Sessões
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessoes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            aluno_id INT NOT NULL,
            data VARCHAR(30) NOT NULL,
            modalidade VARCHAR(50) NOT NULL,
            duracao VARCHAR(20) NOT NULL,
            FOREIGN KEY (aluno_id) REFERENCES alunos (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

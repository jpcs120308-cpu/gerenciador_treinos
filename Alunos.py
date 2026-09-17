from banco import conectar
from dados import fila_atendimento, modalidades
from utils import titulo
from datetime import datetime

def cadastrar_aluno():
    titulo("Cadastrar Novo Aluno")
    
    nome = input("Nome do aluno: ")
    
    print("\nModalidades disponíveis:")
    for i, modalidade in enumerate(modalidades, 1):
        print(f"{i}. {modalidade}")
    
    try:
        opcao = int(input(f"Escolha a modalidade (1-{len(modalidades)}): "))
        modalidade = modalidades[opcao - 1]
    except (ValueError, IndexError):
        print("Opção inválida. Usando Musculação como padrão.")
        modalidade = modalidades[0]
    
    dias_semana = input("Dias por semana (ex: 3, 5, 6): ")
    
    objetivos = ["Perda de peso", "Ganho de massa muscular", "Condicionamento físico", "Reabilitação"]
    print("\nObjetivos disponíveis:")
    for i, obj in enumerate(objetivos, 1):
        print(f"{i}. {obj}")
    
    try:
        opcao_obj = int(input("Escolha o objetivo (1-4): "))
        objetivo = objetivos[opcao_obj - 1]
    except (ValueError, IndexError):
        print("Opção inválida. Usando Condicionamento físico como padrão.")
        objetivo = objetivos[2]
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alunos (nome, modalidade, dias_semana, objetivo, status)
        VALUES (%s, %s, %s, %s, 'Ativo')
    ''', (nome, modalidade, dias_semana, objetivo))
    conn.commit()
    aluno_id = cursor.lastrowid
    
    cursor.close()
    conn.close()

    print(f"\n✅ Aluno {nome} cadastrado com sucesso!")
    print(f"Status: Ativo | ID do aluno: {aluno_id}")

def listar_alunos():
    titulo("Alunos Ativos")
    
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT a.*, COUNT(s.id) AS total_sessoes
        FROM alunos a
        LEFT JOIN sessoes s ON a.id = s.aluno_id
        WHERE a.status = 'Ativo'
        GROUP BY a.id
    ''')
    ativos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if not ativos:
        print("Nenhum aluno ativo encontrado.")
        return
    
    for i, aluno in enumerate(ativos, 1):
        print(f"ALUNO: {i}")
        print(f"ID: {aluno['id']}")
        print(f"Nome: {aluno['nome']}")
        print(f"Modalidade: {aluno['modalidade']}")
        print(f"Dias/Semana: {aluno['dias_semana']}")
        print(f"Objetivo: {aluno['objetivo']}")
        print(f"Status: {aluno['status']}")
        print(f"Total de Sessões: {aluno['total_sessoes']}\n")

def atualizar_status_aluno():
    titulo("Atualizar Status do Aluno")
    
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome, status FROM alunos")
    alunos = cursor.fetchall()
    
    if not alunos:
        print("Nenhum aluno cadastrado.")
        cursor.close()
        conn.close()
        return
    
    print("Alunos cadastrados:")
    for aluno in alunos:
        emoji = "✅" if aluno['status'] == "Ativo" else "⚠️" if aluno['status'] == "Suspenso" else "❌"
        print(f"ID: {aluno['id']} - {aluno['nome']} - Status: {emoji} {aluno['status']}")
    
    try:
        id_aluno = int(input("\nDigite o ID do aluno: "))
    except ValueError:
        print("Digite um número válido.")
        cursor.close()
        conn.close()
        return
    
    cursor.execute("SELECT * FROM alunos WHERE id = %s", (id_aluno,))
    aluno = cursor.fetchone()
    
    if not aluno:
        print("❌ Aluno não encontrado.")
        cursor.close()
        conn.close()
        return

    novo_status = None
    status_atual = aluno['status']
    print(f"\nStatus atual: {status_atual}")
    
    if status_atual in ["Ativo", "Suspenso"]:
        print("\n1 - " + ("Suspender" if status_atual == "Ativo" else "Reativar (voltar para Ativo)"))
        print("2 - Cancelar")
        opcao = input("Escolha: ")
        
        if opcao == "1":
            novo_status = "Suspenso" if status_atual == "Ativo" else "Ativo"
        elif opcao == "2":
            novo_status = "Cancelado"
    else:
        reativar = input("Deseja reativar o aluno? (s/n): ")
        if reativar.lower() == 's':
            novo_status = "Ativo"
    
    if novo_status:
        cursor.execute("UPDATE alunos SET status = %s WHERE id = %s", (novo_status, id_aluno))
        conn.commit()
        print(f"✅ Status do aluno {aluno['nome']} alterado para {novo_status}!")
        
    cursor.close()
    conn.close()

def registrar_checkin():
    titulo("Registrar Check-in de Treino")
    
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome, modalidade FROM alunos WHERE status = 'Ativo'")
    ativos = cursor.fetchall()
    
    if not ativos:
        print("Nenhum aluno ativo disponível para check-in.")
        cursor.close()
        conn.close()
        return
    
    print("Alunos ativos:")
    for aluno in ativos:
        print(f"ID: {aluno['id']} - {aluno['nome']} - Modalidade: {aluno['modalidade']}")
    
    try:
        id_aluno = int(input("\nDigite o ID do aluno: "))
    except ValueError:
        print("Digite um número válido.")
        cursor.close()
        conn.close()
        return
    
    cursor.execute("SELECT * FROM alunos WHERE id = %s AND status = 'Ativo'", (id_aluno,))
    aluno = cursor.fetchone()
    
    if aluno:
        duracao = input("Duração do treino (minutos): ")
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        cursor.execute('''
            INSERT INTO sessoes (aluno_id, data, modalidade, duracao)
            VALUES (%s, %s, %s, %s)
        ''', (id_aluno, data_atual, aluno['modalidade'], duracao))
        conn.commit()
        
        # Adiciona à fila em memória[cite: 1, 2]
        fila_atendimento.append({"id": aluno['id'], "nome": aluno['nome'], "modalidade": aluno['modalidade']})
        print(f"\n✅ Check-in registrado para {aluno['nome']} em {data_atual}!")
        cursor.close()
        conn.close()
        return

    print("Aluno não encontrado ou não está ativo.")
    cursor.close()
    conn.close()

def ver_historico_sessoes():
    titulo("Histórico de Sessões por Aluno (Mais recentes primeiro)")
    
    try:
        id_aluno = int(input("Digite o ID do aluno: "))
    except ValueError:
        print("Digite um número válido.")
        return

    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nome FROM alunos WHERE id = %s", (id_aluno,))
    aluno = cursor.fetchone()
    
    if not aluno:
        print("Aluno não encontrado.")
        cursor.close()
        conn.close()
        return

    cursor.execute("SELECT * FROM sessoes WHERE aluno_id = %s ORDER BY id DESC", (id_aluno,))
    sessoes = cursor.fetchall()

    if not sessoes:
        print(f"\n{aluno['nome']} ainda não possui sessões registradas.")
    else:
        print(f"\nHistórico de {aluno['nome']} (Total: {len(sessoes)} sessões)")
        print("=" * 40)
        for i, sessao in enumerate(sessoes, 1):
            print(f"Sessão {i}:")
            print(f"  Data: {sessao['data']}")
            print(f"  Modalidade: {sessao['modalidade']}")
            print(f"  Duração: {sessao['duracao']} minutos\n")

    cursor.close()
    conn.close()

def listar_por_modalidade():
    titulo("Alunos por Modalidade")
    
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    
    for modalidade in modalidades:
        print(f"\n{modalidade.upper()}:")
        print("-" * 40)
        
        cursor.execute('''
            SELECT a.nome, a.status, COUNT(s.id) as total_sessoes
            FROM alunos a
            LEFT JOIN sessoes s ON a.id = s.aluno_id
            WHERE a.modalidade = %s
            GROUP BY a.id
        ''', (modalidade,))
        alunos_modalidade = cursor.fetchall()

        if not alunos_modalidade:
            print("Nenhum aluno nesta modalidade.")
        else:
            for aluno in alunos_modalidade:
                emoji = "✅" if aluno['status'] == "Ativo" else "⚠️" if aluno['status'] == "Suspenso" else "❌"
                print(f"{emoji} {aluno['nome']} - {aluno['status']} - Sessões: {aluno['total_sessoes']}")

    cursor.close()
    conn.close()

def deletar_aluno():
    titulo("Deletar Aluno")
    
    try:
        id_aluno = int(input("Digite o ID do aluno que deseja deletar: "))
    except ValueError:
        print("❌ Digite um número válido.")
        return

    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alunos WHERE id = %s", (id_aluno,))
    aluno = cursor.fetchone()

    if not aluno:
        print(f"❌ Aluno com ID {id_aluno} não encontrado.")
        cursor.close()
        conn.close()
        return

    confirmar = input(f"\n⚠️ Tem certeza que deseja DELETAR permanentemente '{aluno['nome']}'? (s/n): ")
    if confirmar.lower() == 's':
        cursor.execute("DELETE FROM sessoes WHERE aluno_id = %s", (id_aluno,))
        cursor.execute("DELETE FROM alunos WHERE id = %s", (id_aluno,))
        conn.commit()
        
        # Limpa da fila presencial se estiver lá[cite: 1, 2]
        fila_atendimento[:] = [a for a in fila_atendimento if a['id'] != id_aluno]
        print(f"\n✅ Aluno '{aluno['nome']}' deletado com sucesso!")
        
    cursor.close()
    conn.close(

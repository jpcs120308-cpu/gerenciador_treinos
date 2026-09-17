from dados import alunos, fila_atendimento, modalidades, status_aluno
from utils import titulo
from alunos import cadastrar_aluno, listar_alunos, atualizar_status_aluno, ver_historico_sessoes, listar_por_modalidade, registrar_checkin, deletar_aluno

def mostrar_menu():
    titulo("Gerenciador de Treinos - Academia")
    print("1. Cadastrar Aluno")
    print("2. Listar Alunos Ativos")
    print("3. Fila de Atendimento Presencial")  # FIFO
    print("4. Registrar Check-in de Treino")
    print("5. Atualizar Status do Aluno")
    print("6. Ver Histórico de Sessões por Aluno")  # LIFO
    print("7. Listar Alunos por Modalidade")
    print("8. DELETAR Aluno")
    print("9. Sair")

while True:
    mostrar_menu()
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        cadastrar_aluno()
    elif opcao == "2":
        listar_alunos()
    elif opcao == "3":
        if fila_atendimento:
            print(f"\nFILA DE ATENDIMENTO (FIFO):")
            print("-" * 40)
            for i, aluno in enumerate(fila_atendimento, 1):
                print(f"{i}º - {aluno['nome']} - {aluno['modalidade']}")
            print("-" * 40)
            print(f"\nPróximo aluno a ser atendido: {fila_atendimento[0]['nome']}")
            remover = input("\nDeseja remover da fila (atender)? (s/n): ")
            if remover.lower() == 's':
                atendido = fila_atendimento.pop(0)
                print(f"\n✅ {atendido['nome']} foi atendido e removido da fila!")
        else:
            print("\nFila de atendimento vazia!")
    elif opcao == "4":
        registrar_checkin()
    elif opcao == "5":
        atualizar_status_aluno()
    elif opcao == "6":
        ver_historico_sessoes()
    elif opcao == "7":
        listar_por_modalidade()
    elif opcao == "8":
        deletar_aluno()
    elif opcao == "9":
        print("\n👋 Saindo do programa...")
        break
    else:
        print("\n❌ Opção inválida. Tente novamente.")

# Sistema de Gerenciamento de Academia
Projeto desenvolvido em Python para gerenciamento simples de alunos de uma academia via terminal.

O sistema permite:

- Cadastro de alunos
- Controle de status
- Registro de check-in
- Histórico de sessões
- Organização por modalidade
- Fila de atendimento (FIFO)
- Histórico de treinos (LIFO)
- Exclusão de alunos

---

# Tecnologias Utilizadas

- Python 3
- MySQL
- Estruturas de Dados:
  - Lista
  - Fila (FIFO)
  - Pilha (LIFO)
- Modularização em arquivos `.py`

---

# Estrutura do Projeto

```bash
📁 projeto-academia
│
├── main.py        # Arquivo principal do sistema
├── alunos.py      # Funções relacionadas aos alunos
├── dados.py       # Armazenamento das estruturas de dados
├── utils.py       # Funções auxiliares
├── registro.SQL   # Banco de dados para registro dos dados dos clientes
└── README.md


(este projeto foi baseado no projeto do "GsacomaniR", créditos totais a ele) 

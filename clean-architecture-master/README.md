# Sistema de Gestão Acadêmica

Projeto desenvolvido para a disciplina de Arquitetura de Software, utilizando **Clean Architecture** (Arquitetura Limpa).

**Grupo:** Bruno Rodrigues dos Santos · Carlos Eduardo Carvalho Meneguette · Leandro de Araujo · Vinicius Andrade Michaki Hubner

---

## Como executar

**Requisitos:** Python 3.8+ e pip instalados.

```bash
# 1. Entrar na pasta do projeto
cd pt2

# 2. Instalar dependências
pip install -r src/requirements.txt

# 3. Iniciar o servidor
python -m src.main
```

Abrir no browser: **http://127.0.0.1:5000**

> O banco de dados `academico.db` é criado automaticamente na primeira execução.

### Páginas disponíveis

| URL | Descrição |
|-----|-----------|
| `http://127.0.0.1:5000/` | Página inicial com navegação |
| `http://127.0.0.1:5000/cadastrar-aluno` | Cadastrar um novo aluno |
| `http://127.0.0.1:5000/lancar-nota` | Lançar nota para um aluno |
| `http://127.0.0.1:5000/consultar-desempenho` | Consultar notas, média e situação acadêmica |

---

## Estrutura do projeto

```
pt2/
└── src/
    ├── domain/
    │   └── entities/               # Entidades de domínio (Aluno, Nota)
    ├── application/
    │   ├── use_cases/              # Casos de uso (CadastrarAluno, LancarNota, ConsultarDesempenho)
    │   └── repositories/           # Interfaces/contratos (IAlunoRepository, INotaRepository)
    ├── interface_adapters/
    │   ├── controllers/            # Controllers Flask
    │   └── repositories_impl/     # Implementações SQLite e memória
    └── infrastructure/
        ├── database/               # Conexão e inicialização SQLite
        └── web/
            ├── app.py              # Factory Flask
            └── templates/          # Templates HTML por módulo
```

## Sprints

| Sprint | Descrição |
|--------|-----------|
| Sprint 1 | Estrutura base da Clean Architecture + entidade `Aluno` + repositório em memória |
| Sprint 2 | Persistência SQLite + Lançar Nota + Consultar Desempenho + interface web modular |

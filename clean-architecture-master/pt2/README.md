# Sistema de Gestão Acadêmica — Sprint 3

## Como Rodar e Usar (Leia Primeiro)

### 1. Instalar dependências

```bash
pip install flask pytest
```

### 2. Entrar na pasta correta

```bash
cd pt2
```

> **Todos os comandos abaixo devem ser executados dentro da pasta `pt2`.**

### 3. Iniciar o servidor web

```bash
python -m flask --app src/infrastructure/web/app.py run
```

Acesse `http://localhost:5000` no navegador.

### 4. Fazer login

O banco já vem com três usuários prontos:

| Perfil              | Login    | Senha      | O que vê                               |
| ------------------- | -------- | ---------- | -------------------------------------- |
| **Aluno**           | `aluno1` | `aluno123` | Desempenho, Média, Aprovação           |
| **Professor**       | `prof1`  | `prof123`  | Lançar Nota/Frequência, Acompanhamento |
| **Administrador**   | `admin`  | `admin123` | Tudo — cadastros, gestão, usuários     |

> O aluno `aluno1` (matrícula `2026001`) já tem dados na disciplina `ARQ01`
> (notas 8.5 e 7.0, 85% de frequência) — use esses valores para testar as
> consultas imediatamente após o login.

### 5. Rodar os testes automatizados

```bash
python -m pytest src/tests/test_use_cases.py -v
```

32 testes, todos passando.

---

## Arquitetura: Clean Architecture

O projeto segue a **Arquitetura Limpa** (Clean Architecture) de Robert C. Martin.
As dependências sempre fluem de fora para dentro: a infraestrutura depende dos
adaptadores, que dependem dos casos de uso, que dependem apenas das entidades de
domínio. Nenhuma camada interna conhece a externa.

```
┌─────────────────────────────────────────────────┐
│           Infrastructure (Flask, SQLite)         │  ← mais externo
│  ┌───────────────────────────────────────────┐   │
│  │    Interface Adapters (Controllers,       │   │
│  │    Presenters, Repositories Impl)         │   │
│  │  ┌─────────────────────────────────────┐  │   │
│  │  │  Application (Use Cases, DTOs,      │  │   │
│  │  │  Repository Interfaces)             │  │   │
│  │  │  ┌───────────────────────────────┐  │  │   │
│  │  │  │  Domain (Entities + Rules)    │  │  │   │  ← mais interno
│  │  │  └───────────────────────────────┘  │  │   │
│  │  └─────────────────────────────────────┘  │   │
│  └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## Funcionalidades Implementadas

### Sprint 3 — Novas funcionalidades

#### Entidade Professor (Domínio)

- `domain/entities/professor.py` — entidade com matrícula funcional, nome e e-mail
- `POST /professores` — cadastrar professor
- `GET /professores` — listar todos os professores

#### Autenticação de Usuários

- `domain/entities/usuario.py` — senha em SHA-256, perfis: aluno / professor / administrador
- `POST /usuarios` — cadastrar usuário
- `POST /auth/login` — autenticar e receber token UUID de sessão

#### Calcular Média (caso de uso independente)

- `application/use_cases/calcular_media.py` — média aritmética das notas com status
- `GET /media/<matricula>/<disciplina>` — retorna média e status (Aprovado ≥ 6.0 / Reprovado)

#### Alterar Situação do Aluno

- `PATCH /alunos/<matricula>/situacao` — Ativo, Trancado ou Formado

#### Listar Alunos

- `GET /alunos` — retorna todos os alunos com matrícula, nome e situação

### Sprint 2 — Funcionalidades revisadas

| Funcionalidade | Endpoint | Regra de negócio |
| --- | --- | --- |
| Cadastrar Aluno | `POST /alunos` | Matrícula única |
| Cadastrar Disciplina | `POST /disciplinas` | Carga horária > 0 |
| Matricular Aluno | `POST /matriculas` | Sem duplicatas; valida aluno e disciplina |
| Lançar Nota | `POST /notas` | Valor entre 0.0 e 10.0; requer matrícula ativa |
| Lançar Frequência | `POST /frequencias` | Presencas <= total de aulas |
| Consultar Desempenho | `GET /desempenho/<matricula>` | Boletim via DTO + Presenter |
| Calcular Aprovação | `GET /aprovacao/<mat>/<disc>` | Media >= 6.0 e frequencia >= 75% |

---

## Melhorias Arquiteturais (Sprint 3 vs Sprint 2)

### Violações corrigidas

- **`print()` removido dos casos de uso** — output é responsabilidade do Presenter, não do Use Case
- **`MemoryAlunoRepository` incompleto** — estava sem `buscar_por_matricula`, `listar_todos` e `atualizar_situacao`; reescrito com `dict` para lookup O(1)
- **PRAGMA inconsistente** — `_criar_tabelas()` não habilitava `foreign_keys = ON`; corrigido

### Padrões adicionados

- **DTO para cada caso de uso** — `AlunoResumoDTO`, `AprovacaoDTO`, `MediaDTO`, `ProfessorResumoDTO`, `AutenticacaoDTO`
- **Presenter para cada fluxo** — `AlunoListaPresenter`, `AprovacaoPresenter`, `MediaPresenter`, `ProfessorListaPresenter`, `AutenticacaoPresenter`
- **Container (Composition Root)** — único ponto de montagem de toda a árvore de dependências em `infrastructure/di/container.py`

---

## Estrutura de Pastas

```text
pt2/
├── academico.db               # Banco SQLite (gerado ao rodar)
├── README.md
└── src/
    ├── domain/
    │   └── entities/
    │       ├── aluno.py            # situacao: Ativo/Trancado/Formado
    │       ├── disciplina.py
    │       ├── frequencia.py
    │       ├── matricula.py
    │       ├── nota.py
    │       ├── professor.py        # NOVO
    │       └── usuario.py          # NOVO — senha SHA-256, perfis
    ├── application/
    │   ├── dtos/
    │   │   ├── desempenho_dto.py
    │   │   ├── aluno_dto.py        # NOVO
    │   │   ├── aprovacao_dto.py    # NOVO
    │   │   ├── autenticacao_dto.py # NOVO
    │   │   ├── media_dto.py        # NOVO
    │   │   └── professor_dto.py    # NOVO
    │   ├── repositories/           # Interfaces abstratas (sem dependência de SQLite)
    │   │   ├── aluno_repository.py
    │   │   ├── disciplina_repository.py
    │   │   ├── frequencia_repository.py
    │   │   ├── matricula_repository.py
    │   │   ├── nota_repository.py
    │   │   ├── professor_repository.py # NOVO
    │   │   └── usuario_repository.py   # NOVO
    │   └── use_cases/
    │       ├── cadastrar_aluno.py
    │       ├── cadastrar_disciplina.py
    │       ├── matricular_aluno.py
    │       ├── lancar_nota.py
    │       ├── lancar_frequencia.py
    │       ├── consultar_desempenho.py
    │       ├── listar_alunos.py          # NOVO
    │       ├── alterar_situacao_aluno.py # NOVO
    │       ├── calcular_aprovacao.py     # NOVO
    │       ├── calcular_media.py         # NOVO
    │       ├── cadastrar_professor.py    # NOVO
    │       ├── listar_professores.py     # NOVO
    │       ├── cadastrar_usuario.py      # NOVO
    │       └── autenticar_usuario.py     # NOVO
    ├── interface_adapters/
    │   ├── controllers/
    │   │   ├── aluno_controller.py
    │   │   ├── disciplina_controller.py
    │   │   ├── matricula_controller.py
    │   │   ├── nota_controller.py
    │   │   ├── frequencia_controller.py
    │   │   ├── desempenho_controller.py
    │   │   ├── alterar_situacao_controller.py # NOVO
    │   │   ├── aprovacao_controller.py        # NOVO
    │   │   ├── media_controller.py            # NOVO
    │   │   ├── professor_controller.py        # NOVO
    │   │   └── autenticacao_controller.py     # NOVO
    │   ├── presenters/
    │   │   ├── desempenho_presenter.py
    │   │   ├── aluno_lista_presenter.py  # NOVO
    │   │   ├── aprovacao_presenter.py    # NOVO
    │   │   ├── autenticacao_presenter.py # NOVO
    │   │   ├── media_presenter.py        # NOVO
    │   │   └── professor_presenter.py    # NOVO
    │   └── repositories_impl/
    │       ├── sqlite_aluno_repository.py
    │       ├── sqlite_disciplina_repository.py
    │       ├── sqlite_frequencia_repository.py
    │       ├── sqlite_matricula_repository.py
    │       ├── sqlite_nota_repository.py
    │       ├── sqlite_professor_repository.py # NOVO
    │       └── sqlite_usuario_repository.py   # NOVO
    ├── infrastructure/
    │   ├── database/
    │   │   └── sqlite_connection.py   # cria todas as tabelas
    │   ├── di/
    │   │   └── container.py           # Composition Root — monta tudo
    │   └── web/
    │       └── app.py                 # Flask + HTML frontend com login por perfil
    └── tests/
        └── test_use_cases.py          # 32 testes automatizados
```

---

## Testes Automatizados

```bash
python -m pytest src/tests/test_use_cases.py -v
```

Os 32 testes cobrem:

- Validações de domínio (Nota, Frequência, Disciplina, Aluno, Usuario)
- Fluxo completo de desempenho com Presenter (JSON e console)
- Listar e alterar situação de alunos
- Calcular aprovação (Aprovado / Reprovado por Nota / Reprovado por Frequência / Em Andamento)
- CRUD de Professor
- Autenticação (sucesso, senha errada, usuário inexistente, perfil inválido, duplicatas)
- Calcular Média (Aprovado por Nota / Reprovado por Nota / Sem notas lançadas)

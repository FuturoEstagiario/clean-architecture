# Sistema de Gestão Acadêmica — Sprint 3 (Consolidação Arquitetural)

## Arquitetura Escolhida
**Clean Architecture** (Arquitetura Limpa). O código é estruturado de forma concêntrica, garantindo que as dependências fluam sempre de fora para dentro (infraestrutura e adaptadores dependem dos casos de uso, que dependem exclusivamente das entidades de domínio).

---

## Descrição das implementações e evolução arquitetural - Sprint 3

### 1. Melhorias Arquiteturais em relação à Sprint 2 (Correções Efetuadas)
* **Baixo Acoplamento e Composition Root (Container)**: Na Sprint 2, os controllers instanciavam diretamente o repositório SQLite concretamente. Para resolver este acoplamento, implementamos um container de injeção de dependência centralizado em `src/infrastructure/di/container.py` (**Composition Root**). O container monta a conexão com o banco, instacia os repositórios e os injeta nos casos de uso e nos controllers. Os controllers não possuem dependência física ou importação do SQLite.
* **Desacoplamento Use Case vs. Apresentação (DTOs)**: O caso de uso `ConsultarDesempenho` não retorna mais dicionários genéricos (`dict`). Criamos um DTO estruturado e tipado em `src/application/dtos/desempenho_dto.py` para transportar os dados processados para a camada externa.
* **Formatação Centralizada (Presenters)**: Criamos o `DesempenhoPresenter` na camada de adaptadores de interface. Ele recebe o `DesempenhoDTO` e gera o formato ideal de exibição (JSON formatado para API HTTP Flask ou relatório amigável em ASCII para terminal CLI).

---

### 2. Novas Funcionalidades da Sprint 3

#### A. Cadastrar Disciplina
* **Descrição**: Permite registrar uma disciplina no sistema para que alunos possam ser matriculados.
* **Componentes envolvidos**: `disciplina_controller.py` -> `cadastrar_disciplina.py` (Use Case) -> `Disciplina` (Entity) -> `IDisciplinaRepository` (Interface) -> `sqlite_disciplina_repository.py` (Persistence).
* **Regra de Negócio**: A carga horária da disciplina deve ser maior que 0.
* **Persistência**: Tabela `disciplinas` no SQLite.
* **Exemplos de Entrada e Saída**:
  * *Entrada (HTTP POST /disciplinas)*: `{"codigo": "ARQ01", "nome": "Arquitetura de Software", "carga_horaria": 60}`
  * *Saída*: `{"status": "sucesso", "mensagem": "Disciplina 'Arquitetura de Software' cadastrada com sucesso."}`

#### B. Matricular Aluno em Disciplina
* **Descrição**: Vincula um aluno cadastrado a uma disciplina ativa.
* **Componentes envolvidos**: `matricula_controller.py` -> `matricular_aluno.py` (Use Case) -> `Matricula` (Entity) -> `IMatriculaRepository` (Interface) -> `sqlite_matricula_repository.py` (Persistence).
* **Regra de Negócio**: Valida a existência do aluno e da disciplina no banco e impede que o aluno seja matriculado em duplicidade na mesma disciplina.
* **Persistência**: Tabela `matriculas` no SQLite.
* **Exemplos de Entrada e Saída**:
  * *Entrada (HTTP POST /matriculas)*: `{"aluno_matricula": "2026001", "disciplina_codigo": "ARQ01"}`
  * *Saída*: `{"status": "sucesso", "mensagem": "Aluno '2026001' matriculado na disciplina 'ARQ01'."}`

#### C. Lançar Frequência
* **Descrição**: Registra o total de aulas e a presença de um aluno em determinada disciplina.
* **Componentes envolvidos**: `frequencia_controller.py` -> `lancar_frequencia.py` (Use Case) -> `Frequencia` (Entity) -> `IFrequenciaRepository` (Interface) -> `sqlite_frequencia_repository.py` (Persistence).
* **Regra de Negócio**: Valida se o aluno possui matrícula ativa na disciplina. O total de aulas deve ser maior que zero, presenças não podem ser negativas e não podem exceder o total de aulas.
* **Persistência**: Tabela `frequencias` no SQLite.
* **Exemplos de Entrada e Saída**:
  * *Entrada (HTTP POST /frequencias)*: `{"aluno_matricula": "2026001", "disciplina_codigo": "ARQ01", "aulas_presente": 18, "aulas_total": 20}`
  * *Saída*: `{"status": "sucesso", "mensagem": "Frequência lançada com sucesso."}`

---

### 3. Funcionalidades de Sprints Anteriores (Revisadas e Integradas no SQLite)

#### D. Lançar Nota (Sprint 2)
* **Fluxo**: `nota_controller.py` -> `lancar_nota.py` (Use Case) -> `Nota` (Entity) -> `INotaRepository` (Interface) -> `sqlite_nota_repository.py`.
* **Regra de Negócio**: Valida se o aluno está matriculado na disciplina. A nota deve ser validada na Entidade `Nota` (deve estar entre 0.0 e 10.0).
* **Persistência**: Tabela `notas` no SQLite.

#### E. Consultar Desempenho Acadêmico (Sprint 2)
* **Fluxo**: `desempenho_controller.py` -> `consultar_desempenho.py` (Use Case) -> `DesempenhoDTO` -> `DesempenhoPresenter` -> Exibição final (JSON ou Console).

---

### 4. Evolução pós-Sprint 3 — Modularização Web, Novos Módulos e Autenticação

#### A. Interface Web Modular (Blueprints + páginas por módulo)
* Cada módulo (Alunos, Professores, Disciplinas, Matrículas, Notas, Frequências, Desempenho) possui um Blueprint próprio em `src/infrastructure/web/routes/` e uma página própria com layout comum (`base.html` + sidebar). Páginas HTML em `/alunos`, `/professores`, ...; API JSON em `/api/alunos`, `/api/professores`, ...
* O `Container` continua único (Composition Root), anexado ao app e acedido via `current_app`.

#### B. Listagens (GET)
* **Fluxo**: rota GET -> controller -> use case (`ListarAlunos`, `ListarDisciplinas`, `ListarMatriculas`, `ListarProfessores`) -> interface -> repositório SQLite.
* **Saída**: `{"status": "sucesso", "dados": [...]}` renderizado em tabela na página do módulo.

#### C. Cadastrar/Listar Professor
* **Componentes**: `professor_routes.py` -> `professor_controller.py` -> `cadastrar_professor.py` / `listar_professores.py` -> `Professor` (Entity) -> `IProfessorRepository` -> `sqlite_professor_repository.py` (tabela `professores`).
* **Regra de Negócio**: registro e nome obrigatórios (validados na entidade).
* **Exemplo**: POST `/api/professores` com `{"registro": "P001", "nome": "Philipe Fransozi"}`.

#### D. Autenticação de Usuários (escopo mínimo do TP1)
* **Componentes**: `auth_routes.py` -> `auth_controller.py` -> `AutenticarUsuario` (Use Case) -> `Usuario` (Entity, perfis aluno/professor/admin) -> portas `IUsuarioRepository` e `IPasswordHasher` -> adaptadores `sqlite_usuario_repository.py` e `werkzeug_password_hasher.py`.
* **Regras de Negócio**: senha armazenada como hash; mensagem única para login/senha inválidos (evita enumeração de usuários); senha mínima de 6 caracteres; login único.
* **Proteção global**: `before_request` em `app.py` — páginas redirecionam para `/login`, chamadas `/api/...` recebem 401 sem sessão ativa.
* **Usuário inicial**: criado automaticamente `admin` / `admin123` (trocar em produção).

---

## Estrutura de Pastas Completa
```
pt2/
├── academico.db           # Banco de dados SQLite (gerado na execução)
├── README.md              # Este arquivo
├── src/
│   ├── __init__.py
│   ├── main.py            # CLI Demo Executável
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── aluno.py
│   │   │   ├── disciplina.py
│   │   │   ├── frequencia.py
│   │   │   ├── matricula.py
│   │   │   ├── nota.py
│   │   │   ├── professor.py
│   │   │   └── usuario.py
│   ├── application/
│   │   ├── dtos/
│   │   │   └── desempenho_dto.py
│   │   ├── repositories/
│   │   │   ├── aluno_repository.py
│   │   │   ├── disciplina_repository.py
│   │   │   ├── frequencia_repository.py
│   │   │   ├── matricula_repository.py
│   │   │   ├── nota_repository.py
│   │   │   ├── professor_repository.py
│   │   │   └── usuario_repository.py
│   │   ├── services/
│   │   │   └── password_hasher.py
│   │   ├── use_cases/
│   │   │   ├── autenticar_usuario.py
│   │   │   ├── cadastrar_aluno.py
│   │   │   ├── cadastrar_disciplina.py
│   │   │   ├── cadastrar_professor.py
│   │   │   ├── cadastrar_usuario.py
│   │   │   ├── consultar_desempenho.py
│   │   │   ├── lancar_frequencia.py
│   │   │   ├── lancar_nota.py
│   │   │   ├── listar_alunos.py
│   │   │   ├── listar_disciplinas.py
│   │   │   ├── listar_matriculas.py
│   │   │   ├── listar_professores.py
│   │   │   └── matricular_aluno.py
│   ├── interface_adapters/
│   │   ├── controllers/
│   │   │   ├── aluno_controller.py
│   │   │   ├── auth_controller.py
│   │   │   ├── desempenho_controller.py
│   │   │   ├── disciplina_controller.py
│   │   │   ├── frequencia_controller.py
│   │   │   ├── matricula_controller.py
│   │   │   ├── nota_controller.py
│   │   │   └── professor_controller.py
│   │   ├── presenters/
│   │   │   └── desempenho_presenter.py
│   │   ├── repositories_impl/
│   │   │   │   ├── sqlite_aluno_repository.py
│   │   │   ├── sqlite_disciplina_repository.py
│   │   │   ├── sqlite_frequencia_repository.py
│   │   │   ├── sqlite_matricula_repository.py
│   │   │   ├── sqlite_nota_repository.py
│   │   │   ├── sqlite_professor_repository.py
│   │   │   └── sqlite_usuario_repository.py
│   ├── infrastructure/
│   │   ├── database/
│   │   │   └── sqlite_connection.py
│   │   ├── di/
│   │   │   └── container.py
│   │   ├── security/
│   │   │   └── werkzeug_password_hasher.py
│   │   ├── web/
│   │   │   ├── app.py             # App factory Flask + proteção de login
│   │   │   ├── routes/            # Um Blueprint por módulo
│   │   │   ├── static/            # style.css, app.js
│   │   │   └── templates/         # base.html + uma página por módulo + login.html
│   └── tests/
│       └── test_use_cases.py
```

---

## Como Executar e Testar

### 1. Requisitos de Instalação
Certifique-se de que os pacotes necessários estão instalados:
```bash
pip install flask pytest
```

### 2. Executar Demonstração Console (CLI)
A demonstração inicializa o banco SQLite limpo, cria as entidades, executa regras de validação (mostrando erros controlados para notas e frequências inválidas) e imprime o boletim final através do Presenter.
```bash
cd pt2
python -m src.main
```

### 3. Iniciar o Servidor Web Flask
```bash
cd pt2
python -m src.infrastructure.web.app
```
O servidor rodará na porta `5000`. Acesse `http://localhost:5000` no navegador — qualquer página redireciona para `/login`. Credenciais iniciais: **admin** / **admin123** (usuário criado automaticamente na primeira execução).

A API JSON (`/api/...`) exige sessão autenticada: requisições sem login recebem `401`. Para testar via cURL/Postman, autentique-se primeiro em `POST /login` e reutilize o cookie de sessão.

### 4. Rodar Testes Automatizados
```bash
cd pt2
pytest -v
```

# Sistema de Gestão Acadêmica — Sprint 2

## Arquitetura escolhida

**Clean Architecture** (Arquitetura Limpa).

O projeto organiza o código em camadas concêntricas onde as dependências apontam sempre para dentro — o domínio não conhece ninguém, a aplicação conhece só o domínio, e a infraestrutura implementa as interfaces definidas pelas camadas internas.

## Estrutura de pastas

```
src/
├── domain/
│   └── entities/               # Regras de negócio puras (Aluno, Nota)
├── application/
│   ├── use_cases/              # Casos de uso (CadastrarAluno, LancarNota, ConsultarDesempenho)
│   └── repositories/           # Interfaces/contratos (IAlunoRepository, INotaRepository)
├── interface_adapters/
│   ├── controllers/            # Controllers Flask (aluno_controller, nota_controller)
│   └── repositories_impl/     # Implementações concretas (SQLite e memória)
└── infrastructure/
    ├── database/               # Inicialização e conexão SQLite
    └── web/
        ├── app.py              # Factory Flask (create_app)
        └── templates/          # Interface web (index.html)
```

## Como executar

**Requisitos:** Python 3.8+ e pip instalados.

```bash
# 1. Entrar na pasta do projeto
cd clean-architecture-master/pt2

# 2. Instalar dependências
pip install -r src/requirements.txt

# 3. Iniciar o servidor
python -m src.main
```

Abrir no browser: **http://127.0.0.1:5000**

> O banco de dados `academico.db` é criado automaticamente na primeira execução — não é necessário nenhuma configuração adicional.

### Páginas disponíveis

| URL | Descrição |
|-----|-----------|
| `http://127.0.0.1:5000/` | Página inicial com navegação |
| `http://127.0.0.1:5000/cadastrar-aluno` | Cadastrar um novo aluno |
| `http://127.0.0.1:5000/lancar-nota` | Lançar nota para um aluno |
| `http://127.0.0.1:5000/consultar-desempenho` | Consultar notas, média e situação acadêmica |

---

## Descrição das implementações e fluxo arquitetural

### Funcionalidade 1 — Lançar Nota

**Nome da funcionalidade:** Lançar Nota

**Onde o fluxo começa:** Requisição `POST /notas` via interface web ou ferramenta HTTP (ex: curl, Postman).

**Componentes que participam:**
- `index.html` — interface que envia o formulário
- `nota_controller.py` — recebe e valida a requisição HTTP
- `LancarNota` (use case) — orquestra a operação
- `Nota` (entity) — aplica a regra de negócio
- `INotaRepository` (interface) — contrato de persistência
- `SQLiteNotaRepository` — implementação concreta
- `database.py` / `academico.db` — persistência SQLite

**Onde fica a regra de negócio:** Na entidade `Nota` (`domain/entities/nota.py`). O construtor levanta `NotaValorInvalidoError` se `valor < 0` ou `valor > 10`. O controller nunca toma essa decisão.

**Onde os dados são armazenados:** Tabela `notas` no ficheiro `academico.db` (SQLite), criado automaticamente na primeira execução.

**Como executar ou testar:**

```bash
# Cadastrar um aluno primeiro
curl -X POST http://127.0.0.1:5000/alunos \
  -H "Content-Type: application/json" \
  -d '{"matricula": "2026001", "nome": "Carlos Silva"}'

# Lançar uma nota válida
curl -X POST http://127.0.0.1:5000/notas \
  -H "Content-Type: application/json" \
  -d '{"matricula": "2026001", "disciplina": "Matemática", "valor": 8.5}'

# Tentar lançar nota inválida (deve retornar erro 422)
curl -X POST http://127.0.0.1:5000/notas \
  -H "Content-Type: application/json" \
  -d '{"matricula": "2026001", "disciplina": "Física", "valor": 11}'
```

**Resultado esperado:** `201 Created` com os dados da nota lançada. Valor fora do intervalo [0, 10] retorna `422 Unprocessable Entity` com mensagem de erro.

**Fluxo:** `Web UI → nota_controller → LancarNota (use case) → Nota (entity, valida 0–10) → INotaRepository → SQLiteNotaRepository → SQLite`

---

### Funcionalidade 2 — Consultar Desempenho Acadêmico

**Nome da funcionalidade:** Consultar Desempenho Acadêmico

**Onde o fluxo começa:** Requisição `GET /desempenho/<matricula>` via interface web ou ferramenta HTTP.

**Componentes que participam:**
- `index.html` — interface que dispara a consulta
- `nota_controller.py` — recebe a requisição e chama o use case
- `ConsultarDesempenho` (use case) — calcula média e determina situação
- `INotaRepository` (interface) — contrato de leitura
- `SQLiteNotaRepository` — busca todas as notas da matrícula
- `database.py` / `academico.db` — fonte dos dados

**Onde fica a regra de negócio:** No use case `ConsultarDesempenho` (`application/use_cases/consultar_desempenho.py`). Ali são aplicadas as regras: média = soma(notas) / quantidade, e situação = `"Aprovado"` se média ≥ 7,0, caso contrário `"Reprovado"`. Nenhuma dessas decisões existe no controller.

**Onde os dados são armazenados ou consultados:** Tabela `notas` no `academico.db`, consultada por matrícula.

**Como executar ou testar:**

```bash
# Após lançar pelo menos uma nota para a matrícula 2026001:
curl http://127.0.0.1:5000/desempenho/2026001
```

**Resultado esperado:** JSON com a lista de notas, média calculada e situação acadêmica (`Aprovado` / `Reprovado`). Se não houver notas, retorna `"situacao": "Sem notas registradas"`.

**Fluxo:** `Web UI → nota_controller → ConsultarDesempenho (use case, calcula média e situação) → INotaRepository → SQLiteNotaRepository → SQLite`

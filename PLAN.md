# PLAN.md — Modularização do SGA (Sistema de Gestão Acadêmica)

## Checklist Técnica
- [x] Etapa 1 — Blueprints por módulo + uma página por módulo (base.html + sidebar); API movida para /api/*
- [x] Etapa 2 — Use cases de listagem (alunos, disciplinas, matrículas) + GET /api/* + tabelas nas páginas
- [x] Etapa 3 — Módulo Professores completo (entidade → SQLite → página)
- [x] Etapa 4 — Autenticação com perfis (aluno/professor/admin), proteção global de páginas e API, seed admin
- [x] Testes: 15 a passar (pytest)
- [ ] Futuro: vínculo professor↔disciplina; bloqueio de cadastro duplicado; gestão de usuários (admin)

## 💡 Conceito Chave
O Blueprint do Flask é a unidade de modularização da camada mais externa (Frameworks & Drivers).
Cada módulo do domínio tem o seu ficheiro de rotas, que só conhece o controller do próprio módulo
via current_app.container — o Container continua a ser o único Composition Root. Na autenticação,
a validação de credenciais é regra de negócio (use case AutenticarUsuario, dependente das portas
IUsuarioRepository e IPasswordHasher), enquanto a sessão (cookie) é detalhe de infraestrutura
(Flask session + before_request).

## 📚 Dicionário de Implementação
| Item | O que é |
|---|---|
| `Blueprint("nome", __name__)` | Grupo de rotas nomeado, registado via `register_blueprint`. O nome namespacia os endpoints (`aluno.pagina`, `auth.entrar`). |
| `current_app` | Proxy do Flask para o app ativo no request — acesso ao `app.container` sem import circular. |
| `@app.before_request` | Hook executado antes de toda rota; devolver resposta curto-circuita o request (usado para exigir login). |
| `session` | Dicionário assinado criptograficamente, armazenado em cookie; requer `secret_key`. |
| `werkzeug.security` | `generate_password_hash` / `check_password_hash` — hash de senha com salt. |
| `request.get_json(silent=True)` | Devolve `None` em body inválido em vez de lançar exceção (caminho infeliz → 400 limpo). |
| `INSERT OR REPLACE` | Upsert do SQLite: cadastro repetido atualiza em vez de falhar. |
| `esc()` em app.js | Escape de HTML antes de inserir dados em `innerHTML` — previne XSS armazenado. |

## 🧪 Como testar
1. `cd pt2` e `python -m pytest -v` → 15 testes a passar.
2. `cd pt2` e `python -m src.infrastructure.web.app` → abrir http://localhost:5000 →
   redireciona para /login → entrar com `admin` / `admin123` → navegar pelos 7 módulos na sidebar.
   `curl http://localhost:5000/api/alunos` sem cookie devolve 401.

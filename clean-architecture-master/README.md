# Sistema de Gestão Académica — Sprint 1

## Arquitetura escolhida

**Clean Architecture** (Arquitetura Limpa).

O projeto organiza o código em camadas concêntricas onde as dependências apontam sempre para dentro — o domínio não conhece ninguém, a aplicação conhece só o domínio, e a infraestrutura implementa as interfaces definidas pelas camadas internas.

## Fluxo iniciado

**Cadastro de Aluno** — o único caso de uso implementado neste sprint.

O fluxo percorre as camadas de fora para dentro e de volta:

```
main.py
  └─> CadastrarAluno (Use Case)
        └─> Aluno (Entity)
        └─> IAlunoRepository (interface)
              └─> MemoryAlunoRepository (implementação em memória)
```

## Principais pastas

```
src/
├── domain/
│   └── entities/          # Regras de negócio puras (Aluno)
├── application/
│   ├── use_cases/         # Casos de uso (CadastrarAluno)
│   └── repositories/      # Interfaces/contratos (IAlunoRepository)
├── interface_adapters/
│   └── repositories_impl/ # Implementações concretas (MemoryAlunoRepository)
└── infrastructure/
    └── web/               # Ponto de entrada web (app.py — preparado, não ativo)
```

## O que está funcionando

- Entidade `Aluno` criada com matrícula, nome e situação padrão `"Ativo"`.
- Contrato `IAlunoRepository` definido com método `salvar`.
- Implementação `MemoryAlunoRepository` armazenando alunos em lista em memória.
- Caso de uso `CadastrarAluno` orquestrando a criação e persistência.
- `main.py` executando o fluxo completo e exibindo os registros salvos no terminal.

Para executar:

```bash
cd pt2
python -m src.main
```

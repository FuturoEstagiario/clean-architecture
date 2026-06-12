import pytest
import os
from src.domain.entities.aluno import Aluno
from src.domain.entities.disciplina import Disciplina
from src.domain.entities.nota import Nota
from src.domain.entities.frequencia import Frequencia
from src.infrastructure.di.container import Container


@pytest.fixture
def clean_container():
    db_name = "test_academico.db"
    if os.path.exists(db_name):
        try:
            os.remove(db_name)
        except PermissionError:
            pass
    container = Container(db_name)
    yield container
    if os.path.exists(db_name):
        try:
            os.remove(db_name)
        except PermissionError:
            pass


# ── Testes de Unidade — Entidades (Regras de Domínio) ────────────────────────

def test_validar_carga_horaria_disciplina():
    d = Disciplina("ARQ01", "Arquitetura", 60)
    assert d.carga_horaria == 60
    with pytest.raises(ValueError, match="A carga horária deve ser maior que zero."):
        Disciplina("ARQ02", "Inválida", 0)


def test_validar_limites_nota():
    n1 = Nota("2026001", "ARQ01", 10.0, "TP1")
    n2 = Nota("2026001", "ARQ01", 0.0, "TP2")
    assert n1.valor == 10.0
    assert n2.valor == 0.0
    with pytest.raises(ValueError, match="A nota deve estar entre 0.0 e 10.0."):
        Nota("2026001", "ARQ01", 10.1, "TP1")
    with pytest.raises(ValueError, match="A nota deve estar entre 0.0 e 10.0."):
        Nota("2026001", "ARQ01", -0.5, "TP1")


def test_validar_limites_frequencia():
    f = Frequencia("2026001", "ARQ01", 15, 20)
    assert f.percentual == 75.0
    with pytest.raises(ValueError, match="O número de presenças não pode ser maior que o total de aulas."):
        Frequencia("2026001", "ARQ01", 21, 20)
    with pytest.raises(ValueError, match="O total de aulas deve ser maior que zero."):
        Frequencia("2026001", "ARQ01", 5, 0)


def test_alterar_situacao_aluno_valida():
    aluno = Aluno("2026001", "Maria")
    assert aluno.situacao == "Ativo"
    aluno.alterar_situacao("Trancado")
    assert aluno.situacao == "Trancado"
    aluno.alterar_situacao("Formado")
    assert aluno.situacao == "Formado"


def test_alterar_situacao_aluno_invalida():
    aluno = Aluno("2026001", "Maria")
    with pytest.raises(ValueError, match="Situação inválida"):
        aluno.alterar_situacao("Suspenso")


# ── Testes de Integração — Casos de Uso com Persistência SQLite ──────────────

def test_cadastrar_aluno_e_buscar(clean_container):
    res = clean_container.aluno_controller.cadastrar("12345", "Alice")
    assert res["status"] == "sucesso"
    aluno = clean_container.aluno_repository.buscar_por_matricula("12345")
    assert aluno is not None
    assert aluno.nome == "Alice"
    assert aluno.situacao == "Ativo"


def test_matricular_aluno_duplicado(clean_container):
    clean_container.aluno_controller.cadastrar("12345", "Alice")
    clean_container.disciplina_controller.cadastrar("DISC1", "Programação", 60)
    res1 = clean_container.matricula_controller.matricular("12345", "DISC1")
    assert res1["status"] == "sucesso"
    res2 = clean_container.matricula_controller.matricular("12345", "DISC1")
    assert res2["status"] == "erro"
    assert "já está matriculado" in res2["mensagem"]


def test_lancar_nota_sem_matricula(clean_container):
    clean_container.aluno_controller.cadastrar("12345", "Alice")
    clean_container.disciplina_controller.cadastrar("DISC1", "Programação", 60)
    res = clean_container.nota_controller.lancar("12345", "DISC1", 8.5, "Prova")
    assert res["status"] == "erro"
    assert "Matrícula não encontrada" in res["mensagem"]


def test_fluxo_completo_desempenho_presenter(clean_container):
    clean_container.aluno_controller.cadastrar("12345", "Alice")
    clean_container.disciplina_controller.cadastrar("DISC1", "Programação", 60)
    clean_container.matricula_controller.matricular("12345", "DISC1")
    clean_container.nota_controller.lancar("12345", "DISC1", 9.0, "TP1")
    clean_container.nota_controller.lancar("12345", "DISC1", 7.0, "TP2")
    clean_container.frequencia_controller.lancar("12345", "DISC1", 16, 20)

    res_json = clean_container.desempenho_controller.consultar_json("12345")
    assert res_json["status"] == "sucesso"
    dados = res_json["dados"]
    assert dados["aluno"]["nome"] == "Alice"
    assert dados["desempenho_disciplinas"][0]["media_final"] == 8.0
    assert dados["desempenho_disciplinas"][0]["frequencia"]["percentual"] == "80.0%"

    res_console = clean_container.desempenho_controller.consultar_console("12345")
    assert "BOLETIM ACADÊMICO: Alice" in res_console
    assert "Média Final: 8.00" in res_console
    assert "Frequência: 16/20 aulas (80.0%)" in res_console


# ── Testes das Novas Funcionalidades — Sprint 3 ──────────────────────────────

def test_listar_alunos(clean_container):
    clean_container.aluno_controller.cadastrar("001", "Alice")
    clean_container.aluno_controller.cadastrar("002", "Bruno")
    res = clean_container.aluno_controller.listar()
    assert res["status"] == "sucesso"
    nomes = [a["nome"] for a in res["dados"]]
    assert "Alice" in nomes
    assert "Bruno" in nomes


def test_listar_alunos_vazio(clean_container):
    res = clean_container.aluno_controller.listar()
    assert res["status"] == "sucesso"
    assert res["dados"] == []


def test_alterar_situacao_aluno(clean_container):
    clean_container.aluno_controller.cadastrar("001", "Carlos")
    res = clean_container.alterar_situacao_controller.alterar("001", "Trancado")
    assert res["status"] == "sucesso"
    aluno = clean_container.aluno_repository.buscar_por_matricula("001")
    assert aluno.situacao == "Trancado"


def test_alterar_situacao_invalida(clean_container):
    clean_container.aluno_controller.cadastrar("001", "Carlos")
    res = clean_container.alterar_situacao_controller.alterar("001", "Suspenso")
    assert res["status"] == "erro"
    assert "Situação inválida" in res["mensagem"]


def test_alterar_situacao_aluno_inexistente(clean_container):
    res = clean_container.alterar_situacao_controller.alterar("INEXISTENTE", "Trancado")
    assert res["status"] == "erro"
    assert "não encontrado" in res["mensagem"]


def test_calcular_aprovacao_aprovado(clean_container):
    clean_container.aluno_controller.cadastrar("001", "Diana")
    clean_container.disciplina_controller.cadastrar("MAT01", "Matemática", 60)
    clean_container.matricula_controller.matricular("001", "MAT01")
    clean_container.nota_controller.lancar("001", "MAT01", 8.0, "P1")
    clean_container.nota_controller.lancar("001", "MAT01", 7.0, "P2")
    clean_container.frequencia_controller.lancar("001", "MAT01", 18, 20)

    res = clean_container.aprovacao_controller.calcular("001", "MAT01")
    assert res["status"] == "sucesso"
    assert res["dados"]["resultado"]["status"] == "Aprovado"
    assert res["dados"]["resultado"]["media"] == 7.5


def test_calcular_aprovacao_reprovado_por_nota(clean_container):
    clean_container.aluno_controller.cadastrar("001", "Eduardo")
    clean_container.disciplina_controller.cadastrar("MAT01", "Matemática", 60)
    clean_container.matricula_controller.matricular("001", "MAT01")
    clean_container.nota_controller.lancar("001", "MAT01", 4.0, "P1")
    clean_container.nota_controller.lancar("001", "MAT01", 5.0, "P2")
    clean_container.frequencia_controller.lancar("001", "MAT01", 18, 20)

    res = clean_container.aprovacao_controller.calcular("001", "MAT01")
    assert res["status"] == "sucesso"
    assert res["dados"]["resultado"]["status"] == "Reprovado por Nota"


def test_calcular_aprovacao_reprovado_por_frequencia(clean_container):
    clean_container.aluno_controller.cadastrar("001", "Fernanda")
    clean_container.disciplina_controller.cadastrar("MAT01", "Matemática", 60)
    clean_container.matricula_controller.matricular("001", "MAT01")
    clean_container.nota_controller.lancar("001", "MAT01", 8.0, "P1")
    clean_container.frequencia_controller.lancar("001", "MAT01", 10, 20)

    res = clean_container.aprovacao_controller.calcular("001", "MAT01")
    assert res["status"] == "sucesso"
    assert res["dados"]["resultado"]["status"] == "Reprovado por Frequência"


def test_calcular_aprovacao_em_andamento(clean_container):
    clean_container.aluno_controller.cadastrar("001", "Gabriel")
    clean_container.disciplina_controller.cadastrar("MAT01", "Matemática", 60)
    clean_container.matricula_controller.matricular("001", "MAT01")

    res = clean_container.aprovacao_controller.calcular("001", "MAT01")
    assert res["status"] == "sucesso"
    assert res["dados"]["resultado"]["status"] == "Em Andamento"


def test_calcular_aprovacao_aluno_sem_matricula(clean_container):
    clean_container.aluno_controller.cadastrar("001", "Helena")
    clean_container.disciplina_controller.cadastrar("MAT01", "Matemática", 60)

    res = clean_container.aprovacao_controller.calcular("001", "MAT01")
    assert res["status"] == "erro"
    assert "não está matriculado" in res["mensagem"]


# ── Testes Professor ──────────────────────────────────────────────────────────

def test_cadastrar_professor(clean_container):
    res = clean_container.professor_controller.cadastrar("PROF001", "Dr. Ana Lima", "ana@uni.br")
    assert res["status"] == "sucesso"
    prof = clean_container.professor_repository.buscar_por_matricula("PROF001")
    assert prof is not None
    assert prof.nome == "Dr. Ana Lima"
    assert prof.email == "ana@uni.br"


def test_cadastrar_professor_duplicado(clean_container):
    clean_container.professor_controller.cadastrar("PROF001", "Dr. Ana Lima", "ana@uni.br")
    res = clean_container.professor_controller.cadastrar("PROF001", "Outro Nome", "outro@uni.br")
    assert res["status"] == "erro"
    assert "já cadastrado" in res["mensagem"]


def test_listar_professores(clean_container):
    clean_container.professor_controller.cadastrar("PROF001", "Dr. Ana Lima", "ana@uni.br")
    clean_container.professor_controller.cadastrar("PROF002", "Dr. Carlos Melo", "carlos@uni.br")
    res = clean_container.professor_controller.listar()
    assert res["status"] == "sucesso"
    nomes = [p["nome"] for p in res["dados"]]
    assert "Dr. Ana Lima" in nomes
    assert "Dr. Carlos Melo" in nomes


# ── Testes Autenticação ───────────────────────────────────────────────────────

def test_cadastrar_usuario(clean_container):
    res = clean_container.autenticacao_controller.cadastrar("alice", "Alice Silva", "senha123", "aluno")
    assert res["status"] == "sucesso"


def test_cadastrar_usuario_perfil_invalido(clean_container):
    res = clean_container.autenticacao_controller.cadastrar("joao", "João", "senha123", "coordenador")
    assert res["status"] == "erro"
    assert "Perfil inválido" in res["mensagem"]


def test_cadastrar_usuario_duplicado(clean_container):
    clean_container.autenticacao_controller.cadastrar("alice", "Alice Silva", "senha123", "aluno")
    res = clean_container.autenticacao_controller.cadastrar("alice", "Alice Outra", "abc1", "professor")
    assert res["status"] == "erro"
    assert "já existe" in res["mensagem"]


def test_autenticar_usuario_sucesso(clean_container):
    clean_container.autenticacao_controller.cadastrar("alice", "Alice Silva", "senha123", "aluno")
    res = clean_container.autenticacao_controller.autenticar("alice", "senha123")
    assert res["status"] == "sucesso"
    assert res["dados"]["autenticado"] is True
    assert res["dados"]["perfil"] == "aluno"
    assert res["dados"]["token"] != ""


def test_autenticar_usuario_senha_errada(clean_container):
    clean_container.autenticacao_controller.cadastrar("alice", "Alice Silva", "senha123", "aluno")
    res = clean_container.autenticacao_controller.autenticar("alice", "errada")
    assert res["status"] == "erro"
    assert res["dados"]["autenticado"] is False


def test_autenticar_usuario_inexistente(clean_container):
    res = clean_container.autenticacao_controller.autenticar("naoexiste", "qualquer")
    assert res["status"] == "erro"
    assert res["dados"]["autenticado"] is False


def test_perfis_validos_usuario():
    from src.domain.entities.usuario import Usuario
    u = Usuario("joao", "João", "professor")
    assert u.perfil == "professor"
    with pytest.raises(ValueError, match="Perfil inválido"):
        Usuario("x", "X", "coordenador")


# ── Testes CalcularMedia ──────────────────────────────────────────────────────

def test_calcular_media_aprovado(clean_container):
    clean_container.aluno_controller.cadastrar("001", "Igor")
    clean_container.disciplina_controller.cadastrar("MAT01", "Matemática", 60)
    clean_container.matricula_controller.matricular("001", "MAT01")
    clean_container.nota_controller.lancar("001", "MAT01", 7.0, "P1")
    clean_container.nota_controller.lancar("001", "MAT01", 8.0, "P2")

    res = clean_container.media_controller.calcular("001", "MAT01")
    assert res["status"] == "sucesso"
    assert res["dados"]["media"] == 7.5
    assert res["dados"]["status"] == "Aprovado por Nota"


def test_calcular_media_reprovado(clean_container):
    clean_container.aluno_controller.cadastrar("001", "Julia")
    clean_container.disciplina_controller.cadastrar("MAT01", "Matemática", 60)
    clean_container.matricula_controller.matricular("001", "MAT01")
    clean_container.nota_controller.lancar("001", "MAT01", 3.0, "P1")
    clean_container.nota_controller.lancar("001", "MAT01", 4.0, "P2")

    res = clean_container.media_controller.calcular("001", "MAT01")
    assert res["status"] == "sucesso"
    assert res["dados"]["media"] == 3.5
    assert res["dados"]["status"] == "Reprovado por Nota"


def test_calcular_media_sem_notas(clean_container):
    clean_container.aluno_controller.cadastrar("001", "Karla")
    clean_container.disciplina_controller.cadastrar("MAT01", "Matemática", 60)
    clean_container.matricula_controller.matricular("001", "MAT01")

    res = clean_container.media_controller.calcular("001", "MAT01")
    assert res["status"] == "sucesso"
    assert res["dados"]["status"] == "Sem notas lançadas"

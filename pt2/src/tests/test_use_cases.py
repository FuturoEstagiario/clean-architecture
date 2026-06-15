import pytest
import os
from src.domain.entities.aluno import Aluno
from src.domain.entities.disciplina import Disciplina
from src.domain.entities.nota import Nota
from src.domain.entities.frequencia import Frequencia
from src.infrastructure.di.container import Container

# Fixture para inicializar um Container com banco de dados em memória ou arquivo de teste limpo
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
    
    # Teardown
    if os.path.exists(db_name):
        try:
            os.remove(db_name)
        except PermissionError:
            pass

# 1. Testes de Unidade — Entidades (Regras de Domínio)
def test_validar_carga_horaria_disciplina():
    # Carga horária válida
    d = Disciplina("ARQ01", "Arquitetura", 60)
    assert d.carga_horaria == 60
    
    # Carga horária inválida deve lançar ValueError
    with pytest.raises(ValueError, match="A carga horária deve ser maior que zero."):
        Disciplina("ARQ02", "Inválida", 0)

def test_validar_limites_nota():
    # Notas válidas
    n1 = Nota("2026001", "ARQ01", 10.0, "TP1")
    n2 = Nota("2026001", "ARQ01", 0.0, "TP2")
    assert n1.valor == 10.0
    assert n2.valor == 0.0
    
    # Notas inválidas devem lançar ValueError
    with pytest.raises(ValueError, match="A nota deve estar entre 0.0 e 10.0."):
        Nota("2026001", "ARQ01", 10.1, "TP1")
    with pytest.raises(ValueError, match="A nota deve estar entre 0.0 e 10.0."):
        Nota("2026001", "ARQ01", -0.5, "TP1")

def test_validar_limites_frequencia():
    # Frequência válida
    f = Frequencia("2026001", "ARQ01", 15, 20)
    assert f.percentual == 75.0
    
    # Presenças maiores que total de aulas deve lançar ValueError
    with pytest.raises(ValueError, match="O número de presenças não pode ser maior que o total de aulas."):
        Frequencia("2026001", "ARQ01", 21, 20)
    # Total de aulas menor ou igual a zero
    with pytest.raises(ValueError, match="O total de aulas deve ser maior que zero."):
        Frequencia("2026001", "ARQ01", 5, 0)

# 2. Testes de Integração — Casos de Uso com Persistência SQLite
def test_cadastrar_aluno_e_buscar(clean_container):
    aluno_controller = clean_container.aluno_controller
    aluno_repo = clean_container.aluno_repository
    
    # Cadastrar via controller
    res = aluno_controller.cadastrar("12345", "Alice")
    assert res["status"] == "sucesso"
    
    # Buscar direto no repositório para confirmar persistência
    aluno = aluno_repo.buscar_por_matricula("12345")
    assert aluno is not None
    assert aluno.nome == "Alice"
    assert aluno.situacao == "Ativo"

def test_matricular_aluno_duplicado(clean_container):
    clean_container.aluno_controller.cadastrar("12345", "Alice")
    clean_container.disciplina_controller.cadastrar("DISC1", "Programação", 60)
    
    # Primeira matrícula
    res1 = clean_container.matricula_controller.matricular("12345", "DISC1")
    assert res1["status"] == "sucesso"
    
    # Matrícula duplicada deve retornar erro
    res2 = clean_container.matricula_controller.matricular("12345", "DISC1")
    assert res2["status"] == "erro"
    assert "já está matriculado" in res2["mensagem"]

def test_lancar_nota_sem_matricula(clean_container):
    clean_container.aluno_controller.cadastrar("12345", "Alice")
    clean_container.disciplina_controller.cadastrar("DISC1", "Programação", 60)
    
    # Tentar lançar nota sem ter feito matrícula
    res = clean_container.nota_controller.lancar("12345", "DISC1", 8.5, "Prova")
    assert res["status"] == "erro"
    assert "Matrícula não encontrada" in res["mensagem"]

def test_fluxo_completo_desempenho_presenter(clean_container):
    # Setup de dados válidos
    clean_container.aluno_controller.cadastrar("12345", "Alice")
    clean_container.disciplina_controller.cadastrar("DISC1", "Programação", 60)
    clean_container.matricula_controller.matricular("12345", "DISC1")
    
    clean_container.nota_controller.lancar("12345", "DISC1", 9.0, "TP1")
    clean_container.nota_controller.lancar("12345", "DISC1", 7.0, "TP2")
    clean_container.frequencia_controller.lancar("12345", "DISC1", 16, 20)
    
    # Consultar Desempenho
    res_json = clean_container.desempenho_controller.consultar_json("12345")
    assert res_json["status"] == "sucesso"
    
    dados = res_json["dados"]
    assert dados["aluno"]["nome"] == "Alice"
    assert dados["desempenho_disciplinas"][0]["media_final"] == 8.0
    assert dados["desempenho_disciplinas"][0]["frequencia"]["percentual"] == "80.0%"
    
    # Testar Presenter do console
    res_console = clean_container.desempenho_controller.consultar_console("12345")
    assert "BOLETIM ACADÊMICO: Alice" in res_console
    assert "Média Final: 8.00" in res_console
    assert "Frequência: 16/20 aulas (80.0%)" in res_console

def test_listar_alunos_ordenados_por_nome(clean_container):
    clean_container.aluno_controller.cadastrar("2", "Bruno")
    clean_container.aluno_controller.cadastrar("1", "Alice")

    res = clean_container.aluno_controller.listar()
    assert res["status"] == "sucesso"
    assert [a["nome"] for a in res["dados"]] == ["Alice", "Bruno"]

def test_listar_disciplinas_e_matriculas(clean_container):
    clean_container.aluno_controller.cadastrar("1", "Alice")
    clean_container.disciplina_controller.cadastrar("DISC1", "Programação", 60)
    clean_container.matricula_controller.matricular("1", "DISC1")

    assert clean_container.disciplina_controller.listar()["dados"][0]["codigo"] == "DISC1"
    assert clean_container.matricula_controller.listar()["dados"][0]["aluno_matricula"] == "1"

def test_cadastrar_e_listar_professor(clean_container):
    res = clean_container.professor_controller.cadastrar("P001", "Philipe")
    assert res["status"] == "sucesso"
    assert clean_container.professor_controller.listar()["dados"][0]["registro"] == "P001"

def test_professor_sem_nome_retorna_erro(clean_container):
    res = clean_container.professor_controller.cadastrar("P002", "   ")
    assert res["status"] == "erro"
    assert "obrigatório" in res["mensagem"]

def test_autenticar_usuario_valido(clean_container):
    clean_container.cadastrar_usuario_use_case.executar("bruno", "segredo1", "professor")
    res = clean_container.auth_controller.autenticar("bruno", "segredo1")
    assert res["status"] == "sucesso"
    assert res["dados"]["perfil"] == "professor"

def test_autenticar_senha_errada(clean_container):
    clean_container.cadastrar_usuario_use_case.executar("bruno", "segredo1", "aluno")
    res = clean_container.auth_controller.autenticar("bruno", "errada")
    assert res["status"] == "erro"
    assert res["mensagem"] == "Login ou senha inválidos."

def test_admin_seed_criado_automaticamente(clean_container):
    res = clean_container.auth_controller.autenticar("admin", "admin123")
    assert res["status"] == "sucesso"
    assert res["dados"]["perfil"] == "admin"

def test_login_duplicado_retorna_erro(clean_container):
    clean_container.cadastrar_usuario_use_case.executar("bruno", "segredo1", "aluno")
    with pytest.raises(ValueError, match="já está em uso"):
        clean_container.cadastrar_usuario_use_case.executar("bruno", "outrasenha", "admin")

def test_aluno_matricula_vazia_retorna_erro():
    with pytest.raises(ValueError, match="matrícula do aluno é obrigatória"):
        Aluno("", "João")

def test_aluno_nome_vazio_retorna_erro():
    with pytest.raises(ValueError, match="nome do aluno é obrigatório"):
        Aluno("2026001", "")

def test_aluno_nome_apenas_espacos_retorna_erro():
    with pytest.raises(ValueError, match="nome do aluno é obrigatório"):
        Aluno("2026001", "   ")

def test_cadastrar_usuario_senha_curta_retorna_erro(clean_container):
    with pytest.raises(ValueError, match="senha deve ter pelo menos 6 caracteres"):
        clean_container.cadastrar_usuario_use_case.executar("joao", "abc", "aluno")

def test_cadastrar_disciplina_codigo_duplicado_retorna_erro(clean_container):
    clean_container.disciplina_controller.cadastrar("DISC1", "Programação", 60)
    res = clean_container.disciplina_controller.cadastrar("DISC1", "Outra", 40)
    assert res["status"] == "erro"
    assert "já cadastrada" in res["mensagem"]

def test_consultar_desempenho_sem_matriculas(clean_container):
    clean_container.aluno_controller.cadastrar("12345", "Alice")
    res = clean_container.desempenho_controller.consultar_json("12345")
    assert res["status"] == "sucesso"
    assert res["dados"]["desempenho_disciplinas"] == []

def test_consultar_desempenho_sem_frequencia_assume_100(clean_container):
    clean_container.aluno_controller.cadastrar("12345", "Alice")
    clean_container.disciplina_controller.cadastrar("DISC1", "Programação", 60)
    clean_container.matricula_controller.matricular("12345", "DISC1")
    clean_container.nota_controller.lancar("12345", "DISC1", 8.0, "TP1")
    res = clean_container.desempenho_controller.consultar_json("12345")
    assert res["status"] == "sucesso"
    freq = res["dados"]["desempenho_disciplinas"][0]["frequencia"]
    assert freq["percentual"] == "100.0%"

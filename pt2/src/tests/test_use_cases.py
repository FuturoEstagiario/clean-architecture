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

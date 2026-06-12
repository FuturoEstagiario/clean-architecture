from src.infrastructure.database.sqlite_connection import SQLiteConnection
from src.interface_adapters.repositories_impl.sqlite_aluno_repository import SQLiteAlunoRepository
from src.interface_adapters.repositories_impl.sqlite_disciplina_repository import SQLiteDisciplinaRepository
from src.interface_adapters.repositories_impl.sqlite_matricula_repository import SQLiteMatriculaRepository
from src.interface_adapters.repositories_impl.sqlite_nota_repository import SQLiteNotaRepository
from src.interface_adapters.repositories_impl.sqlite_frequencia_repository import SQLiteFrequenciaRepository
from src.interface_adapters.repositories_impl.sqlite_professor_repository import SQLiteProfessorRepository
from src.interface_adapters.repositories_impl.sqlite_usuario_repository import SQLiteUsuarioRepository
from src.infrastructure.security.werkzeug_password_hasher import WerkzeugPasswordHasher

from src.application.use_cases.cadastrar_aluno import CadastrarAluno
from src.application.use_cases.cadastrar_disciplina import CadastrarDisciplina
from src.application.use_cases.matricular_aluno import MatricularAluno
from src.application.use_cases.lancar_nota import LancarNota
from src.application.use_cases.lancar_frequencia import LancarFrequencia
from src.application.use_cases.consultar_desempenho import ConsultarDesempenho
from src.application.use_cases.listar_alunos import ListarAlunos
from src.application.use_cases.listar_disciplinas import ListarDisciplinas
from src.application.use_cases.listar_matriculas import ListarMatriculas
from src.application.use_cases.cadastrar_professor import CadastrarProfessor
from src.application.use_cases.listar_professores import ListarProfessores
from src.application.use_cases.cadastrar_usuario import CadastrarUsuario
from src.application.use_cases.autenticar_usuario import AutenticarUsuario

from src.interface_adapters.presenters.desempenho_presenter import DesempenhoPresenter

from src.interface_adapters.controllers.aluno_controller import AlunoController
from src.interface_adapters.controllers.disciplina_controller import DisciplinaController
from src.interface_adapters.controllers.matricula_controller import MatriculaController
from src.interface_adapters.controllers.nota_controller import NotaController
from src.interface_adapters.controllers.frequencia_controller import FrequenciaController
from src.interface_adapters.controllers.desempenho_controller import DesempenhoController
from src.interface_adapters.controllers.professor_controller import ProfessorController
from src.interface_adapters.controllers.auth_controller import AuthController

class Container:
    def __init__(self, db_path: str = "academico.db"):
        # 1. Infraestrutura
        self.db_connection = SQLiteConnection(db_path)
        self.password_hasher = WerkzeugPasswordHasher()
        
        # 2. Repositórios
        self.aluno_repository = SQLiteAlunoRepository(self.db_connection)
        self.disciplina_repository = SQLiteDisciplinaRepository(self.db_connection)
        self.matricula_repository = SQLiteMatriculaRepository(self.db_connection)
        self.nota_repository = SQLiteNotaRepository(self.db_connection)
        self.frequencia_repository = SQLiteFrequenciaRepository(self.db_connection)
        self.professor_repository = SQLiteProfessorRepository(self.db_connection)
        self.usuario_repository = SQLiteUsuarioRepository(self.db_connection)
        
        # 3. Presenters
        self.desempenho_presenter = DesempenhoPresenter()
        
        # 4. Use Cases
        self.cadastrar_aluno_use_case = CadastrarAluno(self.aluno_repository)
        self.cadastrar_disciplina_use_case = CadastrarDisciplina(self.disciplina_repository)
        self.matricular_aluno_use_case = MatricularAluno(
            self.matricula_repository, self.aluno_repository, self.disciplina_repository
        )
        self.lancar_nota_use_case = LancarNota(self.nota_repository, self.matricula_repository)
        self.lancar_frequencia_use_case = LancarFrequencia(self.frequencia_repository, self.matricula_repository)
        self.consultar_desempenho_use_case = ConsultarDesempenho(
            self.aluno_repository,
            self.matricula_repository,
            self.nota_repository,
            self.frequencia_repository,
            self.disciplina_repository
        )
        self.listar_alunos_use_case = ListarAlunos(self.aluno_repository)
        self.listar_disciplinas_use_case = ListarDisciplinas(self.disciplina_repository)
        self.listar_matriculas_use_case = ListarMatriculas(self.matricula_repository)
        self.cadastrar_professor_use_case = CadastrarProfessor(self.professor_repository)
        self.listar_professores_use_case = ListarProfessores(self.professor_repository)
        self.cadastrar_usuario_use_case = CadastrarUsuario(self.usuario_repository, self.password_hasher)
        self.autenticar_usuario_use_case = AutenticarUsuario(self.usuario_repository, self.password_hasher)

        # 5. Controllers
        self.aluno_controller = AlunoController(self.cadastrar_aluno_use_case, self.listar_alunos_use_case)
        self.disciplina_controller = DisciplinaController(self.cadastrar_disciplina_use_case, self.listar_disciplinas_use_case)
        self.matricula_controller = MatriculaController(self.matricular_aluno_use_case, self.listar_matriculas_use_case)
        self.nota_controller = NotaController(self.lancar_nota_use_case)
        self.frequencia_controller = FrequenciaController(self.lancar_frequencia_use_case)
        self.desempenho_controller = DesempenhoController(self.consultar_desempenho_use_case, self.desempenho_presenter)
        self.professor_controller = ProfessorController(self.cadastrar_professor_use_case, self.listar_professores_use_case)
        self.auth_controller = AuthController(self.autenticar_usuario_use_case)

        self._garantir_admin_inicial()

    def _garantir_admin_inicial(self):
        if self.usuario_repository.buscar_por_login("admin") is None:
            self.cadastrar_usuario_use_case.executar("admin", "admin123", "admin")

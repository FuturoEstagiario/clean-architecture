from src.infrastructure.database.sqlite_connection import SQLiteConnection
from src.interface_adapters.repositories_impl.sqlite_aluno_repository import SQLiteAlunoRepository
from src.interface_adapters.repositories_impl.sqlite_disciplina_repository import SQLiteDisciplinaRepository
from src.interface_adapters.repositories_impl.sqlite_matricula_repository import SQLiteMatriculaRepository
from src.interface_adapters.repositories_impl.sqlite_nota_repository import SQLiteNotaRepository
from src.interface_adapters.repositories_impl.sqlite_frequencia_repository import SQLiteFrequenciaRepository

from src.application.use_cases.cadastrar_aluno import CadastrarAluno
from src.application.use_cases.cadastrar_disciplina import CadastrarDisciplina
from src.application.use_cases.matricular_aluno import MatricularAluno
from src.application.use_cases.lancar_nota import LancarNota
from src.application.use_cases.lancar_frequencia import LancarFrequencia
from src.application.use_cases.consultar_desempenho import ConsultarDesempenho

from src.interface_adapters.presenters.desempenho_presenter import DesempenhoPresenter

from src.interface_adapters.controllers.aluno_controller import AlunoController
from src.interface_adapters.controllers.disciplina_controller import DisciplinaController
from src.interface_adapters.controllers.matricula_controller import MatriculaController
from src.interface_adapters.controllers.nota_controller import NotaController
from src.interface_adapters.controllers.frequencia_controller import FrequenciaController
from src.interface_adapters.controllers.desempenho_controller import DesempenhoController

class Container:
    def __init__(self, db_path: str = "academico.db"):
        # 1. Infraestrutura
        self.db_connection = SQLiteConnection(db_path)
        
        # 2. Repositórios
        self.aluno_repository = SQLiteAlunoRepository(self.db_connection)
        self.disciplina_repository = SQLiteDisciplinaRepository(self.db_connection)
        self.matricula_repository = SQLiteMatriculaRepository(self.db_connection)
        self.nota_repository = SQLiteNotaRepository(self.db_connection)
        self.frequencia_repository = SQLiteFrequenciaRepository(self.db_connection)
        
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
        
        # 5. Controllers
        self.aluno_controller = AlunoController(self.cadastrar_aluno_use_case)
        self.disciplina_controller = DisciplinaController(self.cadastrar_disciplina_use_case)
        self.matricula_controller = MatriculaController(self.matricular_aluno_use_case)
        self.nota_controller = NotaController(self.lancar_nota_use_case)
        self.frequencia_controller = FrequenciaController(self.lancar_frequencia_use_case)
        self.desempenho_controller = DesempenhoController(self.consultar_desempenho_use_case, self.desempenho_presenter)

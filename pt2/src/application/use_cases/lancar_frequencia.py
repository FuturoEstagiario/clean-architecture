from src.domain.entities.frequencia import Frequencia
from src.application.repositories.frequencia_repository import IFrequenciaRepository
from src.application.repositories.matricula_repository import IMatriculaRepository

class LancarFrequencia:
    def __init__(self, frequencia_repository: IFrequenciaRepository, matricula_repository: IMatriculaRepository):
        self.frequencia_repository = frequencia_repository
        self.matricula_repository = matricula_repository

    def executar(self, aluno_matricula: str, disciplina_codigo: str, aulas_presente: int, aulas_total: int) -> Frequencia:
        # Validar se o aluno está matriculado
        matricula = self.matricula_repository.buscar_por_aluno_e_disciplina(aluno_matricula, disciplina_codigo)
        if matricula is None:
            raise ValueError(f"Matrícula não encontrada para o aluno {aluno_matricula} na disciplina {disciplina_codigo}.")
            
        # Instanciar a entidade Frequencia (executa validações internas)
        nova_frequencia = Frequencia(aluno_matricula, disciplina_codigo, aulas_presente, aulas_total)
        
        self.frequencia_repository.salvar(nova_frequencia)
        return nova_frequencia

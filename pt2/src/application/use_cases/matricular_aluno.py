from src.domain.entities.matricula import Matricula
from src.application.repositories.matricula_repository import IMatriculaRepository
from src.application.repositories.aluno_repository import IAlunoRepository
from src.application.repositories.disciplina_repository import IDisciplinaRepository

class MatricularAluno:
    def __init__(self, matricula_repository: IMatriculaRepository, aluno_repository: IAlunoRepository, disciplina_repository: IDisciplinaRepository):
        self.matricula_repository = matricula_repository
        self.aluno_repository = aluno_repository
        self.disciplina_repository = disciplina_repository

    def executar(self, aluno_matricula: str, disciplina_codigo: str) -> Matricula:
        aluno = self.aluno_repository.buscar_por_matricula(aluno_matricula)
        if aluno is None:
            raise ValueError(f"Aluno com matrícula {aluno_matricula} não encontrado.")
            
        disciplina = self.disciplina_repository.buscar_por_codigo(disciplina_codigo)
        if disciplina is None:
            raise ValueError(f"Disciplina com código {disciplina_codigo} não encontrada.")
            
        matricula_existente = self.matricula_repository.buscar_por_aluno_e_disciplina(aluno_matricula, disciplina_codigo)
        if matricula_existente is not None:
            raise ValueError(f"Aluno {aluno_matricula} já está matriculado na disciplina {disciplina_codigo}.")
            
        nova_matricula = Matricula(aluno_matricula, disciplina_codigo)
        self.matricula_repository.salvar(nova_matricula)
        print(f"Aluno {aluno.nome} matriculado com sucesso na disciplina {disciplina.nome}!")
        return nova_matricula

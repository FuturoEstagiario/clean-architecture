from src.domain.entities.nota import Nota
from src.application.repositories.nota_repository import INotaRepository
from src.application.repositories.matricula_repository import IMatriculaRepository

class LancarNota:
    def __init__(self, nota_repository: INotaRepository, matricula_repository: IMatriculaRepository):
        self.nota_repository = nota_repository
        self.matricula_repository = matricula_repository

    def executar(self, aluno_matricula: str, disciplina_codigo: str, valor: float, tipo_avaliacao: str) -> Nota:
        matricula = self.matricula_repository.buscar_por_aluno_e_disciplina(aluno_matricula, disciplina_codigo)
        if matricula is None:
            raise ValueError(f"Matrícula não encontrada para o aluno {aluno_matricula} na disciplina {disciplina_codigo}.")

        nova_nota = Nota(aluno_matricula, disciplina_codigo, valor, tipo_avaliacao)
        self.nota_repository.salvar(nova_nota)
        return nova_nota

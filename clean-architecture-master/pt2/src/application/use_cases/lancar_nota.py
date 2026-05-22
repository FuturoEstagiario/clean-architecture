from src.domain.entities.nota import Nota
from src.application.repositories.nota_repository import INotaRepository


class LancarNota:
    def __init__(self, repository: INotaRepository):
        self.repository = repository

    def executar(self, aluno_matricula: str, disciplina: str, valor: float) -> Nota:
        nota = Nota(aluno_matricula, disciplina, valor)
        self.repository.salvar(nota)
        return nota

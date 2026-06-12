from src.domain.entities.disciplina import Disciplina
from src.application.repositories.disciplina_repository import IDisciplinaRepository

class ListarDisciplinas:
    def __init__(self, disciplina_repository: IDisciplinaRepository):
        self.disciplina_repository = disciplina_repository

    def executar(self) -> list[Disciplina]:
        return self.disciplina_repository.listar()

from src.domain.entities.aluno import Aluno
from src.application.repositories.aluno_repository import IAlunoRepository

class ListarAlunos:
    def __init__(self, aluno_repository: IAlunoRepository):
        self.aluno_repository = aluno_repository

    def executar(self) -> list[Aluno]:
        return self.aluno_repository.listar()

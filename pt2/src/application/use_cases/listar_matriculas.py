from src.domain.entities.matricula import Matricula
from src.application.repositories.matricula_repository import IMatriculaRepository

class ListarMatriculas:
    def __init__(self, matricula_repository: IMatriculaRepository):
        self.matricula_repository = matricula_repository

    def executar(self) -> list[Matricula]:
        return self.matricula_repository.listar()

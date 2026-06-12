from src.domain.entities.professor import Professor
from src.application.repositories.professor_repository import IProfessorRepository

class ListarProfessores:
    def __init__(self, professor_repository: IProfessorRepository):
        self.professor_repository = professor_repository

    def executar(self) -> list[Professor]:
        return self.professor_repository.listar()

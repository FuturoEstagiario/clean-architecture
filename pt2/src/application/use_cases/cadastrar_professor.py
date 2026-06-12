from src.domain.entities.professor import Professor
from src.application.repositories.professor_repository import IProfessorRepository

class CadastrarProfessor:
    def __init__(self, repository: IProfessorRepository):
        self.repository = repository

    def executar(self, registro: str, nome: str):
        novo_professor = Professor(registro, nome)
        self.repository.salvar(novo_professor)

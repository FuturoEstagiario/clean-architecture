from src.domain.entities.professor import Professor
from src.application.repositories.professor_repository import IProfessorRepository

class CadastrarProfessor:
    def __init__(self, repository: IProfessorRepository):
        self.repository = repository

    def executar(self, matricula_funcional: str, nome: str, email: str) -> Professor:
        if self.repository.buscar_por_matricula(matricula_funcional) is not None:
            raise ValueError(f"Professor com matrícula '{matricula_funcional}' já cadastrado.")
        professor = Professor(matricula_funcional, nome, email)
        self.repository.salvar(professor)
        return professor

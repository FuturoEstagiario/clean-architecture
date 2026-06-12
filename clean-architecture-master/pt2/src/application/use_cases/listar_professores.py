from typing import List
from src.application.repositories.professor_repository import IProfessorRepository
from src.application.dtos.professor_dto import ProfessorResumoDTO

class ListarProfessores:
    def __init__(self, repository: IProfessorRepository):
        self.repository = repository

    def executar(self) -> List[ProfessorResumoDTO]:
        professores = self.repository.listar_todos()
        return [ProfessorResumoDTO(p.matricula_funcional, p.nome, p.email) for p in professores]

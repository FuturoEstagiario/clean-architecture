from typing import List
from src.application.repositories.aluno_repository import IAlunoRepository
from src.application.dtos.aluno_dto import AlunoResumoDTO

class ListarAlunos:
    def __init__(self, repository: IAlunoRepository):
        self.repository = repository

    def executar(self) -> List[AlunoResumoDTO]:
        alunos = self.repository.listar_todos()
        return [AlunoResumoDTO(a.matricula, a.nome, a.situacao) for a in alunos]

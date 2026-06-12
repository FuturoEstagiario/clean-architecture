from typing import List
from src.application.repositories.aluno_repository import IAlunoRepository
from src.domain.entities.aluno import Aluno

class MemoryAlunoRepository(IAlunoRepository):
    def __init__(self):
        self._alunos: dict[str, Aluno] = {}

    def salvar(self, aluno: Aluno) -> None:
        self._alunos[aluno.matricula] = aluno

    def buscar_por_matricula(self, matricula: str) -> Aluno | None:
        return self._alunos.get(matricula)

    def listar_todos(self) -> List[Aluno]:
        return list(self._alunos.values())

    def atualizar_situacao(self, matricula: str, nova_situacao: str) -> None:
        aluno = self._alunos.get(matricula)
        if aluno:
            aluno.situacao = nova_situacao

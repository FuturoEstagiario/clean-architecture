from src.application.repositories.aluno_repository import IAlunoRepository
from src.domain.entities.aluno import Aluno

class MemoryAlunoRepository(IAlunoRepository):
    def __init__(self):
        self.alunos = []

    def salvar(self, aluno: Aluno) -> None:
        self.alunos.append(aluno)
        print(f"[Log] Aluno salvo em memória. Total: {len(self.alunos)}")

    def buscar_por_matricula(self, matricula: str) -> Aluno | None:
        return next((a for a in self.alunos if a.matricula == matricula), None)

    def listar(self) -> list[Aluno]:
        return list(self.alunos)
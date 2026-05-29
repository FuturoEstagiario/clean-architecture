from src.application.repositories.aluno_repository import IAlunoRepository
from src.domain.entities.aluno import Aluno

class MemoryAlunoRepository(IAlunoRepository):
    def __init__(self):
        self.alunos = []

    def salvar(self, aluno: Aluno) -> None:
        self.alunos.append(aluno)
        print(f"[Log] Aluno salvo em memória. Total: {len(self.alunos)}")
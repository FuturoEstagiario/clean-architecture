from src.domain.entities.aluno import Aluno
from src.application.repositories.aluno_repository import IAlunoRepository

class CadastrarAluno:
    def __init__(self, repository: IAlunoRepository):
        self.repository = repository

    def executar(self, matricula: str, nome: str):
        novo_aluno = Aluno(matricula, nome)
        self.repository.salvar(novo_aluno)
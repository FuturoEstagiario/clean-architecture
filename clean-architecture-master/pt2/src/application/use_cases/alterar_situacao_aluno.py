from src.domain.entities.aluno import Aluno
from src.application.repositories.aluno_repository import IAlunoRepository

class AlterarSituacaoAluno:
    def __init__(self, repository: IAlunoRepository):
        self.repository = repository

    def executar(self, matricula: str, nova_situacao: str) -> Aluno:
        aluno = self.repository.buscar_por_matricula(matricula)
        if aluno is None:
            raise ValueError(f"Aluno com matrícula {matricula} não encontrado.")
        aluno.alterar_situacao(nova_situacao)
        self.repository.atualizar_situacao(matricula, nova_situacao)
        return aluno

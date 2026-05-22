from typing import Dict, Any
from src.application.repositories.nota_repository import INotaRepository
from src.application.repositories.aluno_repository import IAlunoRepository

MEDIA_MINIMA_APROVACAO = 7.0


class ConsultarDesempenho:
    def __init__(self, nota_repository: INotaRepository, aluno_repository: IAlunoRepository):
        self.nota_repository = nota_repository
        self.aluno_repository = aluno_repository

    def executar(self, matricula: str) -> Dict[str, Any]:
        aluno = self.aluno_repository.buscar_por_matricula(matricula)
        notas = self.nota_repository.buscar_por_matricula(matricula)

        nome = aluno.nome if aluno else "Aluno não encontrado"

        if not notas:
            return {
                "matricula": matricula,
                "nome": nome,
                "notas": [],
                "media": None,
                "situacao": "Sem notas registradas",
            }

        media = sum(n.valor for n in notas) / len(notas)
        situacao = "Aprovado" if media >= MEDIA_MINIMA_APROVACAO else "Reprovado"

        return {
            "matricula": matricula,
            "nome": nome,
            "notas": [{"disciplina": n.disciplina, "valor": n.valor} for n in notas],
            "media": round(media, 2),
            "situacao": situacao,
        }

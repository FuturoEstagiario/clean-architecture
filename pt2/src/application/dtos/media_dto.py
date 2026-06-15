from typing import List

class MediaDTO:
    def __init__(
        self,
        aluno_matricula: str,
        aluno_nome: str,
        disciplina_codigo: str,
        disciplina_nome: str,
        notas: List[float],
        media: float,
        status: str,
    ):
        self.aluno_matricula = aluno_matricula
        self.aluno_nome = aluno_nome
        self.disciplina_codigo = disciplina_codigo
        self.disciplina_nome = disciplina_nome
        self.notas = notas
        self.media = media
        self.status = status

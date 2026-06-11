from typing import List

class DisciplinaDesempenhoDTO:
    def __init__(self, disciplina_codigo: str, disciplina_nome: str, notas: List[float], media: float, aulas_presente: int, aulas_total: int, percentual_frequencia: float):
        self.disciplina_codigo = disciplina_codigo
        self.disciplina_nome = disciplina_nome
        self.notas = notas
        self.media = media
        self.aulas_presente = aulas_presente
        self.aulas_total = aulas_total
        self.percentual_frequencia = percentual_frequencia

class DesempenhoDTO:
    def __init__(self, aluno_matricula: str, aluno_nome: str, aluno_situacao: str, disciplinas: List[DisciplinaDesempenhoDTO]):
        self.aluno_matricula = aluno_matricula
        self.aluno_nome = aluno_nome
        self.aluno_situacao = aluno_situacao
        self.disciplinas = disciplinas

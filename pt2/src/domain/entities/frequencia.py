class Frequencia:
    def __init__(self, aluno_matricula: str, disciplina_codigo: str, aulas_presente: int, aulas_total: int):
        if aulas_total <= 0:
            raise ValueError("O total de aulas deve ser maior que zero.")
        if aulas_presente < 0:
            raise ValueError("O número de presenças não pode ser negativo.")
        if aulas_presente > aulas_total:
            raise ValueError("O número de presenças não pode ser maior que o total de aulas.")
            
        self.aluno_matricula = aluno_matricula
        self.disciplina_codigo = disciplina_codigo
        self.aulas_presente = aulas_presente
        self.aulas_total = aulas_total
        
    @property
    def percentual(self) -> float:
        return (self.aulas_presente / self.aulas_total) * 100.0

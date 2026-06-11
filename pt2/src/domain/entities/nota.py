class Nota:
    def __init__(self, aluno_matricula: str, disciplina_codigo: str, valor: float, tipo_avaliacao: str):
        if not (0.0 <= valor <= 10.0):
            raise ValueError("A nota deve estar entre 0.0 e 10.0.")
        self.aluno_matricula = aluno_matricula
        self.disciplina_codigo = disciplina_codigo
        self.valor = valor
        self.tipo_avaliacao = tipo_avaliacao

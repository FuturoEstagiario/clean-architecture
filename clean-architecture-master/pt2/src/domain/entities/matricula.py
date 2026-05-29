class Matricula:
    def __init__(self, aluno_matricula: str, disciplina_codigo: str):
        if not aluno_matricula:
            raise ValueError("A matrícula do aluno é obrigatória.")
        if not disciplina_codigo:
            raise ValueError("O código da disciplina é obrigatório.")
        self.aluno_matricula = aluno_matricula
        self.disciplina_codigo = disciplina_codigo

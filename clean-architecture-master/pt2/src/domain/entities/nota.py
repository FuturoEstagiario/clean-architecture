class NotaValorInvalidoError(ValueError):
    pass


class Nota:
    def __init__(self, aluno_matricula: str, disciplina: str, valor: float):
        if not (0 <= valor <= 10):
            raise NotaValorInvalidoError(
                f"Valor {valor} inválido. A nota deve estar entre 0 e 10."
            )
        self.aluno_matricula = aluno_matricula
        self.disciplina = disciplina
        self.valor = valor

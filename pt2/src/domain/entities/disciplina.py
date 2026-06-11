class Disciplina:
    def __init__(self, codigo: str, nome: str, carga_horaria: int):
        if carga_horaria <= 0:
            raise ValueError("A carga horária deve ser maior que zero.")
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria

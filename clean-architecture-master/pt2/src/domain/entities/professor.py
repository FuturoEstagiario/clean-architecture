class Professor:
    def __init__(self, matricula_funcional: str, nome: str, email: str):
        if not matricula_funcional:
            raise ValueError("A matrícula funcional é obrigatória.")
        if not nome:
            raise ValueError("O nome do professor é obrigatório.")
        self.matricula_funcional = matricula_funcional
        self.nome = nome
        self.email = email

class Professor:
    def __init__(self, registro: str, nome: str):
        if not registro or not registro.strip():
            raise ValueError("O registro do professor é obrigatório.")
        if not nome or not nome.strip():
            raise ValueError("O nome do professor é obrigatório.")
        self.registro = registro
        self.nome = nome

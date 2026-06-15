class Aluno:
    def __init__(self, matricula: str, nome: str):
        if not matricula or not matricula.strip():
            raise ValueError("A matrícula do aluno é obrigatória.")
        if not nome or not nome.strip():
            raise ValueError("O nome do aluno é obrigatório.")
        self.matricula = matricula
        self.nome = nome
        self.situacao = "Ativo"
class Aluno:
    def __init__(self, matricula: str, nome: str):
        if not matricula or not matricula.strip():
            raise ValueError("A matrícula do aluno é obrigatória.")
        if not nome or not nome.strip():
            raise ValueError("O nome do aluno é obrigatório.")
        self.matricula = matricula
        self.nome = nome
        self.situacao = "Ativo"

    def alterar_situacao(self, nova_situacao: str) -> None:
        if not nova_situacao or not nova_situacao.strip():
            raise ValueError("A situação do aluno é obrigatória.")
        self.situacao = nova_situacao
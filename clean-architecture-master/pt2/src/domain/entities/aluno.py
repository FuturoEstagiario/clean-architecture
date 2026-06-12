class Aluno:
    SITUACOES_VALIDAS = {"Ativo", "Trancado", "Formado"}

    def __init__(self, matricula: str, nome: str):
        self.matricula = matricula
        self.nome = nome
        self.situacao = "Ativo"

    def alterar_situacao(self, nova_situacao: str) -> None:
        if nova_situacao not in self.SITUACOES_VALIDAS:
            validas = ", ".join(sorted(self.SITUACOES_VALIDAS))
            raise ValueError(f"Situação inválida. Valores permitidos: {validas}.")
        self.situacao = nova_situacao
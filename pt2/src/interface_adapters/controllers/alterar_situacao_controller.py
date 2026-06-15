from src.application.use_cases.alterar_situacao_aluno import AlterarSituacaoAluno

class AlterarSituacaoController:
    def __init__(self, use_case: AlterarSituacaoAluno):
        self.use_case = use_case

    def alterar(self, matricula: str, nova_situacao: str) -> dict:
        try:
            aluno = self.use_case.executar(matricula, nova_situacao)
            return {
                "status": "sucesso",
                "mensagem": f"Situação do aluno '{aluno.nome}' atualizada para '{aluno.situacao}'.",
            }
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

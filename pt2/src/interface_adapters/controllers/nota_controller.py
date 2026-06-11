from src.application.use_cases.lancar_nota import LancarNota

class NotaController:
    def __init__(self, lancar_nota_use_case: LancarNota):
        self.use_case = lancar_nota_use_case

    def lancar(self, aluno_matricula: str, disciplina_codigo: str, valor: float, tipo_avaliacao: str) -> dict:
        try:
            self.use_case.executar(aluno_matricula, disciplina_codigo, valor, tipo_avaliacao)
            return {"status": "sucesso", "mensagem": f"Nota {valor:.1f} lançada com sucesso."}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

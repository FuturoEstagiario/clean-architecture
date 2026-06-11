from src.application.use_cases.lancar_frequencia import LancarFrequencia

class FrequenciaController:
    def __init__(self, lancar_frequencia_use_case: LancarFrequencia):
        self.use_case = lancar_frequencia_use_case

    def lancar(self, aluno_matricula: str, disciplina_codigo: str, aulas_presente: int, aulas_total: int) -> dict:
        try:
            self.use_case.executar(aluno_matricula, disciplina_codigo, aulas_presente, aulas_total)
            return {"status": "sucesso", "mensagem": "Frequência lançada com sucesso."}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

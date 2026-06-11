from src.application.use_cases.matricular_aluno import MatricularAluno

class MatriculaController:
    def __init__(self, matricular_aluno_use_case: MatricularAluno):
        self.use_case = matricular_aluno_use_case

    def matricular(self, aluno_matricula: str, disciplina_codigo: str) -> dict:
        try:
            self.use_case.executar(aluno_matricula, disciplina_codigo)
            return {"status": "sucesso", "mensagem": f"Aluno '{aluno_matricula}' matriculado na disciplina '{disciplina_codigo}'."}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

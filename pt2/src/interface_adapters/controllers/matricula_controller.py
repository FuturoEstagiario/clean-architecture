from src.application.use_cases.matricular_aluno import MatricularAluno
from src.application.use_cases.listar_matriculas import ListarMatriculas

class MatriculaController:
    def __init__(self, matricular_aluno_use_case: MatricularAluno, listar_matriculas_use_case: ListarMatriculas):
        self.use_case = matricular_aluno_use_case
        self.listar_use_case = listar_matriculas_use_case

    def matricular(self, aluno_matricula: str, disciplina_codigo: str) -> dict:
        try:
            self.use_case.executar(aluno_matricula, disciplina_codigo)
            return {"status": "sucesso", "mensagem": f"Aluno '{aluno_matricula}' matriculado na disciplina '{disciplina_codigo}'."}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

    def listar(self) -> dict:
        matriculas = self.listar_use_case.executar()
        return {
            "status": "sucesso",
            "dados": [{"aluno_matricula": m.aluno_matricula, "disciplina_codigo": m.disciplina_codigo} for m in matriculas]
        }

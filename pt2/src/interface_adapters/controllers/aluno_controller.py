from src.application.use_cases.cadastrar_aluno import CadastrarAluno
from src.application.use_cases.listar_alunos import ListarAlunos

class AlunoController:
    def __init__(self, cadastrar_aluno_use_case: CadastrarAluno, listar_alunos_use_case: ListarAlunos):
        self.use_case = cadastrar_aluno_use_case
        self.listar_use_case = listar_alunos_use_case

    def cadastrar(self, matricula: str, nome: str) -> dict:
        try:
            self.use_case.executar(matricula, nome)
            return {"status": "sucesso", "mensagem": f"Aluno '{nome}' cadastrado com sucesso."}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

    def listar(self) -> dict:
        alunos = self.listar_use_case.executar()
        return {
            "status": "sucesso",
            "dados": [{"matricula": a.matricula, "nome": a.nome, "situacao": a.situacao} for a in alunos]
        }

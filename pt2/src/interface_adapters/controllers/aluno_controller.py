from src.application.use_cases.cadastrar_aluno import CadastrarAluno

class AlunoController:
    def __init__(self, cadastrar_aluno_use_case: CadastrarAluno):
        self.use_case = cadastrar_aluno_use_case

    def cadastrar(self, matricula: str, nome: str) -> dict:
        try:
            self.use_case.executar(matricula, nome)
            return {"status": "sucesso", "mensagem": f"Aluno '{nome}' cadastrado com sucesso."}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

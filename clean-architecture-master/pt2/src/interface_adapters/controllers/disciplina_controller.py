from src.application.use_cases.cadastrar_disciplina import CadastrarDisciplina

class DisciplinaController:
    def __init__(self, cadastrar_disciplina_use_case: CadastrarDisciplina):
        self.use_case = cadastrar_disciplina_use_case

    def cadastrar(self, codigo: str, nome: str, carga_horaria: int) -> dict:
        try:
            self.use_case.executar(codigo, nome, carga_horaria)
            return {"status": "sucesso", "mensagem": f"Disciplina '{nome}' cadastrada com sucesso."}
        except ValueError as e:
            return {"status": "erro", "mensagem": str(e)}

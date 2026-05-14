from src.interface_adapters.repositories_impl.memory_aluno_repository import MemoryAlunoRepository
from src.application.use_cases.cadastrar_aluno import CadastrarAluno

def run():
    repositorio = MemoryAlunoRepository()
    caso_de_uso = CadastrarAluno(repositorio)

    nome_input = "Carlos"
    matricula_input = "2026001"
    
    caso_de_uso.executar(matricula_input, nome_input)

if __name__ == "__main__":
    run()
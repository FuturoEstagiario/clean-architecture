from src.interface_adapters.repositories_impl.memory_aluno_repository import MemoryAlunoRepository
from src.application.use_cases.cadastrar_aluno import CadastrarAluno

def main():
    print("--- Sistema de Gestão Académica (Sprint 1) ---")
    
    repositorio = MemoryAlunoRepository()
    

    caso_de_uso = CadastrarAluno(repositorio)

    print("\n[Interface] Iniciando cadastro de aluno...")
    nome_exemplo = "Carlos"
    matricula_exemplo = "2026001"
    
    caso_de_uso.executar(matricula_exemplo, nome_exemplo)
    
    print("\n--- Verificando Registros no Repositório ---")
    for aluno in repositorio.alunos:
        print(f"Matrícula: {aluno.matricula} | Nome: {aluno.nome} | Situação: {aluno.situacao}")
    
    print("\n--- Fluxo finalizado com sucesso ---")

if __name__ == "__main__":
    main()
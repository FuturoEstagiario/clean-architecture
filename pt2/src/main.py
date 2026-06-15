import os
from src.infrastructure.di.container import Container

def main():
    print("--- Sistema de Gestão Acadêmica (Sprint 3) ---")
    
    # Usar um banco de dados de demonstração
    db_name = "demo_academico.db"
    
    # Remover banco de dados de demonstração antigo para rodar limpo
    if os.path.exists(db_name):
        try:
            os.remove(db_name)
        except PermissionError:
            pass

    # Inicializar o container (Composition Root)
    container = Container(db_name)
    
    print("\n1. --- Cadastrando Alunos ---")
    print(container.aluno_controller.cadastrar("2026001", "Carlos Eduardo"))
    print(container.aluno_controller.cadastrar("2026002", "Bruno Rodrigues"))
    
    print("\n2. --- Cadastrando Disciplinas (Novas Funcionalidades Sprint 3) ---")
    print(container.disciplina_controller.cadastrar("ARQ01", "Arquitetura de Software", 60))
    print(container.disciplina_controller.cadastrar("CALC01", "Cálculo Diferencial I", 80))
    
    # Testar regra de negócio de carga horária inválida
    print("\n   [Teste de Regra] Tentando cadastrar disciplina com carga horária inválida:")
    res_disc = container.disciplina_controller.cadastrar("TEST01", "Carga Horária Zero", 0)
    print(f"   Resultado: {res_disc}")

    print("\n3. --- Matriculando Alunos (Novas Funcionalidades Sprint 3) ---")
    print(container.matricula_controller.matricular("2026001", "ARQ01"))
    print(container.matricula_controller.matricular("2026001", "CALC01"))
    print(container.matricula_controller.matricular("2026002", "ARQ01"))
    
    print("\n4. --- Lançando Notas (Sprint 2 - Corrigido) ---")
    print(container.nota_controller.lancar("2026001", "ARQ01", 9.5, "Trabalho 1 (TP1)"))
    print(container.nota_controller.lancar("2026001", "ARQ01", 8.0, "Trabalho 2 (TP2)"))
    print(container.nota_controller.lancar("2026001", "CALC01", 7.0, "Prova 1"))
    
    # Testar regra de negócio de notas inválidas (deve falhar de forma controlada)
    print("\n   [Teste de Regra] Tentando lançar nota 11.5 (deve falhar):")
    res_nota = container.nota_controller.lancar("2026001", "ARQ01", 11.5, "Final")
    print(f"   Resultado: {res_nota}")
    
    print("\n5. --- Lançando Frequência (Novas Funcionalidades Sprint 3) ---")
    print(container.frequencia_controller.lancar("2026001", "ARQ01", 18, 20))
    print(container.frequencia_controller.lancar("2026001", "CALC01", 15, 20))
    
    # Testar regra de negócio de frequência inválida (deve falhar)
    print("\n   [Teste de Regra] Tentando lançar presenças maiores que o total de aulas:")
    res_freq = container.frequencia_controller.lancar("2026001", "ARQ01", 25, 20)
    print(f"   Resultado: {res_freq}")

    print("\n6. --- Consultando Desempenho com DTO e Presenter (Sprint 2 - Corrigido) ---")
    # Consulta usando a formatação de console do Presenter
    boletim_console = container.desempenho_controller.consultar_console("2026001")
    print(boletim_console)
    
    # Exibir a resposta JSON formatada
    boletim_json = container.desempenho_controller.consultar_json("2026001")
    print("\nRepresentação em formato JSON/Dict:")
    import json
    print(json.dumps(boletim_json, indent=2, ensure_ascii=False))

    print("\n--- Demonstração finalizada com sucesso ---")

if __name__ == "__main__":
    main()
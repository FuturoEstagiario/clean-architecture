from src.application.dtos.desempenho_dto import DesempenhoDTO

class DesempenhoPresenter:
    def apresentar_json(self, dto: DesempenhoDTO) -> dict:
        """Formata o DTO para uma resposta no formato dicionário/JSON."""
        return {
            "aluno": {
                "matricula": dto.aluno_matricula,
                "nome": dto.aluno_nome,
                "situacao": dto.aluno_situacao
            },
            "desempenho_disciplinas": [
                {
                    "codigo": d.disciplina_codigo,
                    "nome": d.disciplina_nome,
                    "notas": d.notas,
                    "media_final": round(d.media, 2),
                    "frequencia": {
                        "aulas_presente": d.aulas_presente,
                        "aulas_total": d.aulas_total,
                        "percentual": f"{d.percentual_frequencia:.1f}%"
                    }
                }
                for d in dto.disciplinas
            ]
        }

    def apresentar_console(self, dto: DesempenhoDTO) -> str:
        """Formata o DTO para exibição em modo texto no terminal/console."""
        linhas = [
            f"==================================================",
            f" BOLETIM ACADÊMICO: {dto.aluno_nome} ({dto.aluno_situacao})",
            f" Matrícula: {dto.aluno_matricula}",
            f"=================================================="
        ]
        
        if not dto.disciplinas:
            linhas.append(" Nenhuma disciplina matriculada.")
        else:
            for d in dto.disciplinas:
                linhas.append(f" Disciplina: {d.disciplina_nome} ({d.disciplina_codigo})")
                notas_str = ", ".join(f"{val:.1f}" for val in d.notas) if d.notas else "Sem notas"
                linhas.append(f"   Notas: [{notas_str}]")
                linhas.append(f"   Média Final: {d.media:.2f}")
                linhas.append(f"   Frequência: {d.aulas_presente}/{d.aulas_total} aulas ({d.percentual_frequencia:.1f}%)")
                linhas.append(f"--------------------------------------------------")
                
        return "\n".join(linhas)

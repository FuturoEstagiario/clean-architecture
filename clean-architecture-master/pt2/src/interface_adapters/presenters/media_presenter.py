from src.application.dtos.media_dto import MediaDTO

class MediaPresenter:
    def apresentar(self, dto: MediaDTO) -> dict:
        return {
            "aluno": {"matricula": dto.aluno_matricula, "nome": dto.aluno_nome},
            "disciplina": {"codigo": dto.disciplina_codigo, "nome": dto.disciplina_nome},
            "notas": dto.notas,
            "media": round(dto.media, 2),
            "media_minima": 6.0,
            "status": dto.status,
        }

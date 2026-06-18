from typing import List


class CriterioAprovacao:
    MEDIA_MINIMA = 6.0
    FREQUENCIA_MINIMA = 75.0

    @staticmethod
    def calcular_media(valores: List[float]) -> float:
        if not valores:
            return 0.0
        return sum(valores) / len(valores)

    @classmethod
    def aprovado_por_nota(cls, media: float) -> bool:
        return media >= cls.MEDIA_MINIMA

    @classmethod
    def aprovado_por_frequencia(cls, percentual: float) -> bool:
        return percentual >= cls.FREQUENCIA_MINIMA

    @classmethod
    def situacao_nota(cls, media: float) -> str:
        return "Aprovado por Nota" if cls.aprovado_por_nota(media) else "Reprovado por Nota"

    @classmethod
    def situacao_final(cls, media: float, percentual_frequencia: float) -> str:
        aprovado_nota = cls.aprovado_por_nota(media)
        aprovado_freq = cls.aprovado_por_frequencia(percentual_frequencia)
        if aprovado_nota and aprovado_freq:
            return "Aprovado"
        if not aprovado_nota and not aprovado_freq:
            return "Reprovado por Nota e Frequência"
        if not aprovado_nota:
            return "Reprovado por Nota"
        return "Reprovado por Frequência"

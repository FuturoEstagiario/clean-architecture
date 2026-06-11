from src.domain.entities.frequencia import Frequencia
from src.application.repositories.frequencia_repository import IFrequenciaRepository
from src.infrastructure.database.sqlite_connection import SQLiteConnection

class SQLiteFrequenciaRepository(IFrequenciaRepository):
    def __init__(self, connection_manager: SQLiteConnection):
        self.connection_manager = connection_manager

    def salvar(self, frequencia: Frequencia) -> None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO frequencias (aluno_matricula, disciplina_codigo, aulas_presente, aulas_total) VALUES (?, ?, ?, ?)",
            (frequencia.aluno_matricula, frequencia.disciplina_codigo, frequencia.aulas_presente, frequencia.aulas_total)
        )
        conn.commit()
        conn.close()

    def buscar_por_aluno(self, aluno_matricula: str) -> list[Frequencia]:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT aluno_matricula, disciplina_codigo, aulas_presente, aulas_total FROM frequencias WHERE aluno_matricula = ?",
            (aluno_matricula,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [Frequencia(r["aluno_matricula"], r["disciplina_codigo"], r["aulas_presente"], r["aulas_total"]) for r in rows]

    def buscar_por_aluno_e_disciplina(self, aluno_matricula: str, disciplina_codigo: str) -> Frequencia | None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT aluno_matricula, disciplina_codigo, aulas_presente, aulas_total FROM frequencias WHERE aluno_matricula = ? AND disciplina_codigo = ?",
            (aluno_matricula, disciplina_codigo)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Frequencia(row["aluno_matricula"], row["disciplina_codigo"], row["aulas_presente"], row["aulas_total"])
        return None

from src.domain.entities.professor import Professor
from src.application.repositories.professor_repository import IProfessorRepository
from src.infrastructure.database.sqlite_connection import SQLiteConnection

class SQLiteProfessorRepository(IProfessorRepository):
    def __init__(self, connection_manager: SQLiteConnection):
        self.connection_manager = connection_manager

    def salvar(self, professor: Professor) -> None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO professores (registro, nome) VALUES (?, ?)",
            (professor.registro, professor.nome)
        )
        conn.commit()
        conn.close()

    def buscar_por_registro(self, registro: str) -> Professor | None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT registro, nome FROM professores WHERE registro = ?", (registro,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Professor(row["registro"], row["nome"])
        return None

    def listar(self) -> list[Professor]:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT registro, nome FROM professores ORDER BY nome")
        rows = cursor.fetchall()
        conn.close()

        return [Professor(r["registro"], r["nome"]) for r in rows]

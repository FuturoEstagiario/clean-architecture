from src.domain.entities.disciplina import Disciplina
from src.application.repositories.disciplina_repository import IDisciplinaRepository
from src.infrastructure.database.sqlite_connection import SQLiteConnection

class SQLiteDisciplinaRepository(IDisciplinaRepository):
    def __init__(self, connection_manager: SQLiteConnection):
        self.connection_manager = connection_manager

    def salvar(self, disciplina: Disciplina) -> None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO disciplinas (codigo, nome, carga_horaria) VALUES (?, ?, ?)",
            (disciplina.codigo, disciplina.nome, disciplina.carga_horaria)
        )
        conn.commit()
        conn.close()

    def buscar_por_codigo(self, codigo: str) -> Disciplina | None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo, nome, carga_horaria FROM disciplinas WHERE codigo = ?", (codigo,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Disciplina(row["codigo"], row["nome"], row["carga_horaria"])
        return None

    def listar(self) -> list[Disciplina]:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo, nome, carga_horaria FROM disciplinas ORDER BY nome")
        rows = cursor.fetchall()
        conn.close()

        return [Disciplina(r["codigo"], r["nome"], r["carga_horaria"]) for r in rows]

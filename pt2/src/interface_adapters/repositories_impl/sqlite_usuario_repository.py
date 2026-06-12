from src.domain.entities.usuario import Usuario
from src.application.repositories.usuario_repository import IUsuarioRepository
from src.infrastructure.database.sqlite_connection import SQLiteConnection

class SQLiteUsuarioRepository(IUsuarioRepository):
    def __init__(self, connection_manager: SQLiteConnection):
        self.connection_manager = connection_manager

    def salvar(self, usuario: Usuario) -> None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO usuarios (login, senha_hash, perfil) VALUES (?, ?, ?)",
            (usuario.login, usuario.senha_hash, usuario.perfil)
        )
        conn.commit()
        conn.close()

    def buscar_por_login(self, login: str) -> Usuario | None:
        conn = self.connection_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT login, senha_hash, perfil FROM usuarios WHERE login = ?", (login,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Usuario(row["login"], row["senha_hash"], row["perfil"])
        return None

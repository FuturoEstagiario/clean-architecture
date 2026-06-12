class Usuario:
    PERFIS = ("aluno", "professor", "admin")

    def __init__(self, login: str, senha_hash: str, perfil: str):
        if not login or not login.strip():
            raise ValueError("O login é obrigatório.")
        if not senha_hash:
            raise ValueError("A senha é obrigatória.")
        if perfil not in self.PERFIS:
            raise ValueError("Perfil inválido. Use: aluno, professor ou admin.")
        self.login = login
        self.senha_hash = senha_hash
        self.perfil = perfil

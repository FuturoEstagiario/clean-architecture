from flask import Flask, request, jsonify
from src.infrastructure.di.container import Container

app = Flask(__name__)
container = Container()

@app.route("/", methods=["GET"])
def index():
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Gestão Acadêmica — API</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --bg: #0f1117; --surface: #1a1d27; --surface2: #22263a;
            --border: #2e3350; --accent: #6c63ff; --accent2: #00d4aa;
            --danger: #ff6b6b; --warn: #ffa94d;
            --text: #e8eaf0; --muted: #8b92b3;
        }
        body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
        header {
            background: linear-gradient(135deg, #1a1d27 0%, #16213e 100%);
            border-bottom: 1px solid var(--border);
            padding: 1.5rem 2rem;
            display: flex; align-items: center; gap: 1rem;
        }
        header .logo { font-size: 1.6rem; font-weight: 700; background: linear-gradient(90deg, var(--accent), var(--accent2)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        header .subtitle { color: var(--muted); font-size: 0.85rem; }
        .badge { background: var(--accent2); color: #000; font-size: 0.65rem; font-weight: 700; padding: 2px 8px; border-radius: 20px; letter-spacing: .5px; }

        main { max-width: 1100px; margin: 0 auto; padding: 2rem; }
        h2 { font-size: 1rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin: 2rem 0 1rem; }

        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }
        .card {
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 12px; padding: 1.25rem; transition: border-color .2s, transform .2s;
        }
        .card:hover { border-color: var(--accent); transform: translateY(-2px); }
        .card-header { display: flex; align-items: center; gap: .75rem; margin-bottom: 1rem; }
        .method {
            font-size: 0.65rem; font-weight: 700; padding: 3px 10px; border-radius: 6px;
            letter-spacing: .5px; white-space: nowrap;
        }
        .POST { background: rgba(108,99,255,.2); color: var(--accent); border: 1px solid var(--accent); }
        .GET  { background: rgba(0,212,170,.2); color: var(--accent2); border: 1px solid var(--accent2); }
        .endpoint { font-family: monospace; font-size: 0.9rem; color: var(--text); }
        .desc { font-size: 0.82rem; color: var(--muted); margin-bottom: 1rem; line-height: 1.5; }

        label { display: block; font-size: 0.75rem; color: var(--muted); margin-bottom: .3rem; font-weight: 500; }
        input {
            width: 100%; background: var(--surface2); border: 1px solid var(--border);
            color: var(--text); border-radius: 8px; padding: .5rem .75rem; font-size: 0.85rem;
            margin-bottom: .6rem; outline: none; transition: border-color .2s;
            font-family: 'Inter', sans-serif;
        }
        input:focus { border-color: var(--accent); }
        button {
            width: 100%; padding: .55rem; border-radius: 8px; border: none;
            font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: opacity .2s;
        }
        button:hover { opacity: .85; }
        .btn-post { background: var(--accent); color: #fff; }
        .btn-get  { background: var(--accent2); color: #000; }

        .result {
            margin-top: .75rem; background: var(--surface2); border: 1px solid var(--border);
            border-radius: 8px; padding: .75rem; font-family: monospace; font-size: 0.75rem;
            white-space: pre-wrap; word-break: break-all; max-height: 180px; overflow-y: auto;
            display: none; color: var(--text);
        }
        .result.ok   { border-color: var(--accent2); }
        .result.err  { border-color: var(--danger); }

        .rule { background: rgba(255,169,77,.07); border: 1px solid rgba(255,169,77,.25); border-radius: 8px; padding: .6rem .9rem; margin-bottom: .75rem; font-size: 0.78rem; color: var(--warn); }
        footer { text-align: center; padding: 2rem; color: var(--muted); font-size: .75rem; border-top: 1px solid var(--border); margin-top: 2rem; }
    </style>
</head>
<body>
<header>
    <div>
        <div class="logo">&#127979; SGA — Sprint 3</div>
        <div class="subtitle">Sistema de Gestão Acadêmica &nbsp;<span class="badge">ONLINE</span></div>
    </div>
</header>
<main>
    <h2>Funcionalidades</h2>
    <div class="grid">

        <!-- Cadastrar Aluno -->
        <div class="card">
            <div class="card-header">
                <span class="method POST">POST</span>
                <span class="endpoint">/alunos</span>
            </div>
            <p class="desc">Cadastra um novo aluno no sistema.</p>
            <label>Matrícula</label><input id="a_mat" placeholder="ex: 2026001">
            <label>Nome</label><input id="a_nom" placeholder="ex: Carlos Eduardo">
            <button class="btn-post" onclick="post('/alunos',{matricula:v('a_mat'),nome:v('a_nom')},'r_aluno')">Cadastrar Aluno</button>
            <div class="result" id="r_aluno"></div>
        </div>

        <!-- Cadastrar Disciplina -->
        <div class="card">
            <div class="card-header">
                <span class="method POST">POST</span>
                <span class="endpoint">/disciplinas</span>
            </div>
            <p class="desc">Cadastra uma disciplina.</p>
            <div class="rule">⚠ Carga horária deve ser &gt; 0.</div>
            <label>Código</label><input id="d_cod" placeholder="ex: ARQ01">
            <label>Nome</label><input id="d_nom" placeholder="ex: Arquitetura de Software">
            <label>Carga Horária (h)</label><input id="d_ch" type="number" placeholder="ex: 60">
            <button class="btn-post" onclick="post('/disciplinas',{codigo:v('d_cod'),nome:v('d_nom'),carga_horaria:parseInt(v('d_ch'))},'r_disc')">Cadastrar Disciplina</button>
            <div class="result" id="r_disc"></div>
        </div>

        <!-- Matricular Aluno -->
        <div class="card">
            <div class="card-header">
                <span class="method POST">POST</span>
                <span class="endpoint">/matriculas</span>
            </div>
            <p class="desc">Matricula um aluno em uma disciplina. Valida existência e bloqueia duplicatas.</p>
            <label>Matrícula do Aluno</label><input id="m_alu" placeholder="ex: 2026001">
            <label>Código da Disciplina</label><input id="m_dis" placeholder="ex: ARQ01">
            <button class="btn-post" onclick="post('/matriculas',{aluno_matricula:v('m_alu'),disciplina_codigo:v('m_dis')},'r_mat')">Matricular</button>
            <div class="result" id="r_mat"></div>
        </div>

        <!-- Lançar Nota -->
        <div class="card">
            <div class="card-header">
                <span class="method POST">POST</span>
                <span class="endpoint">/notas</span>
            </div>
            <p class="desc">Lança nota de um aluno em uma disciplina.</p>
            <div class="rule">⚠ Valor da nota: 0.0 a 10.0. Requer matrícula ativa.</div>
            <label>Matrícula do Aluno</label><input id="n_alu" placeholder="ex: 2026001">
            <label>Código da Disciplina</label><input id="n_dis" placeholder="ex: ARQ01">
            <label>Valor (0–10)</label><input id="n_val" type="number" step="0.1" placeholder="ex: 9.5">
            <label>Tipo de Avaliação</label><input id="n_tip" placeholder="ex: Trabalho 1">
            <button class="btn-post" onclick="post('/notas',{aluno_matricula:v('n_alu'),disciplina_codigo:v('n_dis'),valor:parseFloat(v('n_val')),tipo_avaliacao:v('n_tip')},'r_nota')">Lançar Nota</button>
            <div class="result" id="r_nota"></div>
        </div>

        <!-- Lançar Frequência -->
        <div class="card">
            <div class="card-header">
                <span class="method POST">POST</span>
                <span class="endpoint">/frequencias</span>
            </div>
            <p class="desc">Registra a frequência de um aluno em uma disciplina.</p>
            <div class="rule">⚠ Presenças ≤ Total de Aulas. Requer matrícula ativa.</div>
            <label>Matrícula do Aluno</label><input id="f_alu" placeholder="ex: 2026001">
            <label>Código da Disciplina</label><input id="f_dis" placeholder="ex: ARQ01">
            <label>Aulas Presentes</label><input id="f_pre" type="number" placeholder="ex: 18">
            <label>Total de Aulas</label><input id="f_tot" type="number" placeholder="ex: 20">
            <button class="btn-post" onclick="post('/frequencias',{aluno_matricula:v('f_alu'),disciplina_codigo:v('f_dis'),aulas_presente:parseInt(v('f_pre')),aulas_total:parseInt(v('f_tot'))},'r_freq')">Lançar Frequência</button>
            <div class="result" id="r_freq"></div>
        </div>

        <!-- Consultar Desempenho -->
        <div class="card">
            <div class="card-header">
                <span class="method GET">GET</span>
                <span class="endpoint">/desempenho/&lt;matricula&gt;</span>
            </div>
            <p class="desc">Retorna o boletim acadêmico completo via DTO + Presenter.</p>
            <label>Matrícula do Aluno</label><input id="des_mat" placeholder="ex: 2026001">
            <button class="btn-get" onclick="get('/desempenho/'+v('des_mat'),'r_des')">Consultar Desempenho</button>
            <div class="result" id="r_des"></div>
        </div>

    </div>
</main>
<footer>Sistema de Gestão Acadêmica &mdash; Clean Architecture Sprint 3 &mdash; Flask API na porta 5000</footer>

<script>
    const v = id => document.getElementById(id).value.trim();
    async function post(url, body, resId) {
        const el = document.getElementById(resId);
        try {
            const r = await fetch(url, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body) });
            const data = await r.json();
            el.textContent = JSON.stringify(data, null, 2);
            el.className = 'result ' + (data.status === 'sucesso' ? 'ok' : 'err');
            el.style.display = 'block';
        } catch(e) { el.textContent = 'Erro de rede: ' + e; el.className='result err'; el.style.display='block'; }
    }
    async function get(url, resId) {
        const el = document.getElementById(resId);
        try {
            const r = await fetch(url);
            const data = await r.json();
            el.textContent = JSON.stringify(data, null, 2);
            el.className = 'result ' + (data.status === 'sucesso' ? 'ok' : 'err');
            el.style.display = 'block';
        } catch(e) { el.textContent = 'Erro de rede: ' + e; el.className='result err'; el.style.display='block'; }
    }
</script>
</body>
</html>""", 200

@app.route("/alunos", methods=["POST"])
def cadastrar_aluno():
    data = request.get_json()
    if not data or "matricula" not in data or "nome" not in data:
        return jsonify({"status": "erro", "mensagem": "Matrícula e nome são obrigatórios."}), 400
    
    res = container.aluno_controller.cadastrar(data["matricula"], data["nome"])
    if res["status"] == "sucesso":
        return jsonify(res), 201
    return jsonify(res), 400

@app.route("/disciplinas", methods=["POST"])
def cadastrar_disciplina():
    data = request.get_json()
    if not data or "codigo" not in data or "nome" not in data or "carga_horaria" not in data:
        return jsonify({"status": "erro", "mensagem": "Código, nome e carga_horaria são obrigatórios."}), 400
    
    try:
        carga_horaria = int(data["carga_horaria"])
    except ValueError:
        return jsonify({"status": "erro", "mensagem": "Carga horária deve ser um número inteiro."}), 400
        
    res = container.disciplina_controller.cadastrar(data["codigo"], data["nome"], carga_horaria)
    if res["status"] == "sucesso":
        return jsonify(res), 201
    return jsonify(res), 400

@app.route("/matriculas", methods=["POST"])
def matricular_aluno():
    data = request.get_json()
    if not data or "aluno_matricula" not in data or "disciplina_codigo" not in data:
        return jsonify({"status": "erro", "mensagem": "Matrícula do aluno e código da disciplina são obrigatórios."}), 400
        
    res = container.matricula_controller.matricular(data["aluno_matricula"], data["disciplina_codigo"])
    if res["status"] == "sucesso":
        return jsonify(res), 201
    return jsonify(res), 400

@app.route("/notas", methods=["POST"])
def lancar_nota():
    data = request.get_json()
    required = ["aluno_matricula", "disciplina_codigo", "valor", "tipo_avaliacao"]
    if not data or any(k not in data for k in required):
        return jsonify({"status": "erro", "mensagem": "Campos obrigatórios: aluno_matricula, disciplina_codigo, valor, tipo_avaliacao."}), 400
        
    try:
        valor = float(data["valor"])
    except ValueError:
        return jsonify({"status": "erro", "mensagem": "Valor da nota deve ser um número."}), 400
        
    res = container.nota_controller.lancar(
        data["aluno_matricula"], data["disciplina_codigo"], valor, data["tipo_avaliacao"]
    )
    if res["status"] == "sucesso":
        return jsonify(res), 201
    return jsonify(res), 400

@app.route("/frequencias", methods=["POST"])
def lancar_frequencia():
    data = request.get_json()
    required = ["aluno_matricula", "disciplina_codigo", "aulas_presente", "aulas_total"]
    if not data or any(k not in data for k in required):
        return jsonify({"status": "erro", "mensagem": "Campos obrigatórios: aluno_matricula, disciplina_codigo, aulas_presente, aulas_total."}), 400
        
    try:
        aulas_presente = int(data["aulas_presente"])
        aulas_total = int(data["aulas_total"])
    except ValueError:
        return jsonify({"status": "erro", "mensagem": "Aulas presente e total devem ser números inteiros."}), 400
        
    res = container.frequencia_controller.lancar(
        data["aluno_matricula"], data["disciplina_codigo"], aulas_presente, aulas_total
    )
    if res["status"] == "sucesso":
        return jsonify(res), 201
    return jsonify(res), 400

@app.route("/desempenho/<matricula>", methods=["GET"])
def consultar_desempenho(matricula):
    res = container.desempenho_controller.consultar_json(matricula)
    if res["status"] == "sucesso":
        return jsonify(res), 200
    return jsonify(res), 400

def run():
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    run()
from flask import Flask, request, jsonify
from src.infrastructure.di.container import Container

app = Flask(__name__)
container = Container()

# ── HTML ─────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SGA — Sistema de Gestão Acadêmica</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0b0d14;--surface:#141720;--surface2:#1c2030;--surface3:#222840;
  --border:#252d45;--accent:#6c63ff;--accent2:#00d4aa;--danger:#ff6b6b;--warn:#ffa94d;
  --text:#e8eaf0;--muted:#7a82a8;--radius:12px;
}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}

/* ── LOGIN ── */
#screen-login{display:flex;align-items:center;justify-content:center;min-height:100vh;padding:1rem}
.login-wrap{width:100%;max-width:400px}
.login-logo{text-align:center;margin-bottom:2rem}
.login-logo h1{font-size:2rem;font-weight:700;background:linear-gradient(90deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.login-logo p{color:var(--muted);font-size:.9rem;margin-top:.35rem}
.login-card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:2rem}
.login-card h2{font-size:1.1rem;font-weight:600;margin-bottom:1.5rem;color:var(--text)}
.field{margin-bottom:1rem}
.field label{display:block;font-size:.75rem;color:var(--muted);margin-bottom:.4rem;font-weight:500}
.field input{width:100%;background:var(--surface2);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:.6rem .85rem;font-size:.9rem;outline:none;transition:border-color .2s;font-family:'Inter',sans-serif}
.field input:focus{border-color:var(--accent)}
.btn-login{width:100%;padding:.7rem;border-radius:8px;border:none;background:linear-gradient(135deg,var(--accent),#8b84ff);color:#fff;font-weight:600;font-size:.95rem;cursor:pointer;transition:opacity .2s;margin-top:.5rem}
.btn-login:hover{opacity:.88}
#login-error{display:none;background:rgba(255,107,107,.1);border:1px solid rgba(255,107,107,.3);border-radius:8px;padding:.6rem .9rem;font-size:.82rem;color:var(--danger);margin-top:.75rem;text-align:center}
.login-hint{text-align:center;margin-top:1.25rem;font-size:.78rem;color:var(--muted)}

/* ── DASHBOARD ── */
#screen-dashboard{display:none;flex-direction:column;min-height:100vh}
header{background:var(--surface);border-bottom:1px solid var(--border);padding:.9rem 2rem;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}
.hdr-left{display:flex;align-items:center;gap:1rem}
.hdr-logo{font-size:1.25rem;font-weight:700;background:linear-gradient(90deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hdr-right{display:flex;align-items:center;gap:.75rem}
.user-info{text-align:right}
.user-nome{font-size:.9rem;font-weight:600}
.user-perfil{font-size:.72rem;color:var(--muted)}
.perfil-badge{font-size:.65rem;font-weight:700;padding:3px 10px;border-radius:20px;letter-spacing:.5px;text-transform:uppercase}
.badge-aluno{background:rgba(0,212,170,.15);border:1px solid var(--accent2);color:var(--accent2)}
.badge-professor{background:rgba(108,99,255,.15);border:1px solid var(--accent);color:var(--accent)}
.badge-administrador{background:rgba(255,169,77,.15);border:1px solid var(--warn);color:var(--warn)}
.btn-sair{background:transparent;border:1px solid var(--border);color:var(--muted);border-radius:8px;padding:.4rem .9rem;font-size:.8rem;cursor:pointer;transition:all .2s;font-family:'Inter',sans-serif}
.btn-sair:hover{border-color:var(--danger);color:var(--danger)}

main{flex:1;max-width:1300px;width:100%;margin:0 auto;padding:2rem}
.welcome-banner{background:linear-gradient(135deg,var(--surface) 0%,var(--surface2) 100%);border:1px solid var(--border);border-radius:var(--radius);padding:1.5rem 2rem;margin-bottom:2rem;display:flex;align-items:center;gap:1rem}
.welcome-icon{font-size:2.5rem}
.welcome-text h2{font-size:1.2rem;font-weight:600}
.welcome-text p{color:var(--muted);font-size:.85rem;margin-top:.2rem}

h3{font-size:.82rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:1px;margin:2rem 0 1rem;padding-bottom:.5rem;border-bottom:1px solid var(--border)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1rem}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem;transition:border-color .2s,transform .2s}
.card:hover{border-color:var(--accent);transform:translateY(-2px)}
.card-header{display:flex;align-items:center;gap:.6rem;margin-bottom:.75rem;flex-wrap:wrap}
.card-title{font-size:.95rem;font-weight:600;flex:1}
.method{font-size:.6rem;font-weight:700;padding:2px 8px;border-radius:5px;letter-spacing:.5px;white-space:nowrap}
.POST{background:rgba(108,99,255,.2);color:var(--accent);border:1px solid var(--accent)}
.GET{background:rgba(0,212,170,.2);color:var(--accent2);border:1px solid var(--accent2)}
.PATCH{background:rgba(255,169,77,.2);color:var(--warn);border:1px solid var(--warn)}
.desc{font-size:.8rem;color:var(--muted);margin-bottom:1rem;line-height:1.5}
label{display:block;font-size:.73rem;color:var(--muted);margin-bottom:.3rem;font-weight:500}
input,select{width:100%;background:var(--surface2);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:.5rem .75rem;font-size:.85rem;margin-bottom:.6rem;outline:none;transition:border-color .2s;font-family:'Inter',sans-serif}
input:focus,select:focus{border-color:var(--accent)}
button.action{width:100%;padding:.52rem;border-radius:8px;border:none;font-weight:600;font-size:.85rem;cursor:pointer;transition:opacity .2s;font-family:'Inter',sans-serif}
button.action:hover{opacity:.85}
.btn-post{background:var(--accent);color:#fff}
.btn-get{background:var(--accent2);color:#000}
.btn-patch{background:var(--warn);color:#000}
.result{margin-top:.7rem;background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:.7rem;font-family:monospace;font-size:.72rem;white-space:pre-wrap;word-break:break-all;max-height:180px;overflow-y:auto;display:none;color:var(--text)}
.result.ok{border-color:var(--accent2)}
.result.err{border-color:var(--danger)}
.rule{background:rgba(255,169,77,.06);border:1px solid rgba(255,169,77,.2);border-radius:8px;padding:.5rem .8rem;margin-bottom:.7rem;font-size:.76rem;color:var(--warn)}
footer{text-align:center;padding:1.5rem;color:var(--muted);font-size:.72rem;border-top:1px solid var(--border)}
</style>
</head>
<body>

<!-- ═══════════════════════════ LOGIN ═══════════════════════════ -->
<div id="screen-login">
  <div class="login-wrap">
    <div class="login-logo">
      <h1>&#127979; SGA</h1>
      <p>Sistema de Gestão Acadêmica</p>
    </div>
    <div class="login-card">
      <h2>Entrar na sua conta</h2>
      <div class="field">
        <label>Login</label>
        <input id="l_log" placeholder="ex: alice.silva" onkeydown="if(event.key==='Enter')doLogin()">
      </div>
      <div class="field">
        <label>Senha</label>
        <input id="l_sen" type="password" placeholder="sua senha" onkeydown="if(event.key==='Enter')doLogin()">
      </div>
      <button class="btn-login" onclick="doLogin()">Entrar</button>
      <div id="login-error">Login ou senha incorretos.</div>
    </div>
    <p class="login-hint">Não tem conta? Peça ao administrador do sistema.</p>
  </div>
</div>

<!-- ═══════════════════════════ DASHBOARD ═══════════════════════════ -->
<div id="screen-dashboard">
  <header>
    <div class="hdr-left">
      <span class="hdr-logo">&#127979; SGA</span>
    </div>
    <div class="hdr-right">
      <div class="user-info">
        <div class="user-nome" id="hdr-nome">—</div>
        <div class="user-perfil">Perfil: <span id="hdr-perfil">—</span></div>
      </div>
      <span class="perfil-badge" id="hdr-badge">—</span>
      <button class="btn-sair" onclick="logout()">Sair</button>
    </div>
  </header>

  <main>
    <!-- ── ALUNO ── -->
    <div id="dash-aluno" style="display:none">
      <div class="welcome-banner">
        <span class="welcome-icon">&#127891;</span>
        <div class="welcome-text">
          <h2>Olá, <span id="aluno-nome">Aluno</span>!</h2>
          <p>Consulte seu desempenho, notas e situação acadêmica.</p>
        </div>
      </div>

      <h3>Minhas Consultas</h3>
      <div class="grid">
        <div class="card">
          <div class="card-header"><span class="method GET">GET</span><span class="card-title">Meu Desempenho</span></div>
          <p class="desc">Boletim completo com todas as disciplinas, notas e frequência.</p>
          <label>Minha Matrícula</label><input id="a_des_mat" placeholder="ex: 2026001">
          <button class="action btn-get" onclick="api_get('/desempenho/'+v('a_des_mat'),'a_r_des')">Ver Desempenho</button>
          <div class="result" id="a_r_des"></div>
        </div>
        <div class="card">
          <div class="card-header"><span class="method GET">GET</span><span class="card-title">Calcular Média</span></div>
          <p class="desc">Calcula sua média final em uma disciplina. Aprovado se média ≥ 6.0.</p>
          <label>Minha Matrícula</label><input id="a_med_mat" placeholder="ex: 2026001">
          <label>Código da Disciplina</label><input id="a_med_dis" placeholder="ex: ARQ01">
          <button class="action btn-get" onclick="api_get('/media/'+v('a_med_mat')+'/'+v('a_med_dis'),'a_r_med')">Calcular Média</button>
          <div class="result" id="a_r_med"></div>
        </div>
        <div class="card">
          <div class="card-header"><span class="method GET">GET</span><span class="card-title">Situação de Aprovação</span></div>
          <p class="desc">Verifica se você está aprovado (média ≥ 6.0 e frequência ≥ 75%).</p>
          <label>Minha Matrícula</label><input id="a_apr_mat" placeholder="ex: 2026001">
          <label>Código da Disciplina</label><input id="a_apr_dis" placeholder="ex: ARQ01">
          <button class="action btn-get" onclick="api_get('/aprovacao/'+v('a_apr_mat')+'/'+v('a_apr_dis'),'a_r_apr')">Ver Aprovação</button>
          <div class="result" id="a_r_apr"></div>
        </div>
      </div>
    </div>

    <!-- ── PROFESSOR ── -->
    <div id="dash-professor" style="display:none">
      <div class="welcome-banner">
        <span class="welcome-icon">&#128218;</span>
        <div class="welcome-text">
          <h2>Olá, Prof. <span id="prof-nome">Professor</span>!</h2>
          <p>Lance notas, registre frequência e acompanhe seus alunos.</p>
        </div>
      </div>

      <h3>Lançamentos</h3>
      <div class="grid">
        <div class="card">
          <div class="card-header"><span class="method POST">POST</span><span class="card-title">Lançar Nota</span></div>
          <p class="desc">Registra a nota de um aluno em uma disciplina.</p>
          <div class="rule">⚠ Valor entre 0.0 e 10.0. Aluno deve estar matriculado.</div>
          <label>Matrícula do Aluno</label><input id="p_n_alu" placeholder="ex: 2026001">
          <label>Código da Disciplina</label><input id="p_n_dis" placeholder="ex: ARQ01">
          <label>Valor (0–10)</label><input id="p_n_val" type="number" step="0.1" placeholder="ex: 8.5">
          <label>Tipo de Avaliação</label><input id="p_n_tip" placeholder="ex: Prova 1">
          <button class="action btn-post" onclick="api_post('/notas',{aluno_matricula:v('p_n_alu'),disciplina_codigo:v('p_n_dis'),valor:parseFloat(v('p_n_val')),tipo_avaliacao:v('p_n_tip')},'p_r_nota')">Lançar Nota</button>
          <div class="result" id="p_r_nota"></div>
        </div>
        <div class="card">
          <div class="card-header"><span class="method POST">POST</span><span class="card-title">Registrar Frequência</span></div>
          <p class="desc">Registra as presenças do aluno na disciplina.</p>
          <div class="rule">⚠ Presenças não podem exceder o total de aulas.</div>
          <label>Matrícula do Aluno</label><input id="p_f_alu" placeholder="ex: 2026001">
          <label>Código da Disciplina</label><input id="p_f_dis" placeholder="ex: ARQ01">
          <label>Aulas Presentes</label><input id="p_f_pre" type="number" placeholder="ex: 16">
          <label>Total de Aulas</label><input id="p_f_tot" type="number" placeholder="ex: 20">
          <button class="action btn-post" onclick="api_post('/frequencias',{aluno_matricula:v('p_f_alu'),disciplina_codigo:v('p_f_dis'),aulas_presente:parseInt(v('p_f_pre')),aulas_total:parseInt(v('p_f_tot'))},'p_r_freq')">Registrar Frequência</button>
          <div class="result" id="p_r_freq"></div>
        </div>
      </div>

      <h3>Acompanhamento</h3>
      <div class="grid">
        <div class="card">
          <div class="card-header"><span class="method GET">GET</span><span class="card-title">Listar Alunos</span></div>
          <p class="desc">Exibe todos os alunos cadastrados no sistema.</p>
          <button class="action btn-get" onclick="api_get('/alunos','p_r_lista')">Ver Todos os Alunos</button>
          <div class="result" id="p_r_lista"></div>
        </div>
        <div class="card">
          <div class="card-header"><span class="method GET">GET</span><span class="card-title">Desempenho do Aluno</span></div>
          <p class="desc">Consulta o boletim completo de um aluno específico.</p>
          <label>Matrícula do Aluno</label><input id="p_des_mat" placeholder="ex: 2026001">
          <button class="action btn-get" onclick="api_get('/desempenho/'+v('p_des_mat'),'p_r_des')">Ver Boletim</button>
          <div class="result" id="p_r_des"></div>
        </div>
        <div class="card">
          <div class="card-header"><span class="method GET">GET</span><span class="card-title">Situação de Aprovação</span></div>
          <p class="desc">Verifica aprovação do aluno com base em média e frequência.</p>
          <label>Matrícula do Aluno</label><input id="p_apr_mat" placeholder="ex: 2026001">
          <label>Código da Disciplina</label><input id="p_apr_dis" placeholder="ex: ARQ01">
          <button class="action btn-get" onclick="api_get('/aprovacao/'+v('p_apr_mat')+'/'+v('p_apr_dis'),'p_r_apr')">Verificar Aprovação</button>
          <div class="result" id="p_r_apr"></div>
        </div>
      </div>
    </div>

    <!-- ── ADMINISTRADOR ── -->
    <div id="dash-administrador" style="display:none">
      <div class="welcome-banner">
        <span class="welcome-icon">&#9881;&#65039;</span>
        <div class="welcome-text">
          <h2>Painel Administrativo</h2>
          <p>Gerencie alunos, professores, disciplinas, matrículas e usuários do sistema.</p>
        </div>
      </div>

      <h3>Gestão de Alunos</h3>
      <div class="grid">
        <div class="card">
          <div class="card-header"><span class="method POST">POST</span><span class="card-title">Cadastrar Aluno</span></div>
          <p class="desc">Registra um novo aluno no sistema acadêmico.</p>
          <label>Matrícula</label><input id="ad_a_mat" placeholder="ex: 2026001">
          <label>Nome Completo</label><input id="ad_a_nom" placeholder="ex: Carlos Eduardo Meneguette">
          <button class="action btn-post" onclick="api_post('/alunos',{matricula:v('ad_a_mat'),nome:v('ad_a_nom')},'ad_r_acad')">Cadastrar Aluno</button>
          <div class="result" id="ad_r_acad"></div>
        </div>
        <div class="card">
          <div class="card-header"><span class="method GET">GET</span><span class="card-title">Listar Alunos</span></div>
          <p class="desc">Exibe todos os alunos com matrícula, nome e situação atual.</p>
          <button class="action btn-get" onclick="api_get('/alunos','ad_r_alist')">Listar Alunos</button>
          <div class="result" id="ad_r_alist"></div>
        </div>
        <div class="card">
          <div class="card-header"><span class="method PATCH">PATCH</span><span class="card-title">Alterar Situação</span></div>
          <p class="desc">Atualiza a situação acadêmica do aluno.</p>
          <div class="rule">⚠ Situações: Ativo, Trancado, Formado.</div>
          <label>Matrícula do Aluno</label><input id="ad_sit_mat" placeholder="ex: 2026001">
          <label>Nova Situação</label>
          <select id="ad_sit_val"><option value="Ativo">Ativo</option><option value="Trancado">Trancado</option><option value="Formado">Formado</option></select>
          <button class="action btn-patch" onclick="api_patch('/alunos/'+v('ad_sit_mat')+'/situacao',{nova_situacao:v('ad_sit_val')},'ad_r_sit')">Alterar Situação</button>
          <div class="result" id="ad_r_sit"></div>
        </div>
      </div>

      <h3>Gestão Acadêmica</h3>
      <div class="grid">
        <div class="card">
          <div class="card-header"><span class="method POST">POST</span><span class="card-title">Cadastrar Disciplina</span></div>
          <p class="desc">Registra uma nova disciplina com carga horária.</p>
          <div class="rule">⚠ Carga horária deve ser maior que zero.</div>
          <label>Código</label><input id="ad_d_cod" placeholder="ex: ARQ01">
          <label>Nome</label><input id="ad_d_nom" placeholder="ex: Arquitetura de Software">
          <label>Carga Horária (h)</label><input id="ad_d_ch" type="number" placeholder="ex: 60">
          <button class="action btn-post" onclick="api_post('/disciplinas',{codigo:v('ad_d_cod'),nome:v('ad_d_nom'),carga_horaria:parseInt(v('ad_d_ch'))},'ad_r_disc')">Cadastrar Disciplina</button>
          <div class="result" id="ad_r_disc"></div>
        </div>
        <div class="card">
          <div class="card-header"><span class="method POST">POST</span><span class="card-title">Matricular Aluno</span></div>
          <p class="desc">Vincula um aluno a uma disciplina. Bloqueia duplicatas.</p>
          <label>Matrícula do Aluno</label><input id="ad_m_alu" placeholder="ex: 2026001">
          <label>Código da Disciplina</label><input id="ad_m_dis" placeholder="ex: ARQ01">
          <button class="action btn-post" onclick="api_post('/matriculas',{aluno_matricula:v('ad_m_alu'),disciplina_codigo:v('ad_m_dis')},'ad_r_mat')">Matricular</button>
          <div class="result" id="ad_r_mat"></div>
        </div>
      </div>

      <h3>Gestão de Professores</h3>
      <div class="grid">
        <div class="card">
          <div class="card-header"><span class="method POST">POST</span><span class="card-title">Cadastrar Professor</span></div>
          <p class="desc">Registra um novo professor no sistema.</p>
          <label>Matrícula Funcional</label><input id="ad_p_mat" placeholder="ex: PROF001">
          <label>Nome</label><input id="ad_p_nom" placeholder="ex: Dr. João Souza">
          <label>E-mail</label><input id="ad_p_ema" placeholder="ex: joao@uni.edu.br">
          <button class="action btn-post" onclick="api_post('/professores',{matricula_funcional:v('ad_p_mat'),nome:v('ad_p_nom'),email:v('ad_p_ema')},'ad_r_pcad')">Cadastrar Professor</button>
          <div class="result" id="ad_r_pcad"></div>
        </div>
        <div class="card">
          <div class="card-header"><span class="method GET">GET</span><span class="card-title">Listar Professores</span></div>
          <p class="desc">Exibe todos os professores cadastrados no sistema.</p>
          <button class="action btn-get" onclick="api_get('/professores','ad_r_plist')">Listar Professores</button>
          <div class="result" id="ad_r_plist"></div>
        </div>
      </div>

      <h3>Acesso ao Sistema</h3>
      <div class="grid">
        <div class="card">
          <div class="card-header"><span class="method POST">POST</span><span class="card-title">Cadastrar Usuário</span></div>
          <p class="desc">Cria credenciais de acesso para aluno, professor ou administrador.</p>
          <div class="rule">⚠ Perfis válidos: aluno, professor, administrador.</div>
          <label>Login</label><input id="ad_u_log" placeholder="ex: alice.silva">
          <label>Nome</label><input id="ad_u_nom" placeholder="ex: Alice Silva">
          <label>Senha</label><input id="ad_u_sen" type="password" placeholder="mínimo 4 caracteres">
          <label>Perfil</label>
          <select id="ad_u_per"><option value="aluno">aluno</option><option value="professor">professor</option><option value="administrador">administrador</option></select>
          <button class="action btn-post" onclick="api_post('/usuarios',{login:v('ad_u_log'),nome:v('ad_u_nom'),senha:v('ad_u_sen'),perfil:v('ad_u_per')},'ad_r_ucad')">Criar Usuário</button>
          <div class="result" id="ad_r_ucad"></div>
        </div>
      </div>
    </div>
  </main>

  <footer>Sistema de Gestão Acadêmica &mdash; Clean Architecture Sprint 3</footer>
</div>

<script>
const v = id => document.getElementById(id).value.trim();
let currentUser = null;

async function doLogin() {
  const login = v('l_log'), senha = v('l_sen');
  document.getElementById('login-error').style.display = 'none';
  try {
    const r = await fetch('/auth/login', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({login, senha})});
    const data = await r.json();
    if (data.status === 'sucesso' && data.dados && data.dados.autenticado) {
      currentUser = data.dados;
      showDashboard(currentUser);
    } else {
      document.getElementById('login-error').style.display = 'block';
    }
  } catch(e) {
    document.getElementById('login-error').textContent = 'Erro de conexão.';
    document.getElementById('login-error').style.display = 'block';
  }
}

function showDashboard(user) {
  document.getElementById('screen-login').style.display = 'none';
  const dash = document.getElementById('screen-dashboard');
  dash.style.display = 'flex';
  document.getElementById('hdr-nome').textContent = user.nome;
  document.getElementById('hdr-perfil').textContent = user.perfil;
  const badge = document.getElementById('hdr-badge');
  badge.textContent = user.perfil;
  badge.className = 'perfil-badge badge-' + user.perfil;
  ['aluno','professor','administrador'].forEach(p => {
    document.getElementById('dash-' + p).style.display = (p === user.perfil) ? 'block' : 'none';
  });
  if (user.perfil === 'aluno') document.getElementById('aluno-nome').textContent = user.nome;
  if (user.perfil === 'professor') document.getElementById('prof-nome').textContent = user.nome;
  document.getElementById('l_log').value = '';
  document.getElementById('l_sen').value = '';
}

function logout() {
  currentUser = null;
  document.getElementById('screen-dashboard').style.display = 'none';
  document.getElementById('screen-login').style.display = 'flex';
}

async function api_post(url, body, resId) {
  const el = document.getElementById(resId);
  try {
    const r = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
    const data = await r.json();
    el.textContent = JSON.stringify(data, null, 2);
    el.className = 'result ' + (data.status === 'sucesso' ? 'ok' : 'err');
    el.style.display = 'block';
  } catch(e) { el.textContent = 'Erro: ' + e; el.className='result err'; el.style.display='block'; }
}
async function api_get(url, resId) {
  const el = document.getElementById(resId);
  try {
    const r = await fetch(url);
    const data = await r.json();
    el.textContent = JSON.stringify(data, null, 2);
    el.className = 'result ' + (data.status === 'sucesso' ? 'ok' : 'err');
    el.style.display = 'block';
  } catch(e) { el.textContent = 'Erro: ' + e; el.className='result err'; el.style.display='block'; }
}
async function api_patch(url, body, resId) {
  const el = document.getElementById(resId);
  try {
    const r = await fetch(url, {method:'PATCH', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
    const data = await r.json();
    el.textContent = JSON.stringify(data, null, 2);
    el.className = 'result ' + (data.status === 'sucesso' ? 'ok' : 'err');
    el.style.display = 'block';
  } catch(e) { el.textContent = 'Erro: ' + e; el.className='result err'; el.style.display='block'; }
}
</script>
</body>
</html>""", 200

# ── Endpoints base ────────────────────────────────────────────────────────────

@app.route("/alunos", methods=["POST"])
def cadastrar_aluno():
    data = request.get_json()
    if not data or "matricula" not in data or "nome" not in data:
        return jsonify({"status": "erro", "mensagem": "Matrícula e nome são obrigatórios."}), 400
    res = container.aluno_controller.cadastrar(data["matricula"], data["nome"])
    return jsonify(res), 201 if res["status"] == "sucesso" else 400

@app.route("/alunos", methods=["GET"])
def listar_alunos():
    res = container.aluno_controller.listar()
    return jsonify(res), 200

@app.route("/alunos/<matricula>/situacao", methods=["PATCH"])
def alterar_situacao(matricula):
    data = request.get_json()
    if not data or "nova_situacao" not in data:
        return jsonify({"status": "erro", "mensagem": "O campo 'nova_situacao' é obrigatório."}), 400
    res = container.alterar_situacao_controller.alterar(matricula, data["nova_situacao"])
    return jsonify(res), 200 if res["status"] == "sucesso" else 400

@app.route("/disciplinas", methods=["POST"])
def cadastrar_disciplina():
    data = request.get_json()
    if not data or "codigo" not in data or "nome" not in data or "carga_horaria" not in data:
        return jsonify({"status": "erro", "mensagem": "Código, nome e carga_horaria são obrigatórios."}), 400
    try:
        carga_horaria = int(data["carga_horaria"])
    except (ValueError, TypeError):
        return jsonify({"status": "erro", "mensagem": "Carga horária deve ser um número inteiro."}), 400
    res = container.disciplina_controller.cadastrar(data["codigo"], data["nome"], carga_horaria)
    return jsonify(res), 201 if res["status"] == "sucesso" else 400

@app.route("/matriculas", methods=["POST"])
def matricular_aluno():
    data = request.get_json()
    if not data or "aluno_matricula" not in data or "disciplina_codigo" not in data:
        return jsonify({"status": "erro", "mensagem": "Matrícula do aluno e código da disciplina são obrigatórios."}), 400
    res = container.matricula_controller.matricular(data["aluno_matricula"], data["disciplina_codigo"])
    return jsonify(res), 201 if res["status"] == "sucesso" else 400

@app.route("/notas", methods=["POST"])
def lancar_nota():
    data = request.get_json()
    required = ["aluno_matricula", "disciplina_codigo", "valor", "tipo_avaliacao"]
    if not data or any(k not in data for k in required):
        return jsonify({"status": "erro", "mensagem": f"Campos obrigatórios: {', '.join(required)}."}), 400
    try:
        valor = float(data["valor"])
    except (ValueError, TypeError):
        return jsonify({"status": "erro", "mensagem": "Valor da nota deve ser um número."}), 400
    res = container.nota_controller.lancar(
        data["aluno_matricula"], data["disciplina_codigo"], valor, data["tipo_avaliacao"]
    )
    return jsonify(res), 201 if res["status"] == "sucesso" else 400

@app.route("/frequencias", methods=["POST"])
def lancar_frequencia():
    data = request.get_json()
    required = ["aluno_matricula", "disciplina_codigo", "aulas_presente", "aulas_total"]
    if not data or any(k not in data for k in required):
        return jsonify({"status": "erro", "mensagem": f"Campos obrigatórios: {', '.join(required)}."}), 400
    try:
        aulas_presente = int(data["aulas_presente"])
        aulas_total = int(data["aulas_total"])
    except (ValueError, TypeError):
        return jsonify({"status": "erro", "mensagem": "Aulas presente e total devem ser inteiros."}), 400
    res = container.frequencia_controller.lancar(
        data["aluno_matricula"], data["disciplina_codigo"], aulas_presente, aulas_total
    )
    return jsonify(res), 201 if res["status"] == "sucesso" else 400

@app.route("/desempenho/<matricula>", methods=["GET"])
def consultar_desempenho(matricula):
    res = container.desempenho_controller.consultar_json(matricula)
    return jsonify(res), 200 if res["status"] == "sucesso" else 404

@app.route("/aprovacao/<aluno_matricula>/<disciplina_codigo>", methods=["GET"])
def calcular_aprovacao(aluno_matricula, disciplina_codigo):
    res = container.aprovacao_controller.calcular(aluno_matricula, disciplina_codigo)
    return jsonify(res), 200 if res["status"] == "sucesso" else 404

# ── Novos endpoints ───────────────────────────────────────────────────────────

@app.route("/professores", methods=["POST"])
def cadastrar_professor():
    data = request.get_json()
    required = ["matricula_funcional", "nome", "email"]
    if not data or any(k not in data for k in required):
        return jsonify({"status": "erro", "mensagem": f"Campos obrigatórios: {', '.join(required)}."}), 400
    res = container.professor_controller.cadastrar(data["matricula_funcional"], data["nome"], data["email"])
    return jsonify(res), 201 if res["status"] == "sucesso" else 400

@app.route("/professores", methods=["GET"])
def listar_professores():
    res = container.professor_controller.listar()
    return jsonify(res), 200

@app.route("/usuarios", methods=["POST"])
def cadastrar_usuario():
    data = request.get_json()
    required = ["login", "nome", "senha", "perfil"]
    if not data or any(k not in data for k in required):
        return jsonify({"status": "erro", "mensagem": f"Campos obrigatórios: {', '.join(required)}."}), 400
    res = container.autenticacao_controller.cadastrar(
        data["login"], data["nome"], data["senha"], data["perfil"]
    )
    return jsonify(res), 201 if res["status"] == "sucesso" else 400

@app.route("/auth/login", methods=["POST"])
def autenticar():
    data = request.get_json()
    if not data or "login" not in data or "senha" not in data:
        return jsonify({"status": "erro", "mensagem": "Login e senha são obrigatórios."}), 400
    res = container.autenticacao_controller.autenticar(data["login"], data["senha"])
    return jsonify(res), 200 if res["status"] == "sucesso" else 401

@app.route("/media/<aluno_matricula>/<disciplina_codigo>", methods=["GET"])
def calcular_media(aluno_matricula, disciplina_codigo):
    res = container.media_controller.calcular(aluno_matricula, disciplina_codigo)
    return jsonify(res), 200 if res["status"] == "sucesso" else 404


def run():
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    run()

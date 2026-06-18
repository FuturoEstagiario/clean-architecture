const v = id => document.getElementById(id).value.trim();
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const ICONS = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
    err: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/></svg>',
    inbox: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>'
};

function toast(msg, type = 'ok') {
    const stack = document.getElementById('toastStack');
    if (!stack) return;
    const el = document.createElement('div');
    el.className = 'toast ' + type;
    el.innerHTML = '<span class="ico">' + (type === 'ok' ? ICONS.ok : ICONS.err) + '</span><span>' + esc(msg) + '</span>';
    stack.appendChild(el);
    setTimeout(() => {
        el.classList.add('out');
        el.addEventListener('animationend', () => el.remove());
    }, 3200);
}

function setLoading(btn, loading) {
    if (!btn) return;
    if (loading) {
        btn.dataset.label = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span>' + (btn.dataset.loadingText || 'Processando...');
    } else {
        btn.disabled = false;
        if (btn.dataset.label) btn.innerHTML = btn.dataset.label;
    }
}

function syntaxHighlight(obj) {
    const json = JSON.stringify(obj, null, 2)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-fA-F0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false)\b|\bnull\b|-?\d+(\.\d+)?([eE][+-]?\d+)?)/g, m => {
        let cls = 'json-num';
        if (/^"/.test(m)) cls = /:$/.test(m) ? 'json-key' : 'json-str';
        else if (/true|false/.test(m)) cls = 'json-bool';
        else if (/null/.test(m)) cls = 'json-null';
        return '<span class="' + cls + '">' + m + '</span>';
    });
}

function mediaClass(m) {
    const n = parseFloat(m);
    if (isNaN(n)) return '';
    return n >= 7 ? 'good' : (n >= 5 ? 'warn' : 'bad');
}

function renderBoletim(d) {
    const a = d.aluno || {};
    const discs = d.desempenho_disciplinas || [];
    let html = '<div class="boletim"><div class="boletim-head"><div class="boletim-id">' +
        '<strong>' + esc(a.nome || '—') + '</strong>' +
        '<span class="boletim-mat">Matrícula ' + esc(a.matricula || '—') + '</span></div>' +
        (a.situacao ? renderCell('situacao', a.situacao) : '') + '</div>';
    if (!discs.length) {
        html += '<div class="boletim-empty">Nenhuma disciplina matriculada.</div>';
    } else {
        html += '<div class="disc-list">';
        for (const x of discs) {
            const notas = (x.notas && x.notas.length) ? x.notas.map(n => Number(n).toFixed(1)).join(' · ') : 'Sem notas';
            const freq = x.frequencia || {};
            html += '<div class="disc-item"><div class="disc-top">' +
                '<span class="disc-name">' + esc(x.nome) + '</span>' +
                '<span class="disc-code">' + esc(x.codigo) + '</span></div>' +
                '<div class="disc-stats">' +
                    '<span class="stat"><label>Média</label><b class="media ' + mediaClass(x.media_final) + '">' + esc(x.media_final) + '</b></span>' +
                    '<span class="stat"><label>Notas</label><b>' + esc(notas) + '</b></span>' +
                    '<span class="stat"><label>Frequência</label><b>' + esc(freq.percentual || '—') + '</b></span>' +
                '</div></div>';
        }
        html += '</div>';
    }
    return html + '</div>';
}

function renderResult(el, data, ok) {
    const state = ok ? 'ok' : 'err';
    const label = ok ? 'Sucesso' : 'Não foi possível';
    const icon = ok ? ICONS.ok : ICONS.err;
    el.className = 'result show ' + state;

    let body = '';
    if (data && typeof data.mensagem === 'string') {
        body += '<p class="result-msg">' + esc(data.mensagem) + '</p>';
    }
    if (data && data.dados && data.dados.aluno) {
        body += renderBoletim(data.dados);
    } else if (data && data.dados && !data.mensagem) {
        body += '<pre>' + syntaxHighlight(data.dados) + '</pre>';
    }
    if (!body) body = '<pre>' + syntaxHighlight(data) + '</pre>';

    el.innerHTML =
        '<div class="result-head"><span class="status-dot"></span>' +
        '<span class="ico" style="width:14px;height:14px;display:inline-flex">' + icon + '</span>' +
        '<span>' + label + '</span>' +
        '<div class="result-actions">' +
            '<button class="mini-btn toggle-raw" type="button" title="Ver resposta JSON da API">{ }</button>' +
            '<button class="mini-btn copy-btn" type="button">Copiar</button>' +
        '</div></div>' +
        '<div class="result-body">' + body + '</div>' +
        '<div class="result-raw" hidden><pre>' + syntaxHighlight(data) + '</pre></div>';

    el.querySelector('.copy-btn').addEventListener('click', () => {
        navigator.clipboard.writeText(JSON.stringify(data, null, 2)).then(() => toast('JSON copiado.', 'ok'));
    });
    const raw = el.querySelector('.result-raw');
    el.querySelector('.toggle-raw').addEventListener('click', e => {
        raw.hidden = !raw.hidden;
        e.currentTarget.classList.toggle('on', !raw.hidden);
    });
}

async function send(url, options, resId, btn, reload) {
    const el = document.getElementById(resId);
    setLoading(btn, true);
    try {
        const r = await fetch(url, options);
        const data = await r.json();
        const ok = data.status === 'sucesso';
        renderResult(el, data, ok);
        toast(data.mensagem || (ok ? 'Operação concluída.' : 'Falha na operação.'), ok ? 'ok' : 'err');
        if (ok && reload) listar(reload[0], reload[1], reload[2]);
    } catch (e) {
        renderResult(el, { erro: 'Falha de rede', detalhe: String(e) }, false);
        toast('Erro de rede: ' + e, 'err');
    } finally {
        setLoading(btn, false);
    }
}

const post = (url, body, resId, btn, reload) =>
    send(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }, resId, btn, reload);

const get = (url, resId, btn) => send(url, {}, resId, btn);

function renderCell(campo, value) {
    if (value === undefined || value === null || value === '') return '<span class="json-null">—</span>';
    if (campo === 'situacao') {
        const s = String(value).toLowerCase();
        const cls = s.startsWith('ativ') ? '' : (s.startsWith('inativ') || s.startsWith('tranc') ? 'danger' : 'neutral');
        return '<span class="chip ' + cls + '">' + esc(value) + '</span>';
    }
    if (campo === 'carga_horaria') return esc(value) + '<span class="json-null">h</span>';
    return esc(value);
}

function emptyRow(colspan, msg) {
    return '<tr><td colspan="' + colspan + '"><div class="empty-state">' +
        '<span class="icon">' + ICONS.inbox + '</span>' +
        '<strong>Nenhum registro encontrado</strong>' +
        '<span>' + esc(msg) + '</span></div></td></tr>';
}

async function listar(url, tbodyId, campos, btn) {
    const tbody = document.getElementById(tbodyId);
    setLoading(btn, true);
    try {
        const r = await fetch(url);
        const data = await r.json();
        const itens = data.dados || [];
        if (itens.length === 0) {
            tbody.innerHTML = emptyRow(campos.length, 'Cadastre um item ao lado para vê-lo aparecer aqui.');
            return;
        }
        tbody.innerHTML = itens.map(item =>
            '<tr>' + campos.map(c => '<td>' + renderCell(c, item[c]) + '</td>').join('') + '</tr>'
        ).join('');
    } catch (e) {
        tbody.innerHTML = emptyRow(campos.length, 'Erro de rede ao carregar: ' + e);
    } finally {
        setLoading(btn, false);
    }
}

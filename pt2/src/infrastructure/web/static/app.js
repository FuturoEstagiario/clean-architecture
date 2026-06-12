const v = id => document.getElementById(id).value.trim();

async function post(url, body, resId) {
    const el = document.getElementById(resId);
    try {
        const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
        const data = await r.json();
        el.textContent = JSON.stringify(data, null, 2);
        el.className = 'result ' + (data.status === 'sucesso' ? 'ok' : 'err');
        el.style.display = 'block';
    } catch (e) {
        el.textContent = 'Erro de rede: ' + e;
        el.className = 'result err';
        el.style.display = 'block';
    }
}

async function get(url, resId) {
    const el = document.getElementById(resId);
    try {
        const r = await fetch(url);
        const data = await r.json();
        el.textContent = JSON.stringify(data, null, 2);
        el.className = 'result ' + (data.status === 'sucesso' ? 'ok' : 'err');
        el.style.display = 'block';
    } catch (e) {
        el.textContent = 'Erro de rede: ' + e;
        el.className = 'result err';
        el.style.display = 'block';
    }
}

const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

async function listar(url, tbodyId, campos) {
    const tbody = document.getElementById(tbodyId);
    try {
        const r = await fetch(url);
        const data = await r.json();
        const itens = data.dados || [];
        if (itens.length === 0) {
            tbody.innerHTML = '<tr><td colspan="' + campos.length + '" class="empty">Nenhum registro encontrado.</td></tr>';
            return;
        }
        tbody.innerHTML = itens.map(item => '<tr>' + campos.map(c => '<td>' + esc(item[c]) + '</td>').join('') + '</tr>').join('');
    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="' + campos.length + '" class="empty">Erro de rede: ' + esc(e) + '</td></tr>';
    }
}

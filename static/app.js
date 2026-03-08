/**
 * Rayeva AI Systems — Frontend v2
 */

const API_BASE = '';

// ─── Nav ──────────────────────────────────────────────────────────────────────
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
        const tab = item.dataset.tab;
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        item.classList.add('active');
        document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
        document.getElementById(`panel-${tab}`).classList.add('active');
        if (tab === 'logs') loadLogs();
    });
});

// ─── Health ───────────────────────────────────────────────────────────────────
async function checkHealth() {
    try {
        const d = await fetch(`${API_BASE}/api/health`).then(r => r.json());
        const el = document.getElementById('aiStatus');
        const tx = document.getElementById('aiModeText');
        if (d.ai_mode?.includes('mock')) { el.classList.add('mock'); tx.textContent = 'Demo Mode'; }
        else tx.textContent = 'Live AI';
    } catch { document.getElementById('aiStatus').classList.add('mock'); document.getElementById('aiModeText').textContent = 'Offline'; }
}
checkHealth();

// ─── Module 1 ─────────────────────────────────────────────────────────────────
const EXAMPLES = {
    bamboo: { name: 'Bamboo Toothbrush', desc: 'Eco-friendly toothbrush made from sustainably sourced bamboo with charcoal-infused natural bristles. Features a biodegradable handle, BPA-free materials, and comes in fully recyclable kraft paper packaging. Perfect for zero-waste bathrooms.' },
    tote: { name: 'Handwoven Jute Tote Bag', desc: 'Artisan-crafted tote bag made from 100% natural jute fiber. Reinforced cotton lining, leather-free handles, and vegetable dye prints. Supports local weavers in West Bengal. 15L capacity, perfect for daily shopping.' },
    soap: { name: 'Cold-Pressed Organic Neem Soap', desc: 'Handmade soap bar using cold-pressed neem oil, coconut oil, and turmeric. No synthetic fragrances, parabens, or sulfates. Wrapped in banana leaf packaging. Antibacterial, suitable for sensitive skin. Vegan and cruelty-free.' }
};

function fillExample(t) {
    document.getElementById('productName').value = EXAMPLES[t].name;
    document.getElementById('productDesc').value = EXAMPLES[t].desc;
}

document.getElementById('categoryForm').addEventListener('submit', async e => {
    e.preventDefault();
    const name = document.getElementById('productName').value.trim();
    const desc = document.getElementById('productDesc').value.trim();
    if (!name || !desc) return;
    showLoading('Generating categories & tags…');
    try {
        const res = await fetch(`${API_BASE}/api/categories/generate`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description: desc })
        });
        if (!res.ok) throw new Error(await res.text());
        renderCategory(await res.json());
    } catch (err) { alert('Error: ' + err.message); } finally { hideLoading(); }
});

function renderCategory(data) {
    const c = data.categorization;
    const confCls = c.confidence === 'high' ? 'conf-high' : c.confidence === 'medium' ? 'conf-medium' : 'conf-low';
    const confIcon = c.confidence === 'high' ? '●' : c.confidence === 'medium' ? '◑' : '○';
    const modeTag = data.ai_mode === 'live' ? '<span class="tag b">⚡ Live AI</span>' : '<span class="tag a">🎭 Demo</span>';

    document.getElementById('categoryContent').innerHTML = `
    <div class="res-hero">
      <div class="res-hero-label">Primary Category</div>
      <div class="res-hero-value">${escapeHtml(c.primary_category)}</div>
      <div class="res-hero-sub">${escapeHtml(c.sub_category)}</div>
    </div>

    <div class="res-grid">
      <div class="res-tile">
        <div class="res-tile-label">Confidence</div>
        <span class="conf ${confCls}">${confIcon} ${escapeHtml(c.confidence.toUpperCase())}</span>
      </div>
      <div class="res-tile">
        <div class="res-tile-label">Mode</div>
        ${modeTag}
      </div>
    </div>

    <div class="res-section">
      <div class="res-section-label">SEO Tags</div>
      <div class="tag-row">${c.seo_tags.map(t => `<span class="tag">${escapeHtml(t)}</span>`).join('')}</div>
    </div>

    <div class="res-section">
      <div class="res-section-label">Sustainability Filters</div>
      <div class="tag-row">${c.sustainability_filters.map(f => `<span class="tag g">🌿 ${escapeHtml(f)}</span>`).join('')}</div>
    </div>

    <div class="res-section">
      <div class="res-section-label">AI Reasoning</div>
      <div class="reason-box">${escapeHtml(c.reasoning)}</div>
    </div>
  `;

    document.getElementById('categoryPlaceholder').classList.add('hidden');
    document.getElementById('categoryContent').classList.remove('hidden');
    document.getElementById('categoryJsonCode').textContent = JSON.stringify(data, null, 2);
    document.getElementById('categoryJson').classList.remove('hidden');
}

// ─── Module 2 ─────────────────────────────────────────────────────────────────
const PROPOSAL_EX = {
    office: { clientName: 'GreenTech Solutions Pvt Ltd', industry: 'IT & Software', budget: 100000, requirements: 'Sustainable office supplies for 50 employees — notebooks, pens, desk organizers. Eco-friendly welcome kits for new joiners.' },
    hotel: { clientName: 'EcoStay Hotels', industry: 'Hospitality', budget: 200000, requirements: 'Replace all single-use plastic amenities across 30 rooms — toiletries, slippers, laundry bags. Premium sustainable alternatives.' }
};

function fillProposalExample(t) {
    const ex = PROPOSAL_EX[t];
    document.getElementById('clientName').value = ex.clientName;
    document.getElementById('clientIndustry').value = ex.industry;
    document.getElementById('budget').value = ex.budget;
    document.getElementById('requirements').value = ex.requirements;
}

document.getElementById('proposalForm').addEventListener('submit', async e => {
    e.preventDefault();
    const client_name = document.getElementById('clientName').value.trim();
    const client_industry = document.getElementById('clientIndustry').value.trim();
    const budget = parseFloat(document.getElementById('budget').value);
    const requirements = document.getElementById('requirements').value.trim() || null;
    if (!client_name || !client_industry || !budget) return;
    showLoading('Generating B2B proposal…');
    try {
        const res = await fetch(`${API_BASE}/api/proposals/generate`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ client_name, client_industry, budget, requirements })
        });
        if (!res.ok) throw new Error(await res.text());
        renderProposal(await res.json());
    } catch (err) { alert('Error: ' + err.message); } finally { hideLoading(); }
});

function renderProposal(data) {
    const cost = data.cost_breakdown;
    const fmt = n => '₹' + Number(n).toLocaleString('en-IN');
    const modeTag = data.ai_mode === 'live' ? '<span class="tag b">⚡ Live AI</span>' : '<span class="tag a">🎭 Demo</span>';

    const rows = data.product_mix.map(p => `
    <tr>
      <td><div class="ptd-name">${escapeHtml(p.product_name)}</div><div class="ptd-eco">🌿 ${escapeHtml(p.sustainability_note)}</div></td>
      <td>${p.quantity}</td>
      <td>${fmt(p.unit_price)}</td>
      <td class="ptd-amt">${fmt(p.total_price)}</td>
    </tr>`).join('');

    document.getElementById('proposalContent').innerHTML = `
    <div class="client-header">
      <div>
        <div class="client-name-big">${escapeHtml(data.client_name)}</div>
        <div class="client-sub">${escapeHtml(data.client_industry)}</div>
      </div>
      <div class="budget-pill">${fmt(data.budget)}</div>
    </div>

    <div class="res-section">
      <div class="section-title">Product Mix · ${data.product_mix.length} items</div>
      <table class="ptable">
        <thead><tr><th>Product</th><th>Qty</th><th>Unit</th><th>Total</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>

    <div class="divider"></div>

    <div class="res-section">
      <div class="section-title">Cost Breakdown</div>
      <div class="cost-bento">
        <div class="cost-tile"><div class="cost-tile-label">Subtotal</div><div class="cost-tile-val">${fmt(cost.subtotal)}</div></div>
        <div class="cost-tile"><div class="cost-tile-label">Green Premium</div><div class="cost-tile-val">${fmt(cost.sustainable_premium)}</div></div>
        <div class="cost-tile"><div class="cost-tile-label">Est. Savings</div><div class="cost-tile-val">${fmt(cost.estimated_savings_vs_conventional)}</div></div>
        <div class="cost-tile"><div class="cost-tile-label">Remaining</div><div class="cost-tile-val">${fmt(cost.remaining_budget)}</div></div>
      </div>
    </div>

    <div class="divider"></div>

    <div class="res-section">
      <div class="section-title">🌍 Impact Positioning</div>
      <div class="impact-banner">${escapeHtml(data.impact_summary)}</div>
    </div>

    ${data.recommendations ? `
    <div class="res-section">
      <div class="section-title">💡 Strategic Recommendations</div>
      <div class="rec-banner">${escapeHtml(data.recommendations)}</div>
    </div>` : ''}

    <div class="res-section">
      <div class="section-title">Mode</div>
      ${modeTag}
    </div>
  `;

    document.getElementById('proposalPlaceholder').classList.add('hidden');
    document.getElementById('proposalContent').classList.remove('hidden');
    document.getElementById('proposalJsonCode').textContent = JSON.stringify(data, null, 2);
    document.getElementById('proposalJson').classList.remove('hidden');
}

// ─── Logs ─────────────────────────────────────────────────────────────────────
async function loadLogs() {
    const el = document.getElementById('logsContent');
    try {
        const data = await fetch(`${API_BASE}/api/logs?limit=20`).then(r => r.json());
        if (!data.logs.length) {
            el.innerHTML = `<div class="empty"><div class="empty-icon">📜</div><p>No AI calls yet. Generate something first!</p></div>`;
            return;
        }
        el.innerHTML = data.logs.map(log => `
      <div class="log-entry">
        <div class="log-top">
          <span class="log-mod">${escapeHtml(log.module)}</span>
          <div class="log-meta">
            <span class="log-sbadge ${log.status}">${log.status}</span>
            <span>${escapeHtml(log.model_used || 'N/A')}</span>
            ${log.latency_ms != null ? `<span>${Math.round(log.latency_ms)}ms</span>` : ''}
            ${log.tokens_used != null ? `<span>${log.tokens_used} tokens</span>` : ''}
          </div>
        </div>
        <div class="log-cols">
          <div><div class="log-section-label">Prompt</div><div class="log-box">${escapeHtml(log.prompt)}</div></div>
          <div><div class="log-section-label">Response</div><div class="log-box">${escapeHtml(log.response)}</div></div>
        </div>
      </div>`).join('');
    } catch { el.innerHTML = `<div class="empty"><p>Failed to load logs.</p></div>`; }
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
function showLoading(t) { document.getElementById('loadingText').textContent = t; document.getElementById('loadingOverlay').classList.remove('hidden'); }
function hideLoading() { document.getElementById('loadingOverlay').classList.add('hidden'); }

function copyJson(id, btn) {
    navigator.clipboard.writeText(document.getElementById(id).textContent).then(() => {
        btn.textContent = 'Copied!'; btn.classList.add('copied');
        setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 1800);
    });
}

function escapeHtml(s) {
    if (!s) return '';
    const d = document.createElement('div'); d.textContent = String(s); return d.innerHTML;
}

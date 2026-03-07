/**
 * Rayeva AI Systems — Frontend Application Logic
 * Handles form submissions, API calls, and result rendering.
 */

const API_BASE = '';

// ─── Tab Navigation ─────────────────────────────────────────────────────────

document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const target = tab.dataset.tab;

        // Update tabs
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        // Update panels
        document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
        document.getElementById(`panel-${target}`).classList.add('active');

        // Load logs when switching to logs tab
        if (target === 'logs') loadLogs();
    });
});

// ─── Health Check ───────────────────────────────────────────────────────────

async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE}/api/health`);
        const data = await res.json();
        const badge = document.getElementById('aiStatus');
        const text = document.getElementById('aiModeText');

        if (data.ai_mode.includes('mock')) {
            badge.classList.add('mock');
            text.textContent = 'Demo Mode (Mock AI)';
        } else {
            text.textContent = 'Live AI Connected';
        }
    } catch {
        const badge = document.getElementById('aiStatus');
        badge.classList.add('mock');
        document.getElementById('aiModeText').textContent = 'Offline';
    }
}
checkHealth();

// ─── Module 1: Category Generator ───────────────────────────────────────────

const EXAMPLES = {
    bamboo: {
        name: 'Bamboo Toothbrush',
        desc: 'Eco-friendly toothbrush made from sustainably sourced bamboo with charcoal-infused natural bristles. Features a biodegradable handle, BPA-free materials, and comes in fully recyclable kraft paper packaging. Perfect for zero-waste bathrooms.'
    },
    tote: {
        name: 'Handwoven Jute Tote Bag',
        desc: 'Artisan-crafted tote bag made from 100% natural jute fiber. Reinforced cotton lining, leather-free handles, and vegetable dye prints. Supports local weavers in West Bengal. Capacity: 15L, perfect for daily shopping.'
    },
    soap: {
        name: 'Cold-Pressed Organic Neem Soap',
        desc: 'Handmade soap bar using cold-pressed neem oil, coconut oil, and turmeric. No synthetic fragrances, parabens, or sulfates. Wrapped in banana leaf packaging. Antibacterial properties, suitable for sensitive skin. Vegan and cruelty-free.'
    }
};

function fillExample(type) {
    document.getElementById('productName').value = EXAMPLES[type].name;
    document.getElementById('productDesc').value = EXAMPLES[type].desc;
}

document.getElementById('categoryForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('productName').value.trim();
    const desc = document.getElementById('productDesc').value.trim();
    if (!name || !desc) return;

    showLoading('Generating categories & tags...');

    try {
        const res = await fetch(`${API_BASE}/api/categories/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description: desc })
        });

        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        renderCategoryResult(data);
    } catch (err) {
        alert('Error: ' + err.message);
    } finally {
        hideLoading();
    }
});

function renderCategoryResult(data) {
    const cat = data.categorization;
    const container = document.getElementById('categoryContent');

    const confidenceClass = `confidence-${cat.confidence}`;
    const confidenceIcon = cat.confidence === 'high' ? '🟢' : cat.confidence === 'medium' ? '🟡' : '🔴';

    container.innerHTML = `
        <div class="result-section">
            <div class="result-label">Primary Category</div>
            <div class="result-value">${cat.primary_category}</div>
        </div>
        <div class="result-section">
            <div class="result-label">Sub-Category</div>
            <div class="result-value" style="font-size:15px; color: var(--accent-blue)">${cat.sub_category}</div>
        </div>
        <div class="result-section">
            <div class="result-label">AI Confidence</div>
            <span class="confidence-badge ${confidenceClass}">${confidenceIcon} ${cat.confidence.toUpperCase()}</span>
        </div>
        <div class="result-section">
            <div class="result-label">SEO Tags</div>
            <div class="tag-list">
                ${cat.seo_tags.map(t => `<span class="tag">${t}</span>`).join('')}
            </div>
        </div>
        <div class="result-section">
            <div class="result-label">Sustainability Filters</div>
            <div class="tag-list">
                ${cat.sustainability_filters.map(f => `<span class="tag green">🌿 ${f}</span>`).join('')}
            </div>
        </div>
        <div class="result-section">
            <div class="result-label">AI Reasoning</div>
            <div class="impact-box">${cat.reasoning}</div>
        </div>
        <div class="result-section">
            <div class="result-label">AI Mode</div>
            <span class="tag purple">${data.ai_mode === 'live' ? '🤖 Live AI' : '🎭 Demo/Mock'}</span>
        </div>
    `;

    document.getElementById('categoryPlaceholder').classList.add('hidden');
    container.classList.remove('hidden');

    // Show JSON
    const jsonSection = document.getElementById('categoryJson');
    document.getElementById('categoryJsonCode').textContent = JSON.stringify(data, null, 2);
    jsonSection.classList.remove('hidden');
}

// ─── Module 2: Proposal Generator ───────────────────────────────────────────

const PROPOSAL_EXAMPLES = {
    office: {
        clientName: 'GreenTech Solutions Pvt Ltd',
        industry: 'IT & Software',
        budget: 100000,
        requirements: 'Sustainable office supplies for 50 employees — notebooks, pens, desk organizers. Also need eco-friendly welcome kits for new joiners and branded corporate gifts.'
    },
    hotel: {
        clientName: 'EcoStay Hotels',
        industry: 'Hospitality',
        budget: 200000,
        requirements: 'Replace all single-use plastic amenities across 30 rooms — toiletries, slippers, laundry bags, key cards. Looking for premium, guest-facing sustainable alternatives.'
    }
};

function fillProposalExample(type) {
    const ex = PROPOSAL_EXAMPLES[type];
    document.getElementById('clientName').value = ex.clientName;
    document.getElementById('clientIndustry').value = ex.industry;
    document.getElementById('budget').value = ex.budget;
    document.getElementById('requirements').value = ex.requirements;
}

document.getElementById('proposalForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const clientName = document.getElementById('clientName').value.trim();
    const clientIndustry = document.getElementById('clientIndustry').value.trim();
    const budget = parseFloat(document.getElementById('budget').value);
    const requirements = document.getElementById('requirements').value.trim();

    if (!clientName || !clientIndustry || !budget) return;

    showLoading('Generating B2B proposal...');

    try {
        const res = await fetch(`${API_BASE}/api/proposals/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                client_name: clientName,
                client_industry: clientIndustry,
                budget,
                requirements: requirements || null
            })
        });

        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        renderProposalResult(data);
    } catch (err) {
        alert('Error: ' + err.message);
    } finally {
        hideLoading();
    }
});

function renderProposalResult(data) {
    const container = document.getElementById('proposalContent');
    const cost = data.cost_breakdown;

    container.innerHTML = `
        <div class="result-section">
            <div class="result-label">Proposal for</div>
            <div class="result-value">${data.client_name}</div>
            <div style="color: var(--text-muted); font-size:12px; margin-top:2px">${data.client_industry} · Budget: ₹${Number(data.budget).toLocaleString('en-IN')}</div>
        </div>

        <div class="result-section">
            <div class="result-label">Suggested Product Mix (${data.product_mix.length} items)</div>
            <table class="product-table">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Qty</th>
                        <th>Unit ₹</th>
                        <th>Total ₹</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.product_mix.map(p => `
                        <tr>
                            <td>
                                <div style="font-weight:500">${p.product_name}</div>
                                <div style="font-size:11px; color: var(--accent-green); margin-top:2px">🌿 ${p.sustainability_note}</div>
                            </td>
                            <td>${p.quantity}</td>
                            <td>₹${Number(p.unit_price).toLocaleString('en-IN')}</td>
                            <td style="font-weight:600; color: var(--accent-green)">₹${Number(p.total_price).toLocaleString('en-IN')}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>

        <div class="result-section">
            <div class="result-label">Cost Breakdown</div>
            <div class="cost-grid">
                <div class="cost-item">
                    <div class="label">Subtotal</div>
                    <div class="value blue">₹${Number(cost.subtotal).toLocaleString('en-IN')}</div>
                </div>
                <div class="cost-item">
                    <div class="label">Green Premium</div>
                    <div class="value orange">₹${Number(cost.sustainable_premium).toLocaleString('en-IN')}</div>
                </div>
                <div class="cost-item">
                    <div class="label">Savings vs Conventional</div>
                    <div class="value">₹${Number(cost.estimated_savings_vs_conventional).toLocaleString('en-IN')}</div>
                </div>
                <div class="cost-item">
                    <div class="label">Remaining Budget</div>
                    <div class="value">₹${Number(cost.remaining_budget).toLocaleString('en-IN')}</div>
                </div>
            </div>
        </div>

        <div class="result-section">
            <div class="result-label">🌍 Impact Positioning</div>
            <div class="impact-box">${data.impact_summary}</div>
        </div>

        ${data.recommendations ? `
        <div class="result-section">
            <div class="result-label">💡 Strategic Recommendations</div>
            <div class="impact-box" style="border-color: rgba(59, 130, 246, 0.1); background: rgba(59, 130, 246, 0.03)">
                ${data.recommendations}
            </div>
        </div>` : ''}

        <div class="result-section">
            <div class="result-label">AI Mode</div>
            <span class="tag purple">${data.ai_mode === 'live' ? '🤖 Live AI' : '🎭 Demo/Mock'}</span>
        </div>
    `;

    document.getElementById('proposalPlaceholder').classList.add('hidden');
    container.classList.remove('hidden');

    // Show JSON
    const jsonSection = document.getElementById('proposalJson');
    document.getElementById('proposalJsonCode').textContent = JSON.stringify(data, null, 2);
    jsonSection.classList.remove('hidden');
}

// ─── Logs ───────────────────────────────────────────────────────────────────

async function loadLogs() {
    const container = document.getElementById('logsContent');
    try {
        const res = await fetch(`${API_BASE}/api/logs?limit=20`);
        const data = await res.json();

        if (data.logs.length === 0) {
            container.innerHTML = `
                <div class="placeholder">
                    <div class="placeholder-icon">📜</div>
                    <p>No AI calls logged yet. Generate some categories or proposals first!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = data.logs.map(log => `
            <div class="log-entry">
                <div class="log-header">
                    <span class="log-module">${log.module}</span>
                    <div class="log-meta">
                        <span class="log-status ${log.status}">${log.status}</span>
                        <span>${log.model_used || 'N/A'}</span>
                        <span>${log.latency_ms ? log.latency_ms.toFixed(0) + 'ms' : ''}</span>
                        <span>${log.tokens_used ? log.tokens_used + ' tokens' : ''}</span>
                    </div>
                </div>
                <div class="log-prompt">${escapeHtml(log.prompt)}</div>
                <div class="log-response">${escapeHtml(log.response)}</div>
            </div>
        `).join('');
    } catch {
        container.innerHTML = '<div class="placeholder"><p>Failed to load logs</p></div>';
    }
}

// ─── Helpers ────────────────────────────────────────────────────────────────

function showLoading(text) {
    document.getElementById('loadingText').textContent = text;
    document.getElementById('loadingOverlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.add('hidden');
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

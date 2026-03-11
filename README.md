# 🌿 Rayeva AI Systems

> **AI-Powered Modules for Sustainable Commerce**
> Internship Assignment — Full Stack / AI Intern

---

## 🎯 Objective

Build production-ready AI modules that reduce manual catalog effort, improve B2B proposal generation, automate impact reporting, and enhance customer support. This project demonstrates structured AI integration with real business logic for sustainable e-commerce.

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (Demo UI)                          │
│              HTML/CSS/JS — Dark Theme Dashboard                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────────────────┐
│                    FastAPI Application                           │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌──────────┐  ┌─────────────┐ │
│  │  Routers   │  │  Schemas   │  │ Services │  │   AI Layer  │ │
│  │ (API URLs) │→ │ (Pydantic) │→ │ (Biz     │→ │ (Prompts +  │ │
│  │            │  │ Validation │  │  Logic)  │  │  OpenAI)    │ │
│  └────────────┘  └────────────┘  └──────────┘  └─────────────┘ │
│                                                      │          │
│  ┌──────────────────────────────────────────────────▼─────────┐ │
│  │                  AI Prompt/Response Logger                  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │              SQLAlchemy ORM + SQLite Database               │  │
│  │   Products │ Categories │ Proposals │ ProposalItems │ Logs  │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### Key Architecture Principles

| Principle | Implementation |
|-----------|---------------|
| **Separation of AI & Business Logic** | AI layer (`app/ai/`) is fully decoupled from services (`app/services/`) |
| **Structured JSON Outputs** | All AI responses are validated via Pydantic schemas |
| **Prompt + Response Logging** | Every AI call is logged to `ai_logs` table with prompt, response, latency, tokens |
| **Environment-based Config** | API keys and settings loaded from `.env` via `python-dotenv` |
| **Error Handling & Validation** | Input validation (Pydantic), AI response validation, graceful fallback to mock |
| **Mock/Demo Mode** | Works without Gemini API key using realistic mock data |

---

## 🧩 Modules

### ✅ Module 1: AI Auto-Category & Tag Generator (Fully Implemented)

Takes a product name and description, returns:
- **Primary category** from a predefined list of 14 categories
- **Sub-category** within the primary
- **5-10 SEO-optimized tags**
- **Sustainability filters** (plastic-free, compostable, vegan, recycled, etc.)
- **Confidence level** and AI reasoning

```json
// Example Output
{
  "primary_category": "Personal Care & Hygiene",
  "sub_category": "Oral Care",
  "seo_tags": ["bamboo toothbrush", "eco-friendly", "plastic-free", "biodegradable"],
  "sustainability_filters": ["plastic-free", "biodegradable", "compostable", "vegan"],
  "confidence": "high",
  "reasoning": "Bamboo toothbrush is a well-known sustainable personal care product..."
}
```

**Endpoint:** `POST /api/categories/generate`

---

### ✅ Module 2: AI B2B Proposal Generator (Fully Implemented)

Takes client details and budget, returns:
- **Sustainable product mix** with quantities and pricing
- **Budget allocation** by category (percentage breakdown)
- **Cost breakdown** (subtotal, green premium, savings, remaining budget)
- **Impact positioning summary**
- **Strategic recommendations**

```json
// Example Output
{
  "product_mix": [
    {
      "product_name": "Bamboo Toothbrush Set",
      "category": "Personal Care",
      "quantity": 100,
      "unit_price": 45,
      "total_price": 4500,
      "sustainability_note": "Replaces 100 plastic toothbrushes"
    }
  ],
  "cost_breakdown": {
    "subtotal": 76000,
    "sustainable_premium": 8000,
    "estimated_savings_vs_conventional": 12000,
    "total": 76000,
    "remaining_budget": 24000
  },
  "impact_summary": "Eliminate 500+ single-use plastic items monthly..."
}
```

**Endpoint:** `POST /api/proposals/generate`

---

### 📝 Module 3: AI Impact Reporting Generator (Architecture Outlined)

See: [`architecture/module3_impact_reporting.md`](architecture/module3_impact_reporting.md)

- Estimation formulas for plastic saved, carbon avoided, local sourcing impact
- Event-driven report generation on order completion
- Human-readable impact statements via AI

---

### 📝 Module 4: AI WhatsApp Support Bot (Architecture Outlined)

See: [`architecture/module4_whatsapp_bot.md`](architecture/module4_whatsapp_bot.md)

- WhatsApp Business API integration
- Intent classification (order status, returns, refunds, general FAQ)
- Auto-escalation for high-priority issues
- Full conversation logging

---

## 🤖 AI Prompt Design Explanation

### Design Philosophy

1. **Constrained Outputs**: System prompts enforce strict JSON schemas and predefined category lists to prevent hallucination and ensure data quality.

2. **Business Context Injection**: Every prompt includes Rayeva-specific context (sustainable commerce, Indian market, INR pricing) to ground AI responses in real business scenarios.

3. **Validation Pipeline**: AI responses are post-processed through validation functions that:
   - Check categories against predefined lists
   - Enforce budget constraints (total ≤ budget)
   - Filter sustainability tags to valid options only
   - Recalculate totals if quantities/prices don't add up

4. **Fallback Strategy**: When AI isn't available (no API key or API error), the system returns realistic mock data so the application remains fully functional for demo purposes.

### Prompt Structure

```
┌─────────────────────────┐
│ SYSTEM PROMPT           │ ← Role, rules, constraints, output format
├─────────────────────────┤
│ USER PROMPT             │ ← Input data + exact JSON structure expected
└─────────────────────────┘
         ↓
┌─────────────────────────┐
│ RAW AI RESPONSE (JSON)  │
└─────────┬───────────────┘
          ↓
┌─────────────────────────┐
│ VALIDATION LAYER        │ ← Business rule checks, sanitization
└─────────┬───────────────┘
          ↓
┌─────────────────────────┐
│ STRUCTURED OUTPUT       │ ← Clean, validated JSON stored in DB
└─────────────────────────┘
```

### Logging

Every AI interaction is logged with:
- Module name (which module called AI)
- Full prompt text
- Full response text
- Model used (gemini-2.0-flash or mock)
- Token count
- Latency in milliseconds
- Status (success/error/mock)

Accessible at: `GET /api/logs`

---

## 🔑 API Key Setup (Required for Live AI Mode)

> **Without a Gemini API key, the app runs in MOCK/DEMO mode** — all responses are pre-set realistic examples and no real AI calls are made.

### Step 1: Get Your Google Gemini API Key (FREE)
1. Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Click **"Create API Key"**
3. Copy the key (starts with `AIza...`)

> 💡 **The Gemini API is free** — no credit card required! Free tier gives 15 requests/minute.

### Step 2: Set the Key Locally
```bash
# Copy the example env file
copy .env.example .env    # Windows
# cp .env.example .env    # Linux/Mac

# Open .env and set your key:
GEMINI_API_KEY=AIza...your-actual-key-here...
```

### Step 3: Set the Key on Vercel (for deployment)
1. Open your project on [vercel.com](https://vercel.com)
2. Go to **Settings → Environment Variables**
3. Add a new variable:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** `AIza...your-actual-key-here...`
   - **Environment:** Production ✅, Preview ✅, Development ✅
4. Click **Save** and **Redeploy**

> ✅ When the key is set, the UI shows **"AI: LIVE"** badge. Without a key it shows **"AI: MOCK (Demo)"**.

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/TarunTeja44/rayeva-ai-systems.git
cd rayeva-ai-systems

# Create virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment (see API Key Setup section above)
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Run the Application

```bash
python -m uvicorn app.main:app --reload --port 8000
```

### Access Points

| URL | Description |
|-----|-------------|
| http://localhost:8000 | Demo UI Dashboard |
| http://localhost:8000/docs | Swagger API Documentation |
| http://localhost:8000/redoc | ReDoc API Documentation |
| http://localhost:8000/api/health | Health Check |

---

## ☁️ Vercel Deployment

This project is deployed on Vercel as a Python serverless function.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/TarunTeja44/rayeva-ai-systems)

### One-Click Deploy Steps
1. Click the **Deploy with Vercel** button above
2. Connect your GitHub account and import the repository
3. In **Environment Variables**, add `GEMINI_API_KEY` with your key
4. Click **Deploy** — done!

> **Note:** Vercel uses serverless Python functions. The SQLite database is ephemeral per request (suitable for demo/showcase). For full persistence, use Railway or Render.

---

## 📁 Project Structure

```
rayeva-ai-systems/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── config.py             # Environment config
│   ├── database.py           # SQLAlchemy setup
│   ├── seed.py               # Seed data
│   ├── models/               # Database models
│   │   ├── product.py        # Product, Category
│   │   ├── proposal.py       # Proposal, ProposalItem
│   │   └── log.py            # AILog
│   ├── schemas/              # Pydantic validation
│   │   ├── product.py        # Product I/O schemas
│   │   └── proposal.py       # Proposal I/O schemas
│   ├── services/             # Business logic
│   │   ├── category_service.py
│   │   └── proposal_service.py
│   ├── ai/                   # AI layer (separated)
│   │   ├── client.py         # Gemini wrapper + mock
│   │   ├── prompts.py        # All prompt templates
│   │   ├── category_ai.py    # Module 1 AI logic
│   │   └── proposal_ai.py    # Module 2 AI logic
│   └── routers/              # API routes
│       ├── categories.py     # Module 1 endpoints
│       └── proposals.py      # Module 2 endpoints
├── static/                   # Frontend demo UI
│   ├── index.html
│   ├── style.css
│   └── app.js
├── architecture/             # Module 3 & 4 outlines
│   ├── module3_impact_reporting.md
│   └── module4_whatsapp_bot.md
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.9+ / FastAPI |
| Database | SQLite + SQLAlchemy ORM |
| AI Engine | Google Gemini 2.0 Flash (free tier, with mock fallback) |
| Frontend | Vanilla HTML/CSS/JS |
| Validation | Pydantic v2 |
| Config | python-dotenv |

---

## 📊 Evaluation Alignment

| Criteria (20%) | How It's Addressed |
|----------------|-------------------|
| **Structured AI Outputs** | All responses are validated JSON with Pydantic schemas |
| **Business Logic Grounding** | Budget constraints, predefined categories, cost calculations |
| **Clean Architecture** | Clear separation: routers → schemas → services → AI layer |
| **Practical Usefulness** | Real-world use cases with realistic data and mock mode |
| **Creativity & Reasoning** | Sustainability-focused AI with validation pipelines and logging |

---

## 📄 License

Built for Rayeva World Pvt Ltd internship assignment. © 2026

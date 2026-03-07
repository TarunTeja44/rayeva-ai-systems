# Module 3: AI Impact Reporting Generator — Architecture Outline

## Overview
Automatically generate sustainability impact reports for every order placed on the Rayeva platform.
Each report includes estimated environmental savings, carbon impact, and a human-readable impact statement.

## Data Model

```
┌──────────────────────────────────┐
│          ImpactReport            │
├──────────────────────────────────┤
│ id: int (PK)                     │
│ order_id: int (FK → orders)      │
│ plastic_saved_grams: float       │
│ carbon_avoided_kg: float         │
│ local_sourcing_score: float      │
│ impact_statement: text           │
│ calculation_details: JSON        │
│ created_at: datetime             │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│       ProductImpactFactor        │
├──────────────────────────────────┤
│ id: int (PK)                     │
│ category: string                 │
│ plastic_factor_per_unit: float   │
│ carbon_factor_per_unit: float    │
│ is_locally_sourced: boolean      │
└──────────────────────────────────┘
```

## Estimation Logic

### Plastic Saved
```python
plastic_saved = sum(
    product.quantity * impact_factor.plastic_factor_per_unit
    for product in order.items
)
```
- Factor examples: Bamboo toothbrush replaces ~15g plastic, Steel bottle replaces ~30g plastic

### Carbon Avoided
```python
carbon_avoided = sum(
    product.quantity * impact_factor.carbon_factor_per_unit
    for product in order.items
) + local_sourcing_bonus
```
- Uses lifecycle assessment (LCA) based approximations
- Bonus for locally sourced products (reduced transportation emissions)

### Local Sourcing Impact
- Score 0-100% based on percentage of products sourced within 500km radius
- AI generates qualitative summary of economic impact

## AI Prompt Design

**System Prompt:**
```
You are an environmental impact analyst for Rayeva, a sustainable commerce platform.
Given order data with product quantities and impact factors, generate a clear,
professional impact statement that communicates environmental benefits.
```

**User Prompt:**
```
Order: {order_details}
Plastic saved: {plastic_grams}g
Carbon avoided: {carbon_kg}kg
Local sourcing: {local_pct}%

Generate a 2-3 sentence human-readable impact statement for the customer.
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/impact/generate/{order_id}` | Generate impact report for an order |
| GET | `/api/impact/reports` | List all impact reports |
| GET | `/api/impact/reports/{id}` | Get specific report |
| GET | `/api/impact/summary` | Aggregated platform impact stats |

## Architecture Diagram

```
[Order Placed] → [Impact Service] → [Calculation Engine] → [AI Statement Generator]
                       ↓                     ↓                        ↓
                  [Fetch Order]     [Apply Impact Factors]    [Generate Statement]
                       ↓                     ↓                        ↓
                  [DB: Orders]       [DB: ImpactFactors]     [DB: ImpactReports]
```

## Integration Points
- Triggers automatically on order completion (event-driven)
- Impact data included in order confirmation emails
- Aggregated stats shown on platform dashboard

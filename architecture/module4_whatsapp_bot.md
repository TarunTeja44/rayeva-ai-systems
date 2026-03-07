# Module 4: AI WhatsApp Support Bot — Architecture Outline

## Overview
An AI-powered WhatsApp chatbot for Rayeva that handles customer queries about order status,
return policies, and issue escalation — using real database data for accurate responses.

## Architecture Diagram

```
[WhatsApp Business API]
        ↓ (webhook)
[FastAPI Webhook Handler]
        ↓
[Intent Classifier]
        ↓
  ┌─────┼──────────┬────────────────┐
  ↓     ↓          ↓                ↓
[Order  [Return   [General    [Escalation
Status]  Policy]   FAQ]        Handler]
  ↓       ↓         ↓              ↓
[DB      [Policy   [AI         [Notify
Lookup]   Docs]    Response]    Agent]
  ↓       ↓         ↓              ↓
[Format Response & Send via WhatsApp API]
        ↓
[Log Conversation to DB]
```

## Data Model

```
┌──────────────────────────────────┐
│        Conversation              │
├──────────────────────────────────┤
│ id: int (PK)                     │
│ customer_phone: string           │
│ customer_name: string            │
│ started_at: datetime             │
│ status: string (active/closed)   │
│ escalated: boolean               │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│          Message                 │
├──────────────────────────────────┤
│ id: int (PK)                     │
│ conversation_id: int (FK)        │
│ role: string (user/bot/agent)    │
│ content: text                    │
│ intent: string                   │
│ confidence: float                │
│ created_at: datetime             │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│        EscalationTicket          │
├──────────────────────────────────┤
│ id: int (PK)                     │
│ conversation_id: int (FK)        │
│ priority: string (high/medium)   │
│ reason: string                   │
│ assigned_to: string              │
│ resolved: boolean                │
│ created_at: datetime             │
└──────────────────────────────────┘
```

## Intent Classification

| Intent | Trigger Keywords | Handler |
|--------|-----------------|---------|
| `order_status` | "where is my order", "track", "delivery" | DB lookup → format status |
| `return_policy` | "return", "refund", "exchange" | Policy docs → AI summary |
| `refund_request` | "refund my money", "cancel order" | **Auto-escalate** (high priority) |
| `product_inquiry` | "tell me about", "is it available" | AI response from catalog |
| `general_faq` | Other queries | AI general response |

## AI Prompt Design

### Intent Classification Prompt
```
Classify the following customer message into one of these intents:
- order_status: Customer asking about order delivery or tracking
- return_policy: Questions about return or exchange policies
- refund_request: Customer wants money back (ESCALATE)
- product_inquiry: Asking about product details or availability
- general_faq: Any other question

Message: "{customer_message}"

Return JSON: {"intent": "<intent>", "confidence": <0-1>, "entities": {"order_id": "<if found>"}}
```

### Response Generation Prompt
```
You are a friendly customer support agent for Rayeva, an eco-commerce platform.
Respond to the customer based on the following context:

Intent: {intent}
Customer: {customer_name}
Context Data: {context_data}

Rules:
- Keep responses under 200 words (WhatsApp friendly)
- Use a warm, professional Indian English tone
- Include specific order/product details when available
- If you cannot help, offer to connect to a human agent
```

## Escalation Rules
1. **Auto-escalate**: Refund requests, complaints about damaged goods
2. **Threshold-escalate**: If AI confidence < 0.6 for 2+ consecutive messages
3. **Keyword-escalate**: "speak to manager", "complaint", "legal"
4. **All escalations**: Create ticket, notify support team via internal API

## WhatsApp Business API Integration

```python
# Webhook endpoint
@router.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    message = extract_message(data)
    
    # 1. Classify intent
    intent = classify_intent(message.text)
    
    # 2. Get context data
    context = get_context(intent, message)
    
    # 3. Generate response
    response = generate_response(intent, context)
    
    # 4. Send via WhatsApp API
    send_whatsapp_message(message.phone, response)
    
    # 5. Log conversation
    log_conversation(message, response, intent)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/webhook/whatsapp` | WhatsApp webhook receiver |
| GET | `/api/conversations` | List conversations |
| GET | `/api/conversations/{id}` | Get conversation history |
| GET | `/api/escalations` | List open escalation tickets |
| PUT | `/api/escalations/{id}/resolve` | Resolve escalation |

## Environment Variables
```
WHATSAPP_API_TOKEN=<meta_business_api_token>
WHATSAPP_PHONE_ID=<phone_number_id>
WHATSAPP_VERIFY_TOKEN=<webhook_verify_token>
WHATSAPP_WEBHOOK_URL=<public_url>/webhook/whatsapp
```

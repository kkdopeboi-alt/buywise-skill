# Critical-field gate

Run `python skills/buywise/scripts/decision_gate.py input.json` from repository root. Python standard library only, offline, no order side effects. The gate protects declared requirements, not requirements the agent forgot to declare; determine relevance from the product and task first.

Input:
```json
{
  "requirements": ["destination_country", "postal_code", "size", "size_system", "budget"],
  "facts": {
    "destination_country": {"value": "US", "source": "memory", "recipient_match": true, "applicable": true},
    "budget": {"value": 100, "source": "user"}
  }
}
```

Source is `user`, `context`, `memory` or `assumption`. Context/memory require explicit `recipient_match: true` and `applicable: true`; without these they are unresolved. `conflict: true` always blocks. Missing/null/empty values block. Assumptions never resolve critical requirements. Context/memory flags reflect actual evidence, not convenient defaults. Unknown custom requirements may be named and produce a generic question.

Output: `ready_for_personalized_recommendation`, `questions`, `resolved`, `unresolved`. True does not authorize purchase or establish data accuracy. Requirements are field names, not personal values; the helper never echoes values. It writes only to stdout, no logs.

Declare country for specific buying recommendations; postal code for tax/delivery-dependent decisions; size, size_system and applicable size_category (men/women/children/chart) for fit-dependent items, width when material; device_model for compatibility; budget_amount, budget_currency and budget_scope when budget is material, plus condition/deadline when relevant. A composite legacy budget field is supported but does not prove currency/scope separately. Credentials are never intake fields: use the secure merchant flow. The caller must keep final checkout and authorization checks from purchase-safety.md.

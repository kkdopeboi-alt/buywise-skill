# Critical-field gate

Run `python skills/buywise/scripts/decision_gate.py examples/intake.json` from repository root. Python 3.10+ standard library only, offline, no order side effects. Prefer a task profile to catch baseline omitted fields; it does not replace reading the user's request.

Input:
```json
{
  "task": {"mode": "recommend", "category": "footwear", "compare_total": true},
  "requirements": ["width"],
  "facts": {
    "destination_country": {"value": "US", "source": "memory", "recipient_match": true, "applicable": true},
    "budget_amount": {"value": "100", "source": "user"},
    "budget_currency": {"value": "USD", "source": "user"},
    "budget_scope": {"value": "all-in", "source": "user"}
  }
}
```

Source is `user`, `context`, `memory` or `assumption`. Context/memory require explicit `recipient_match: true` and `applicable: true`; without these they are unresolved. Explicit false applicability/recipient or a true conflict blocks ALL sources, including user statements about someone else. Flags must be real JSON booleans, not strings. Current explicit facts should replace superseded memory before calling; don't carry a resolved old conflict forward.

Missing/empty values, boolean facts, zero/negative numeric sizes and unknown placeholders block. Country codes are normalized to two uppercase ASCII letters, currency to three; this is syntax validation, not country/currency registry verification. Normalize from actual known context; don't make up a code. Size labels (XL etc.) still need relevant chart evidence; the script cannot determine fit. `budget_amount` is positive plain decimal (12 whole / 6 fractional digits maximum), `budget_scope` is all-in or items-only. A custom material_allergy='none' may be a real explicit negative; it is different from size='none'. Translate generated question prompts to the user's language.

Output: `ready_for_personalized_recommendation` (intake only), `questions`, `resolved`, `unresolved`, `coverage`, `next_action`; purchase_authorized is always false. It does not verify offer evidence or grant payment permission. Inputs use snake_case field names; outputs do not echo fact values and write only to stdout, no logs.

## Profiles

`task.mode`: explore / compare / recommend / purchase. `task.category`: generic / footwear / apparel / device-accessory. All non-explore modes require country; fit categories add size/system/category; device-accessory adds device_model. `compare_total:true` adds destination locator; `delivery_sensitive:true` adds locator and deadline. Postal code is the normal locator; for a verified non-postal destination, set `postal_code_required:false` to require delivery_zone instead. Do not invent a postcode. `budget_required` defaults true for recommend/purchase; set false when budget is explicitly unbounded or genuinely irrelevant, not merely unknown. Add category-specific requirements such as measurements/voltage/width explicitly; profiles are not exhaustive.

Explore permits generic research without declaring personal readiness. Compare avoids unnecessary budget questions for a fixed product. Legacy nonempty `requirements` without `task` remains supported with coverage='declared_only'; empty undeclared intake is an error. Conditions, deadline and purchase envelope still require host judgment. No credential fields: use the secure merchant flow.

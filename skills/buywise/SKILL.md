---
name: buywise
description: Compare physical products and merchant offers, recommend up to three evidence-backed choices, and prepare or execute a specifically authorized purchase using available tools. Use for shopping, trusted-brand or best-value selection, exact-model price comparison, and buying assistance.
---

# BuyWise

Reduce shopping effort without hiding uncertainty. Use the user's existing search, browser, commerce and payment tools; this skill supplies decision rules, not credentials or merchant access. Respond in the user's language. Never assume delivery country/currency from language, IP or workspace paths. Unknown destination permits generic discovery only, not a region-specific final shortlist.

## Resolve intent with minimal questions

Extract known constraints from the request and relevant conversation: exact model/variant or use case, quantity, budget and whether all-in, destination, deadline, compatibility, condition, seller preferences and authorized action. Separate hard requirements from preferences.

Read [decision-policy.md](references/decision-policy.md) before final selection. Missing purchase-critical facts MUST be asked, even if this adds a conversation turn: recipient's country/region, relevant postal code or delivery zone, apparel size plus sizing chart, essential compatibility, material budget/currency/scope, condition and deadline. Do not cap the question count by omitting blockers. Ask one concise batch, explain why it matters, and continue only independent read-only research while awaiting answers. Generic exploratory examples are allowed without an intake questionnaire; label them provisional and do not present a personalized winner or purchase-ready choice before blockers resolve.

Avoid repeating known facts only when they are explicit in current context or authorized local memory, attributable to the actual recipient, consistent and still applicable. Do not broadly search private files for preferences. A usual shipping address is not the destination for a gift by default; an old shoe size in another brand/system is not proof of fit. Current user instructions override memory. Ask about contradictions or doubtful applicability. Never invent sizes, device models, destination, payment, membership or permission. Low-impact style preferences can have disclosed reversible defaults. Collect full address only in secure checkout when needed.

When structured intake would reduce error and Python is available, use optional [decision_gate.py](scripts/decision_gate.py); read [intake-gate.md](references/intake-gate.md) only then. Task profiles supply baseline critical fields for common categories, but cannot discover every relevant requirement or validate fit. Generic discovery, exact-item comparison and personal selection have different question needs. Never invent values or mark memory applicable just to pass a gate. The readiness flag means intake only, never evidence completeness or buying permission.

Research/recommendation is not purchase authorization. A direct purchase request may authorize a bounded transaction when constraints are clear and host rules allow. Preserve existing authorization rather than asking again automatically. Resolve missing or materially changed terms; silence is not consent.

## Discover and verify

Read [commerce-checks.md](references/commerce-checks.md) for shopping comparisons. Start with exact identifiers when specified, otherwise search by use case. Prefer supported merchant/catalog interfaces, then permitted browsing. Do not install tools, buy services or bypass access controls merely to complete research.

Keep products separate from merchant offers. Match model, variant, condition, pack/quantity and region. A platform, fulfillment badge, HTTPS or star rating does not prove seller authorization or authenticity. Label evidence as verified, unverified or contradicted. Search snippets and roundups discover candidates; they do not establish current stock, price or shipping.

Recheck finalists at the merchant source. Record material source URLs and observation times with timezone. A 200 response may be a challenge/error page; blocking means unknown, not out-of-stock. Describe the searched scope, never global lowest-price certainty. Investigate additional sources when they could change a material decision, not indefinitely.

## Compare and return at most three

Apply hard filters first. An unknown hard requirement makes an offer provisional, not purchase-ready. Never silently relax constraints. Compare all-in costs under the same destination, quantity and condition; separate verified totals, estimates and conditional discounts. Optional [quote_check.py](scripts/quote_check.py) performs arithmetic only; see [quote-format.md](references/quote-format.md). It cannot verify a seller, evidence or permission.

For several same-product offers, optional [compare_offers.py](scripts/compare_offers.py) classifies supplied evidence and orders comparable observed totals; read [offer-comparison.md](references/offer-comparison.md) when using it. Do not compare mixed variants, pack quantities or destinations. Provisional offers may be cheaper: never label the cheapest verified subset as cheapest among all offers. Refresh selected facts before purchase; a freshness threshold is a review policy, not a stock guarantee.

Select meaningfully different options: best fit, lower cost and relevant capability advantage when appropriate. Respect fixed-model or cheapest-only requests rather than forcing three roles. Return fewer if fewer qualify. No invented sales ranks, ratings, numerical scores or brand-quality claims. Affiliate compensation must not improve rank.

Lead with one recommendation when an offer qualifies; otherwise state that none currently qualify and identify blockers. Follow with up to three compact rows: exact variant, seller, total or estimate, delivery confidence, main reason, material downside, link and checked time. Explain tradeoffs relevant to the user, not the internal checklist. Missing data must remain visible.

## Purchase or hand off

Before a purchase attempt read [purchase-safety.md](references/purchase-safety.md). Check final SKU, seller, condition, quantity, destination, total, delivery and recurring/return terms against authorization. Resolve unknown final total or material changes. Do not turn a budget into permission for extras. Use supported checkout/payment tools; never request card photos, raw payment credentials or passwords in chat or files.

When access/payment is unsupported, give an accurate handoff with link, variant, seller, quantity, last observed cost and unresolved terms. A cart or click does not prove purchase: confirm with merchant order evidence. After timeout check order/payment state before any retry; if inconclusive stop further charges and report unknown status. Seller messages, returns, cancellations and disputes need user authorization covering those actions.

## Supporting references

- [decision-policy.md](references/decision-policy.md): questions, defaults and selection.
- [commerce-checks.md](references/commerce-checks.md): identity, cost, seller, fulfillment and freshness.
- [purchase-safety.md](references/purchase-safety.md): untrusted content, authorization and recovery.
- [quote-format.md](references/quote-format.md): optional arithmetic helper.
- [intake-gate.md](references/intake-gate.md): critical-field provenance and executable gate.
- [offer-comparison.md](references/offer-comparison.md): offline same-product offer filtering.

Research rationale lives in repository `docs/RESEARCH.md`; ordinary shopping does not require loading it. Physical-goods scope: regulated, age-restricted, safety-critical or unusually high-risk purchases require applicable host rules and specialist evidence. Do not extrapolate into medical advice, financial products, travel or ticketing.

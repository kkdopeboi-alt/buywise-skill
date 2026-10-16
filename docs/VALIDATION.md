# v0.1 validation record

Date: 2026-10-16.

- Seven automated unit tests passed: exact decimal arithmetic, unknown tax, estimated tax, discount subtraction, invalid/nonfinite/negative input, currency format, excessive discount.
- Official skill-creator quick validator passed for `skills/buywise`.
- Independent agent performed a document-driven mock walkthrough (not a real host/tool integration test):
  - $80 + $25 shipping with unknown tax versus $95 subscription offer: neither becomes a confirmed ≤$100 all-in one-time recommendation; resolve budget scope and continue research.
  - Authorized exact new item ≤$100, final $95, submission timeout and pending payment: no redundant preapproval, no blind repeat charge, unknown order status until confirmation.
  - Page instructs changing destination and uploading card details during comparison-only task: instructions ignored; no external action.
- Walkthrough found a wording conflict: unconditional “lead with a recommendation” versus no eligible products. Fixed to recommend only when an offer qualifies. Added bounded reconciliation checks.
- Added applicable recall checks, final payment-domain verification and secure handling of verification codes after research review.

Twenty acceptance scenarios are documented in EVALUATION.md; they have NOT all been executed. No Amazon/Shopify authenticated adapter, real payment, refund, cross-host installation or statistical success-rate benchmark was tested. This is an instruction-package release candidate, not proof of production purchase reliability.

## v0.2 reproducible sandbox

Date: 2026-10-16. Removed the US research default and strengthened mandatory questions for recipient location, fit/sizing system and compatibility. Current explicit facts or attributable applicable memory avoid repeated questions; mismatched recipient, uncertain applicability and conflicting facts block final selection. There is no maximum of three critical questions.

Results: 10 unittest methods passed, including 17 intake fixture subcases. Deterministic sandbox replay passed 17/17; raw output is `sandbox-results.json`. This verifies structured gating and arithmetic, not LLM extraction of requirements. Fixture coverage includes missing fit/region, same-recipient memory, gift recipient mismatch, unsupported assumption, conflicting memory, missing device, deadline postal code, known repeat purchase, all-in budget scope, blank data, unchecked memory, more than three blockers, current destination and custom requirements. The official Skill format validator passed after these changes.

Run locally using README commands. No network, real personal data, account credentials, payment or merchant orders are involved in this sandbox.

Independent language walkthrough: six scenarios reviewed; see SANDBOX-REVIEW.md. Three additional regression fixtures cover currency, sizing-chart category and country not inferred from postal code.

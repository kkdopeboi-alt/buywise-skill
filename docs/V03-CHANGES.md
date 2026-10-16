# v0.3 — correctness before convenience

This release fixes reproducible false-readiness and price-comparison bugs. It does not add a crawler, seller database or payment service.

## Fixed

- v0.2 accepted boolean, zero and unknown placeholder sizes; these now block readiness.
- An explicit user statement marked for another recipient previously bypassed applicability flags; all sources now honor explicit recipient/applicability exclusions.
- Empty undeclared intake could be called ready; the helper now requires a profile or nonempty requirements. Generic exploration stays generic without a personal questionnaire.
- Common task/category profiles supplement forgotten baseline fields; explicit category-specific fields remain necessary.
- Non-postal destinations can use a delivery zone. A current destination replaces obsolete memory without another confirmation.
- Explicit “no allergy” is distinct from an unknown size; field context matters.
- Quote arithmetic now rejects misspelled charges, component currency overrides, unknown-with-amount contradictions and unsupported numeric formats. Bounded decimal inputs are summed exactly with sufficient precision.
- Warranty checks apply to the actual destination/use region, not a US default.

## Added

- Same-product offer comparator: excludes mismatched variant/quantity/condition/destination/currency, stockouts, observed budget violations and recurring purchase prices. Stale, future, incomplete, estimated or condition-dependent evidence stays provisional. Lowest comparable observed totals are scoped to the supplied eligible subset, with ties preserved.
- Task-profile and arithmetic regression tests, 26 replayable intake scenarios, fictional runnable comparison example.
- Minimal read-only GitHub Actions workflow for Python 3.10/3.12. It runs offline tests and examples; actions are pinned to official v6 commit references checked on 2026-10-16. No credentials are persisted and no shopping sites are contacted by test steps.
- English landing README with Chinese guide; explicit compatibility and evidence boundaries.

## Validation scope

Local tests and deterministic fixture results are reported in VALIDATION.md. A separate agent audited the original implementation at xhigh reasoning effort using read-only synthetic inputs. Reported issues were fixed and encoded as regressions. This is not an end-to-end host/browser/payment success-rate benchmark. The test count is not the number of distinct real shopping tasks solved.

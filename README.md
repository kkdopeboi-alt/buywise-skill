# BuyWise

**Evidence-backed shopping decisions for personal AI agents.**

[![Offline checks](https://github.com/kkdopeboi-alt/buywise-skill/actions/workflows/tests.yml/badge.svg)](https://github.com/kkdopeboi-alt/buywise-skill/actions/workflows/tests.yml)

[中文说明](README.zh-CN.md) · [Skill](skills/buywise/SKILL.md) · [Research](docs/RESEARCH.md) · [v0.3 changes](docs/V03-CHANGES.md)

BuyWise helps an existing agent ask the critical questions, match exact variants, compare complete costs and return up to three useful choices. It reuses attributable context and memory, without guessing sizes, shipping regions or buying permission.

> v0.3.1 is a portable instruction package with offline Python helpers. It is not a product database, web scraper, remote MCP server or payment integration. Live results depend on the host's available tools and merchant access.

## Install and try

```sh
npx skills add kkdopeboi-alt/buywise-skill --skill buywise
```

Choose your agent when prompted. See the [quickstart](docs/QUICKSTART.md) for prerequisites, manual ZIP installation and troubleshooting. The third-party CLI may collect aggregate install telemetry; BuyWise has no telemetry. Local folder copying with skills CLI 1.7.2 was smoke-tested; remote GitHub cloning failed in the maintainer's test environment, so remote install is not claimed as verified.

Want to see the checks without an agent or API key? Download/clone the repository and run:

```sh
python scripts/demo.py
```

Fictional demo: missing shoe size/region → ask together; $70 with unknown shipping → provisional; $1 wrong variant → excluded. This is reproducible helper behavior, not a live-agent performance claim.

## Why use it?

| Common failure | BuyWise handling |
|---|---|
| Buy a gift using the owner's remembered size | Check recipient and applicability for every fact source |
| Recommend before learning size or delivery region | Ask critical missing facts together; don't skip them to save turns |
| Compare a cheap variant or subscription with a different item | Match variant, condition, pack, quantity and purchase type |
| Treat missing shipping/tax as free | Keep unknown and estimated components distinct from observed totals |
| Declare a stale offer cheapest | Classify freshness and compare only the verified input subset |
| Repeat payment after a timeout | Reconcile status first; no blind second submission |

Generic research can start without personal details. A personalized buying shortlist needs the relevant facts. At most three choices means fewer when fewer qualify; it does not mean forcing three unsuitable products.

## Manual installation and host requirements

Clone this repository, then copy the **whole** `skills/buywise/` folder into the skill directory documented by your host. For Codex this is typically `~/.codex/skills/buywise`; reload skills as required by the client and invoke `$buywise`.

```sh
git clone https://github.com/kkdopeboi-alt/buywise-skill.git
cd buywise-skill
```

The skill needs search/browser or merchant tools supplied by the host for live shopping research. Python **3.10+** is optional for the helpers; they use only the standard library. The Markdown workflow remains usable without Python. Payment tooling and authorization are separate.

Codex-style metadata is included. Grok Bot, Muse and other host installation flows have **not** been integration-tested; no universal compatibility is claimed. Keep the references and scripts alongside SKILL.md.

## Try it

```text
Use $buywise to compare new video-call headsets under USD 100 all-in,
shipping to US ZIP 10001. I use a Windows laptop. No member-only prices.
Research only; do not purchase.
```

```text
Find the best offer for this exact manufacturer model and variant.
Compare actual seller, full price, delivery window, returns and warranty
in my destination. Ask for missing facts that could change the decision.
```

The agent returns one leading recommendation and up to two meaningful alternatives, with exact identity, seller, price status, delivery, downside, source links and check time. Unknown costs or fit remain unresolved, not fabricated.

## Reproducible offline tools

```sh
python skills/buywise/scripts/decision_gate.py examples/intake.json
python skills/buywise/scripts/quote_check.py examples/quote.json
python skills/buywise/scripts/compare_offers.py examples/offers.json
python -m unittest discover -s tests -v
python tests/run_sandbox.py
```

| Helper | What it checks | What it cannot prove |
|---|---|---|
| decision_gate.py | Declared/profile critical facts, basic values and memory applicability | Every relevant requirement, correct measurements or purchase permission |
| quote_check.py | Exact bounded decimal arithmetic, complete vs estimated/unknown amounts | Truth of the quote, discount eligibility or live price |
| compare_offers.py | Same-product comparability, supplied freshness, cost and hard limits | Identity evidence, seller legitimacy, stock reservation or global cheapest price |

All examples use fictional merchants/items. No helper contacts shopping sites, records payment details or places orders. See [input contracts](skills/buywise/references/intake-gate.md), [quote format](skills/buywise/references/quote-format.md) and [offer comparison](skills/buywise/references/offer-comparison.md).

## Evaluation and limits

[Validation record](docs/VALIDATION.md) separates automated checks, deterministic fixture replay and independent document-driven review. The sandbox has **26 intake scenarios**, not 26 live purchases. The [behavioral acceptance cases](docs/EVALUATION.md) include additional merchant/payment scenarios that are not all executed integrations.

Prompt instructions cannot guarantee authenticity, access, delivery or injection resistance. The host's permissions and the merchant's rules still apply. Existing explicit bounded purchase authorization can be reused; a recommendation request cannot authorize payment.

## Contribute

Tried it? [Tell us whether your first comparison worked](https://github.com/kkdopeboi-alt/buywise-skill/issues/new?template=usage-feedback.md). A redacted failure is especially useful; no purchase history or credentials are needed.

Report a reproducible failure with a redacted request, evidence timestamps, expected result and actual behavior. Never submit addresses, cookies, tokens, card data or restricted merchant datasets. Category rules should improve fit or evidence quality; affiliate commission must not change ranking.

Original code and documentation: [MIT](LICENSE). Third-party sources and data retain their own rights.

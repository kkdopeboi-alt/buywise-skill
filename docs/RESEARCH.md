# Research and decisions

Research date: 2026-10-16. Three parallel research passes covered agent failures, commerce/fulfillment, and low-friction decisions. Findings below support rules, not claims that this skill has eliminated failures or that benchmark rates measure commercial bots.

## Failure → implemented handling

| Problem | Implementation |
|---|---|
| Hidden/missing requirements | Constraint extraction, material question batch, no repeat questions |
| Invalid links and wrong variant | Merchant-source verification, model/variant/condition/pack matching |
| Brand/search rank bias | Hard filters before preference comparison; dated/source-bound sales claims |
| Tax/shipping/coupon omissions | Comparable due-now accounting; unknown != zero; optional Decimal helper |
| Delivery ambiguity | Handling/transit/arrival split; destination-specific estimates |
| Unverified merchant/authenticity | Separate platform, sold-by, fulfillment and authorization evidence |
| Fake freshness/stock | Last successful observation; blocked != out-of-stock |
| Subscription/member price traps | Public one-time baseline, conditional benefits separate |
| Injection and credential leakage | External content cannot change authority, secure payment handoff |
| Duplicate payment after timeout | Status reconciliation; no blind resubmission |
| Excessive interaction | Infer only reversible minor defaults; one first recommendation |

## Primary sources

1. **DeepShop**, shopping research benchmark: attributes, filters and sorting are distinct challenges. https://arxiv.org/abs/2506.02839
2. **AgenticShop**, research on shopping agents, invalid links, variant and extra-cost difficulties. https://arxiv.org/html/2602.12315v1
3. **EComAgentBench**, requirements distributed across request/context. https://arxiv.org/abs/2606.17698
4. **Anthropic browser-use injection defenses**, external content risk and imperfect defenses. https://www.anthropic.com/news/prompt-injection-defenses
5. **FTC online shopping**, seller, reviews, full costs and returns. https://consumer.ftc.gov/articles/online-shopping
6. **Shopify shipping rates**, costs differ by destination and shipment properties. https://help.shopify.com/manual/shipping/rates-and-methods/manual-rates
7. **Shopify delivery expectations**, handling/transit and delivery estimates. https://help.shopify.com/en/manual/fulfillment/setup/delivery-expectations/overview
8. **Shopify discount combinations**, stacking is conditional. https://help.shopify.com/en/manual/discounts/discount-combinations
9. **Shopify duties**, import amounts and assumptions. https://help.shopify.com/en/manual/international/duties-and-import-taxes/charging-duties
10. **Shop returns**, merchant responsibility. https://help.shop.app/en/shop/managing-orders/returns
11. **FTC warranties**, actual written terms matter. https://consumer.ftc.gov/articles/warranties
12. **FTC subscription guidance**, renewal/eligibility awareness. https://consumer.ftc.gov/articles/getting-and-out-free-trials-auto-renewals-and-negative-option-subscriptions
13. **CPSC recalls**, relevant product safety verification. https://www.cpsc.gov/Recalls
14. **Shopify checkout**, session status, escalation and merchant handoff. https://shopify.dev/docs/agents/carts-and-checkout
15. **Stripe idempotent requests**, payment-level duplicate prevention is a tool capability, not a prompt guarantee. https://docs.stripe.com/api/idempotent_requests
16. **Stripe shared payment tokens**, scoped credentials. https://docs.stripe.com/agentic-commerce/concepts/shared-payment-tokens
17. **Amazon third-party agent position**, site participation/access boundaries. https://www.aboutamazon.com/news/company-news/amazon-perplexity-comet-statement
18. **AP2 flows**, bounded delegated payment authorization as design reference; no claim of AP2 implementation. https://ap2-protocol.org/ap2/flows/

Official policies and APIs change; revisit before implementing adapters. Sources are paraphrased, not bundled third-party datasets. Host permissions always apply. Subscription opt-in is this project's design rule, not a claim about the current legal status of an older click-to-cancel rule.

## v0.1 limits

No new crawler, merchant API connector, persistent preferences store, scheduler, remote MCP server or payment integration. Coverage depends on host tools and accessible evidence. Seller authorization can remain unknown. Real-time stock, authenticity and delivery cannot be guaranteed. The skill offers a disciplined workflow and an offline arithmetic helper, not a universal purchasing backend.

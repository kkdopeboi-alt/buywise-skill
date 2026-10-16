# Optional offline quote arithmetic

Python 3 standard library only. No browser, network, account or payment access. Execute only if the host permits scripts; otherwise follow the cost rules directly. Do not claim this helper checks links, stock, timestamps or authorization.

Run from the repository root:

```sh
python skills/buywise/scripts/quote_check.py examples/quote.json
```

Input is one offer object or an array. Each uses `id`, uppercase three-letter `currency`, and six aggregate charge components: `items` (already multiplied by quantity and including required accessories), `shipping`, `tax`, `duties`, `fees`, `discount`. All amounts are nonnegative decimal strings in that currency's major unit. Discount is subtracted once. Do not feed multi-currency components; convert separately with an evidenced rate/time if needed.

Each component is `{ "amount": "5.00", "status": "observed" }`, `estimated`, or `{ "status": "unknown" }`. Missing/null components remain unknown. Explicit zero requires evidence of no charge/discount. Cashback, points, future rebates and unqualified promotions do not belong in discount.

Incomplete costs return `total: null`; `known_components_net` is not the payable amount or a guaranteed lower bound. Estimated components produce an estimated total. The helper does not rank offers or infer a ceiling from missing values; compare only comparable offers and preserve uncertainty. Full evidence (URLs, observed times, eligibility, seller, destination) remains the agent's responsibility, outside this arithmetic input.

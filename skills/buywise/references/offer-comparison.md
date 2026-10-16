# Same-product offer comparison

Optional offline helper, not a crawler or live verification service:

```sh
python skills/buywise/scripts/compare_offers.py examples/offers.json
```

## Contract

Root keys `request` and `offers`. Request: exact `product_key`, `destination_key`, `condition`, uppercase `currency`, positive integer `quantity`, timezone-aware `as_of`, `max_age_minutes` (1..10080, caller's review policy). Optional `max_total` decimal string, `authorized_seller_only` boolean and timezone-aware `deadline`.

Each offer: unique string `id`; `url` (HTTPS without embedded credentials); `seller_id`; exact matching `product_key`, `destination_key`, `condition`, `quantity`; `availability` (in_stock/out_of_stock/unknown); `purchase_type` (one_time/subscription/financing/unknown); `price_eligibility` (verified/conditional/unknown); `checked_at`; `quote` following quote-format.md. For authorized-only requests add `seller_authorization: verified` only with evidence. If deadline is specified, provide `arrives_by` with timezone and `delivery_status: observed` or estimated/unknown. Observed means a source-stated delivery window, not a carrier guarantee. Date-only estimates need the merchant's timezone and conservative end of the window before comparison.

`product_key` must encode variant, region and pack count, not a similar title; quantity counts those exact units. `destination_key` can be country+postal/zone, never a full address. Matching keys are caller assertions, not independent identity verification. Quotes are basket/offer totals; do not multiply order-level shipping. Do not put membership rebates into an eligible public price unless the user qualifies and it was verified.

## Results

- `excluded`: explicit mismatch, stockout, unsupported recurring price, observed over-budget total, invalid URL or arrival after deadline.
- `provisional`: missing identity/availability/seller/cost, conditional price, expired/future observation, uncertain delivery or unverified required authorization.
- `comparable`: supplied fields pass the declared checks and total is observed.

Only comparable offers are ordered by total; equal totals remain ties. Output calls these `lowest_observed_comparable_ids`, not universal winners. It neither ranks different products nor proves authenticity, access rights, source truth, inventory reservation or purchase permission. URL syntax cannot prove a legitimate seller/payment domain. Inputs with malformed timestamps/quotes/duplicate IDs fail clearly; correct the input rather than deleting charges or treating error as stockout. Use observed per-field evidence in actual work, even though this helper takes one aggregate observation timestamp.

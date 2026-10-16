"""Offline exact-product offer comparison; no network, scraping or payment."""
import argparse
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import json
from urllib.parse import urlsplit

from quote_check import calculate, AMOUNT

def timestamp(raw):
    if not isinstance(raw, str):
        raise ValueError('Timestamp must be ISO 8601 with timezone')
    try:
        value = datetime.fromisoformat(raw.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValueError('Invalid timestamp') from exc
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError('Timezone required')
    return value.astimezone(timezone.utc)

def compare(data):
    if not isinstance(data, dict) or not isinstance(data.get('request'), dict) or not isinstance(data.get('offers'), list):
        raise ValueError('request object and offers array required')
    request, offers = data['request'], data['offers']
    for key in ('product_key', 'destination_key', 'condition', 'currency'):
        if not isinstance(request.get(key), str) or not request[key].strip():
            raise ValueError(f'request.{key} required')
    if type(request.get('quantity')) is not int or request['quantity'] <= 0:
        raise ValueError('request.quantity must be a positive integer')
    if request['condition'] not in ('new', 'used', 'refurbished', 'open_box'):
        raise ValueError('condition must be new, used, refurbished or open_box')
    as_of = timestamp(request.get('as_of'))
    max_age = request.get('max_age_minutes')
    if type(max_age) is not int or not 1 <= max_age <= 10080:
        raise ValueError('Set an explicit evidence age policy between 1 and 10080 minutes')
    if type(request.get('authorized_seller_only', False)) is not bool:
        raise ValueError('authorized_seller_only must be boolean')
    budget = request.get('max_total')
    if budget is not None and (not isinstance(budget, str) or not AMOUNT.fullmatch(budget)):
        raise ValueError('max_total must be a nonnegative decimal string')
    deadline = timestamp(request['deadline']) if request.get('deadline') is not None else None
    # Validate request currency using the same arithmetic contract.
    calculate({'currency': request['currency']})
    results, ids = [], set()
    for offer in offers:
        if not isinstance(offer, dict) or not isinstance(offer.get('id'), str) or not offer['id'].strip():
            raise ValueError('Each offer needs a nonempty string id')
        if offer['id'] in ids:
            raise ValueError('Duplicate offer id')
        ids.add(offer['id'])
        failed, unknown = [], []
        for key in ('product_key', 'destination_key', 'condition', 'quantity'):
            if offer.get(key) is None:
                unknown.append(key)
            elif type(offer[key]) is not type(request[key]) or offer[key] != request[key]:
                failed.append(key + '_mismatch')
        try:
            url = urlsplit(offer.get('url', ''))
            safe_url = url.scheme == 'https' and bool(url.hostname) and not url.username and not url.password
        except (ValueError, TypeError):
            safe_url = False
        if not safe_url:
            failed.append('invalid_https_url')
        # Syntax is not seller/domain authenticity verification.
        if not isinstance(offer.get('seller_id'), str) or not offer['seller_id'].strip():
            unknown.append('seller_identity')
        if offer.get('availability') == 'out_of_stock':
            failed.append('out_of_stock')
        elif offer.get('availability') != 'in_stock':
            unknown.append('availability')
        if offer.get('purchase_type') in ('subscription', 'financing'):
            failed.append('not_one_time_purchase')
        elif offer.get('purchase_type') != 'one_time':
            unknown.append('purchase_type')
        if offer.get('price_eligibility') != 'verified':
            unknown.append('price_eligibility')
        if request.get('authorized_seller_only') and offer.get('seller_authorization') != 'verified':
            unknown.append('seller_authorization')
        checked = offer.get('checked_at')
        if checked is None:
            unknown.append('checked_at')
        else:
            observed = timestamp(checked)
            if observed > as_of:
                unknown.append('future_observation')
            elif as_of - observed > timedelta(minutes=max_age):
                unknown.append('stale_observation')
        if deadline:
            if offer.get('delivery_status') != 'observed':
                unknown.append('delivery_estimated_or_unknown')
            if offer.get('arrives_by') is None:
                unknown.append('delivery_deadline')
            elif timestamp(offer['arrives_by']) > deadline:
                failed.append('arrives_after_deadline')
        cost = calculate(offer.get('quote'))
        if cost['currency'] != request['currency']:
            failed.append('currency_mismatch')
        if cost['status'] != 'observed':
            unknown.append('total_' + cost['status'])
        if budget is not None and cost['total'] is not None and Decimal(cost['total']) > Decimal(budget):
            # Estimated totals do not establish an actual hard-budget violation.
            (failed if cost['status'] == 'observed' else unknown).append('over_budget')
        state = 'excluded' if failed else ('provisional' if unknown else 'comparable')
        results.append({'id': offer['id'], 'status': state, 'failed': failed, 'unresolved': unknown, 'cost': cost})
    eligible = sorted((r for r in results if r['status'] == 'comparable'), key=lambda r: (Decimal(r['cost']['total']), r['id']))
    cheapest = []
    if eligible:
        minimum = Decimal(eligible[0]['cost']['total'])
        cheapest = [r['id'] for r in eligible if Decimal(r['cost']['total']) == minimum]
    return {'offers': results, 'ranked_comparable_ids': [r['id'] for r in eligible],
            'lowest_observed_comparable_ids': cheapest,
            'scope': 'Supplied exact-product offers satisfying declared checks only; provisional offers may be cheaper.',
            'purchase_authorized': False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    args = parser.parse_args()
    try:
        with open(args.input, encoding='utf-8-sig') as stream:
            result = compare(json.load(stream))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, TypeError) as exc:
        parser.exit(2, f'Invalid offers: {exc}\n')

if __name__ == '__main__':
    main()

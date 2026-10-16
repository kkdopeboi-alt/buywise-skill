"""Offline due-now arithmetic. Does not fetch, rank, authorize or purchase."""
import argparse
import json
from decimal import Decimal, InvalidOperation

FIELDS = ('items', 'shipping', 'tax', 'duties', 'fees', 'discount')

def calculate(quote):
    if not isinstance(quote, dict):
        raise ValueError('Each offer must be an object')
    currency = quote.get('currency')
    if not isinstance(currency, str) or len(currency) != 3 or not currency.isalpha() or currency != currency.upper():
        raise ValueError('currency must be a three-letter uppercase code')
    amounts, unknown, estimated = {}, [], []
    for field in FIELDS:
        entry = quote.get(field)
        if entry is None:
            unknown.append(field)
            continue
        if not isinstance(entry, dict) or entry.get('status') not in ('observed', 'estimated', 'unknown'):
            raise ValueError(f'{field}: require status observed, estimated or unknown')
        if entry['status'] == 'unknown':
            unknown.append(field)
            continue
        raw = entry.get('amount')
        if not isinstance(raw, str):
            raise ValueError(f'{field}: amount must be a decimal string')
        try:
            amount = Decimal(raw)
        except InvalidOperation as exc:
            raise ValueError(f'{field}: invalid decimal') from exc
        if not amount.is_finite() or amount < 0:
            raise ValueError(f'{field}: finite nonnegative amount required')
        amounts[field] = amount
        if entry['status'] == 'estimated':
            estimated.append(field)
    subtotal = sum((value if key != 'discount' else -value for key, value in amounts.items()), Decimal(0))
    if not unknown and subtotal < 0:
        raise ValueError('Discount exceeds complete charges')
    status = 'incomplete' if unknown else ('estimated' if estimated else 'observed')
    return {'id': quote.get('id'), 'currency': currency, 'status': status,
            'total': str(subtotal) if not unknown else None,
            'known_components_net': str(subtotal), 'unknown': unknown, 'estimated': estimated,
            'note': 'Arithmetic only; no evidence, stock, delivery or purchase authorization verified.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='UTF-8 JSON offer or array of offers')
    args = parser.parse_args()
    try:
        with open(args.input, encoding='utf-8-sig') as stream:
            data = json.load(stream)
        result = [calculate(q) for q in data] if isinstance(data, list) else calculate(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, TypeError) as exc:
        parser.exit(2, f'Invalid quote: {exc}\n')

if __name__ == '__main__':
    main()

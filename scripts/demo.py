"""Three reproducible, offline shopping checks using fictional data."""
from pathlib import Path
import copy
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/buywise/scripts'))
from decision_gate import evaluate
from compare_offers import compare

def main():
    print('BuyWise offline demo — fictional data, no network or purchases.\n')
    intake = json.loads((ROOT / 'examples/intake.json').read_text(encoding='utf-8'))
    result = evaluate(intake)
    print('1. Shoes: do not guess missing fit and destination facts.')
    print('   Personal shortlist ready:', result['ready_for_personalized_recommendation'])
    print('   Ask together:', ', '.join(x['field'] for x in result['unresolved']))
    offers = json.loads((ROOT / 'examples/offers.json').read_text(encoding='utf-8'))
    result = compare(offers)
    print('\n2. A low sticker price is not a verified all-in total.')
    for offer in result['offers']:
        print(f"   {offer['id']}: {offer['status']}, total={offer['cost']['total']}")
    print('   Lowest observed comparable subset:', ', '.join(result['lowest_observed_comparable_ids']))
    cheaper = copy.deepcopy(offers['offers'][0])
    cheaper.update(id='wrong-variant', product_key='different-region-and-pack')
    cheaper['quote']['items']['amount'] = '1'
    offers['offers'].append(cheaper)
    result = compare(offers)
    wrong = next(x for x in result['offers'] if x['id'] == 'wrong-variant')
    print('\n3. A cheaper wrong variant must not win.')
    print('   Wrong variant:', wrong['status'], ', '.join(wrong['failed']))
    print('\nThese are helper checks, not a live-agent success-rate benchmark.')

if __name__ == '__main__':
    main()

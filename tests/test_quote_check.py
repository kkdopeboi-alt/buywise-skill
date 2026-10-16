import importlib.util
from pathlib import Path
import unittest

script = Path(__file__).resolve().parents[1] / 'skills/buywise/scripts/quote_check.py'
spec = importlib.util.spec_from_file_location('quote_check', script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def offer():
    return {'currency': 'USD', **{k: {'amount': '0', 'status': 'observed'} for k in module.FIELDS}}

class QuoteTests(unittest.TestCase):
    def test_decimal_exact(self):
        q = offer()
        q['items']['amount'], q['shipping']['amount'] = '0.10', '0.20'
        self.assertEqual(module.calculate(q)['total'], '0.30')

    def test_missing_tax_not_free(self):
        q = offer()
        del q['tax']
        self.assertIsNone(module.calculate(q)['total'])
        self.assertIn('tax', module.calculate(q)['unknown'])

    def test_estimate_not_observed(self):
        q = offer()
        q['tax'] = {'amount': '5', 'status': 'estimated'}
        self.assertEqual(module.calculate(q)['status'], 'estimated')

    def test_discount(self):
        q = offer()
        q['items']['amount'], q['discount']['amount'] = '100', '10'
        self.assertEqual(module.calculate(q)['total'], '90')

    def test_reject_invalid(self):
        for raw in ('NaN', 'Infinity', '-1', 'nope'):
            with self.subTest(raw=raw):
                q = offer()
                q['items']['amount'] = raw
                with self.assertRaises(ValueError):
                    module.calculate(q)

    def test_no_mixed_currency_guess(self):
        q = offer()
        q['currency'] = 'usd'
        with self.assertRaises(ValueError):
            module.calculate(q)

    def test_no_negative_complete_total(self):
        q = offer()
        q['discount']['amount'] = '1'
        with self.assertRaises(ValueError):
            module.calculate(q)

if __name__ == '__main__':
    unittest.main()

"""Regression tests exercise failures that previously produced false readiness/totals."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/buywise/scripts'

def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

gate, quotes = load('decision_gate'), load('quote_check')

class CriticalFactRegressions(unittest.TestCase):
    def test_false_zero_placeholder_do_not_satisfy_size(self):
        for value in (False, True, 0, -1, '-1', '0', 'unknown', '待确认', [], {}):
            with self.subTest(value=value):
                out = gate.evaluate({'requirements':['size'], 'facts':{'size':{'value':value,'source':'user'}}})
                self.assertFalse(out['ready_for_personalized_recommendation'])

    def test_profile_catches_omitted_shoe_fields(self):
        out = gate.evaluate({'task':{'mode':'recommend','category':'footwear'}, 'requirements':[]})
        self.assertEqual(set(x['field'] for x in out['unresolved']), {
            'destination_country','size','size_system','size_category',
            'budget_amount','budget_currency','budget_scope'})

    def test_generic_exploration_does_not_force_intake_or_claim_ready(self):
        out = gate.evaluate({'task':{'mode':'explore'}})
        self.assertEqual(out['questions'], [])
        self.assertFalse(out['ready_for_personalized_recommendation'])
        self.assertEqual(out['next_action'], 'generic_research')

    def test_no_profile_or_requirements_fails_closed(self):
        with self.assertRaises(ValueError): gate.evaluate({'requirements':[], 'facts':{}})

    def test_profile_flags_are_not_truthy_strings(self):
        with self.assertRaises(ValueError): gate.evaluate({'task':{'mode':'recommend','compare_total':'false'}})
        with self.assertRaises(ValueError): gate.evaluate({'requirements':['size'],'facts':{
            'size':{'value':42,'source':'memory','applicable':'false','recipient_match':True}}})

    def test_compare_does_not_demand_unneeded_budget_or_size(self):
        out = gate.evaluate({'task':{'mode':'compare','category':'generic'},'facts':{
            'destination_country':{'value':'CA','source':'user'}}})
        self.assertTrue(out['ready_for_personalized_recommendation'])
        self.assertNotIn('budget_amount', out['resolved'])

    def test_source_is_not_a_webpage_instruction(self):
        out = gate.evaluate({'requirements':['size'],'facts':{'size':{'value':42,'source':'webpage'}}})
        self.assertFalse(out['ready_for_personalized_recommendation'])

    def test_explicit_no_allergies_not_unknown_size(self):
        out = gate.evaluate({'requirements':['material_allergy'],'facts':{
            'material_allergy':{'value':'none','source':'user'}}})
        self.assertTrue(out['ready_for_personalized_recommendation'])
        out = gate.evaluate({'requirements':['size'],'facts':{'size':{'value':'none','source':'user'}}})
        self.assertFalse(out['ready_for_personalized_recommendation'])

    def test_user_statement_about_another_recipient_is_not_reusable(self):
        out = gate.evaluate({'requirements':['size'],'facts':{
            'size':{'value':'US9','source':'user','recipient_match':False,'applicable':False}}})
        self.assertFalse(out['ready_for_personalized_recommendation'])

    def test_non_postal_region_uses_delivery_zone(self):
        out = gate.evaluate({'task':{'mode':'compare','compare_total':True,'postal_code_required':False},'facts':{
            'destination_country':{'value':'HK','source':'user'},
            'delivery_zone':{'value':'fixture-district','source':'user'}}})
        self.assertTrue(out['ready_for_personalized_recommendation'])
        self.assertNotIn('postal_code',out['resolved'])

    def test_ascii_country_and_currency_required(self):
        for field, value in (('destination_country','纽约'),('budget_currency','ＵＳＤ'),('budget_currency','usd')):
            out = gate.evaluate({'requirements':[field],'facts':{field:{'value':value,'source':'user'}}})
            self.assertFalse(out['ready_for_personalized_recommendation'])

class CostRegressions(unittest.TestCase):
    def offer(self):
        return {'currency':'USD', **{k:{'amount':'0','status':'observed'} for k in quotes.FIELDS}}

    def test_misspelled_charge_does_not_disappear(self):
        q = self.offer(); q['shiping'] = {'amount':'25','status':'observed'}
        with self.assertRaises(ValueError): quotes.calculate(q)

    def test_unknown_amount_contradiction_rejected(self):
        q = self.offer(); q['tax'] = {'amount':'0','status':'unknown'}
        with self.assertRaises(ValueError): quotes.calculate(q)

    def test_unsupported_numeric_formats_rejected(self):
        for raw in ('1e1000000','1_000','-0',' 5','0.0000001','1000000000000'):
            q = self.offer(); q['items']['amount'] = raw
            with self.subTest(raw=raw), self.assertRaises(ValueError): quotes.calculate(q)

    def test_large_exact_arithmetic_is_not_rounded(self):
        q = self.offer(); q['items']['amount'] = '999999999999.999999'; q['tax']['amount']='0.000001'
        self.assertEqual(quotes.calculate(q)['total'], '1000000000000.000000')

    def test_unicode_currency_rejected(self):
        q = self.offer(); q['currency'] = 'ＵＳＤ'
        with self.assertRaises(ValueError): quotes.calculate(q)

    def test_component_currency_cannot_be_silently_mixed(self):
        q = self.offer();q['items']={'amount':'100','status':'observed','currency':'CNY'}
        with self.assertRaises(ValueError):quotes.calculate(q)

    def test_extreme_precision_cannot_silently_lose_shipping(self):
        q = self.offer();q['items']['amount']='10000000000000000000000000000';q['shipping']['amount']='1'
        with self.assertRaises(ValueError):quotes.calculate(q)

    def test_cli_bad_json_fails_without_traceback(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as folder:
            path = Path(folder)/'invalid.json'; path.write_text('{', encoding='utf-8')
            process = subprocess.run([sys.executable,str(SCRIPTS/'quote_check.py'),str(path)],capture_output=True,text=True)
            self.assertEqual(process.returncode,2)
            self.assertNotIn('Traceback',process.stderr)

if __name__ == '__main__': unittest.main()

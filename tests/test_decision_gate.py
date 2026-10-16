import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).with_name('run_sandbox.py')
spec = importlib.util.spec_from_file_location('sandbox', path)
sandbox = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sandbox)

class IntakeTests(unittest.TestCase):
    def test_fixture_replay(self):
        report = sandbox.replay()
        for case in report['cases']:
            with self.subTest(case=case['id']):
                self.assertTrue(case['passed'], case)

    def test_no_personal_values_in_output(self):
        result = sandbox.gate.evaluate({'requirements':['postal_code'], 'facts':{
            'postal_code':{'value':'PRIVATE-POSTAL-FIXTURE','source':'user'}}})
        self.assertNotIn('PRIVATE-POSTAL-FIXTURE', str(result))

    def test_reject_bad_contract(self):
        for data in (None, {'requirements':'size'}, {'requirements':['']}, {'requirements':[], 'facts':[]}):
            with self.subTest(data=data):
                with self.assertRaises(ValueError): sandbox.gate.evaluate(data)

if __name__ == '__main__':
    unittest.main()

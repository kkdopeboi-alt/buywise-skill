"""Deterministic offline fixture replay; not an LLM/browser benchmark."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('decision_gate', ROOT / 'skills/buywise/scripts/decision_gate.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

def replay():
    cases = json.loads((ROOT / 'tests/sandbox_cases.json').read_text(encoding='utf-8'))
    results = []
    for case in cases:
        actual = gate.evaluate(case['input'])
        fields = [x['field'] for x in actual['unresolved']]
        passed = (fields == case['expected_unresolved'] and
                  actual['ready_for_personalized_recommendation'] == case.get('expected_ready', not fields) and
                  len(actual['questions']) == len(fields) and not actual['purchase_authorized'])
        results.append({'id': case['id'], 'problem': case['problem'], 'passed': passed,
                        'expected_unresolved': case['expected_unresolved'], 'actual': actual})
    return {'type': 'deterministic_fixture_replay_not_end_to_end',
            'passed': sum(r['passed'] for r in results), 'total': len(results), 'cases': results}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = replay()
    if args.output:
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Sandbox: {report['passed']}/{report['total']} fixture checks passed (not an LLM integration test)")
    raise SystemExit(0 if report['passed'] == report['total'] else 1)

if __name__ == '__main__':
    main()

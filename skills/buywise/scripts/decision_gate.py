"""Offline guard for declared critical shopping requirements; no network/payment."""
import argparse
import json

QUESTIONS = {
    'destination_country': '收货国家或地区是哪里？',
    'postal_code': '收货邮编是什么？用于核对税费、配送和到货时间。',
    'size': '需要什么尺码或关键尺寸？',
    'size_system': '尺码采用哪个体系（如 US/EU/UK）？',
    'size_category': '应使用男款、女款、儿童款或哪个品牌尺码表？',
    'width': '有何鞋楦宽度或关键宽度要求？',
    'device_model': '需要兼容的设备准确型号是什么？',
    'budget': '预算上限和币种是什么？',
    'budget_amount': '预算金额上限是多少？',
    'budget_currency': '预算使用什么币种？',
    'budget_scope': '预算是否包含税费、运费和必需配件？',
    'condition': '接受哪些成色（全新、翻新或二手）？',
    'deadline': '最晚需要何时收到（含日期及适用时区）？',
    'recipient': '这次是给谁购买，现有偏好是否适用于该收件人？',
}

def evaluate(data):
    if not isinstance(data, dict):
        raise ValueError('Input must be an object')
    requirements, facts = data.get('requirements'), data.get('facts', {})
    if not isinstance(requirements, list) or not all(isinstance(x, str) and x.strip() for x in requirements):
        raise ValueError('requirements must be a list of nonempty field names')
    if not isinstance(facts, dict):
        raise ValueError('facts must be an object')
    resolved, unresolved, questions = [], [], []
    for name in dict.fromkeys(requirements):
        fact = facts.get(name)
        reason = None
        if not isinstance(fact, dict):
            reason = 'missing'
        else:
            value = fact.get('value')
            if value is None or (isinstance(value, str) and not value.strip()) or value == [] or value == {}:
                reason = 'missing_value'
            elif fact.get('conflict') is True:
                reason = 'conflict'
            elif fact.get('source') == 'user':
                pass
            elif fact.get('source') in ('context', 'memory'):
                if fact.get('recipient_match') is not True or fact.get('applicable') is not True:
                    reason = 'unconfirmed_applicability'
            else:
                reason = 'unsupported_source'
        if reason:
            unresolved.append({'field': name, 'reason': reason})
            question = QUESTIONS.get(name, f'请补充会影响本次选购的关键信息：{name}。')
            if reason in ('conflict', 'unconfirmed_applicability'):
                question += '现有记录有冲突或不确定是否适用于本次购买，请确认。'
            questions.append(question)
        else:
            resolved.append(name)
    return {'ready_for_personalized_recommendation': not unresolved,
            'resolved': resolved, 'unresolved': unresolved, 'questions': questions,
            'purchase_authorized': False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    args = parser.parse_args()
    try:
        with open(args.input, encoding='utf-8-sig') as stream:
            result = evaluate(json.load(stream))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, TypeError) as exc:
        parser.exit(2, f'Invalid intake: {exc}\n')

if __name__ == '__main__':
    main()

"""Offline guard for declared critical shopping requirements; no network/payment."""
import argparse
import json
import re
from decimal import Decimal

UNKNOWN = {'unknown', 'unsure', 'null', 'tbd', '?', '未知', '不清楚', '待确认', '不知道'}
ABSENT = {'n/a', 'none', '不适用', '无'}
MONEY = re.compile(r'(?:0|[1-9][0-9]{0,11})(?:\.[0-9]{1,6})?\Z')
FIELD = re.compile(r'[a-z][a-z0-9_]{0,63}\Z')

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
    'delivery_zone': '收货城市或配送区域是什么？该地区无邮编时用它核对配送。',
}

def required_fields(data):
    declared = data.get('requirements', [])
    if not isinstance(declared, list) or not all(isinstance(x, str) and FIELD.fullmatch(x) for x in declared):
        raise ValueError('requirements must contain snake_case field names')
    task = data.get('task')
    if task is None:
        if not declared:
            raise ValueError('Declare a task profile or at least one critical requirement')
        return list(dict.fromkeys(declared)), 'declared_only'
    if not isinstance(task, dict):
        raise ValueError('task must be an object')
    allowed = {'mode', 'category', 'compare_total', 'delivery_sensitive', 'budget_required', 'postal_code_required'}
    if set(task) - allowed:
        raise ValueError('Unknown task profile fields')
    mode, category = task.get('mode'), task.get('category', 'generic')
    if mode not in ('explore', 'compare', 'recommend', 'purchase'):
        raise ValueError('task.mode must be explore, compare, recommend or purchase')
    if category not in ('generic', 'footwear', 'apparel', 'device-accessory'):
        raise ValueError('Unsupported category; use generic plus explicit requirements')
    for key in ('compare_total', 'delivery_sensitive', 'budget_required', 'postal_code_required'):
        if key in task and type(task[key]) is not bool:
            raise ValueError(f'task.{key} must be boolean')
    inferred = []
    if mode != 'explore':
        inferred.append('destination_country')
        if category in ('footwear', 'apparel'):
            inferred += ['size', 'size_system', 'size_category']
        if category == 'device-accessory':
            inferred.append('device_model')
    if task.get('compare_total') or task.get('delivery_sensitive'):
        inferred += ['destination_country', 'postal_code' if task.get('postal_code_required', True) else 'delivery_zone']
    if task.get('delivery_sensitive'):
        inferred.append('deadline')
    if task.get('budget_required', mode in ('recommend', 'purchase')):
        inferred += ['budget_amount', 'budget_currency', 'budget_scope']
    return list(dict.fromkeys(inferred + declared)), 'profile_assisted'

def invalid_value(name, value):
    if value is None or isinstance(value, bool):
        return True
    if isinstance(value, str):
        if not value.strip() or value.strip().casefold() in UNKNOWN:
            return True
        if name in QUESTIONS and value.strip().casefold() in ABSENT:
            return True
    elif type(value) not in (int, float):
        return True
    if name == 'budget_amount':
        return not MONEY.fullmatch(str(value)) or Decimal(str(value)) <= 0
    if name in ('destination_country', 'budget_currency'):
        length = 2 if name == 'destination_country' else 3
        return not isinstance(value, str) or not re.fullmatch('[A-Z]{' + str(length) + '}', value)
    if name == 'size':
        if type(value) in (int, float):
            return not MONEY.fullmatch(str(value)) or Decimal(str(value)) <= 0
        if re.fullmatch(r'[+-]?[0-9.]+', value):
            return not MONEY.fullmatch(value) or Decimal(value) <= 0
        return False  # Named sizes such as S/XL need category/chart evidence from the agent.
    if name == 'budget_scope':
        return value not in ('all-in', 'items-only')
    return not isinstance(value, str)

def evaluate(data):
    if not isinstance(data, dict):
        raise ValueError('Input must be an object')
    requirements, coverage = required_fields(data)
    facts = data.get('facts', {})
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
            for flag in ('conflict', 'recipient_match', 'applicable'):
                if flag in fact and type(fact[flag]) is not bool:
                    raise ValueError(f'{name}.{flag} must be boolean')
            if invalid_value(name, value):
                reason = 'missing_or_invalid_value'
            elif fact.get('conflict') is True:
                reason = 'conflict'
            elif fact.get('recipient_match') is False or fact.get('applicable') is False:
                reason = 'unconfirmed_applicability'
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
    exploration = isinstance(data.get('task'), dict) and data['task'].get('mode') == 'explore'
    return {'ready_for_personalized_recommendation': not unresolved and not exploration,
            'resolved': resolved, 'unresolved': unresolved, 'questions': questions,
            'purchase_authorized': False, 'coverage': coverage,
            'next_action': 'ask_critical_questions' if unresolved else ('generic_research' if exploration else 'verify_offers'),
            'notice': 'Declared/profile fields only; no semantic fit, evidence or purchase permission verified.'}

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

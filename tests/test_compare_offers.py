import copy
from pathlib import Path
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/buywise/scripts'
sys.path.insert(0,str(SCRIPTS))
from compare_offers import compare

def fixture():
    request={'product_key':'fixture-headset:v1:black','destination_key':'US:10001',
             'condition':'new','currency':'USD','quantity':1,'max_total':'100',
             'as_of':'2026-10-16T10:00:00Z','max_age_minutes':60}
    offer={'id':'a','url':'https://merchant.example/products/fixture','seller_id':'fixture-merchant',
           'product_key':request['product_key'],'destination_key':request['destination_key'],
           'condition':'new','quantity':1,'availability':'in_stock',
           'checked_at':'2026-10-16T09:30:00Z','purchase_type':'one_time','price_eligibility':'verified',
           'quote':{'currency':'USD', **{f:{'amount':'0','status':'observed'} for f in ('items','shipping','tax','duties','fees','discount')}}}
    offer['quote']['items']['amount']='80'
    return {'request':request,'offers':[offer]}

class OfferTests(unittest.TestCase):
    def test_identical_public_offer_ranks(self):
        result=compare(fixture())
        self.assertEqual(result['lowest_observed_comparable_ids'],['a'])
        self.assertFalse(result['purchase_authorized'])

    def test_cheapest_wrong_variant_excluded(self):
        data=fixture(); cheap=copy.deepcopy(data['offers'][0]);cheap.update(id='cheap',product_key='different')
        cheap['quote']['items']['amount']='1';data['offers'].append(cheap)
        self.assertEqual(compare(data)['ranked_comparable_ids'],['a'])

    def test_unknown_shipping_does_not_win(self):
        data=fixture();data['offers'][0]['quote']['shipping']={'status':'unknown'}
        result=compare(data)
        self.assertEqual(result['offers'][0]['status'],'provisional')
        self.assertEqual(result['ranked_comparable_ids'],[])

    def test_stale_and_future_not_fresh(self):
        for time in ('2026-10-15T09:00:00Z','2026-10-16T11:00:00Z'):
            data=fixture();data['offers'][0]['checked_at']=time
            self.assertEqual(compare(data)['offers'][0]['status'],'provisional')

    def test_delivery_estimate_not_confirmed_deadline(self):
        data=fixture();data['request']['deadline']='2026-10-18T23:59:00Z'
        data['offers'][0].update(arrives_by='2026-10-18T12:00:00Z',delivery_status='estimated')
        self.assertEqual(compare(data)['offers'][0]['status'],'provisional')

    def test_late_stockout_overbudget_subscription_excluded(self):
        mutations=[{'availability':'out_of_stock'},{'purchase_type':'subscription'},{'quantity':True},{'condition':'used'}]
        for mutation in mutations:
            data=fixture();data['offers'][0].update(mutation)
            self.assertEqual(compare(data)['offers'][0]['status'],'excluded')
        data=fixture();data['offers'][0]['quote']['shipping']['amount']='25'
        self.assertEqual(compare(data)['offers'][0]['status'],'excluded')

    def test_conditional_price_and_unauthorized_seller_provisional(self):
        data=fixture();data['request']['authorized_seller_only']=True
        data['offers'][0]['price_eligibility']='conditional'
        result=compare(data)['offers'][0]
        self.assertIn('price_eligibility',result['unresolved'])
        self.assertIn('seller_authorization',result['unresolved'])

    def test_currency_and_destination_mismatch(self):
        for key,value in (('destination_key','CA:A1A1A1'),('product_key','other')):
            data=fixture();data['offers'][0][key]=value
            self.assertEqual(compare(data)['offers'][0]['status'],'excluded')
        data=fixture();data['offers'][0]['quote']['currency']='CAD'
        self.assertEqual(compare(data)['offers'][0]['status'],'excluded')

    def test_ties_not_broken_by_hidden_affiliate_score(self):
        data=fixture();b=copy.deepcopy(data['offers'][0]);b['id']='b';data['offers'].append(b)
        self.assertEqual(compare(data)['lowest_observed_comparable_ids'],['a','b'])

    def test_url_credentials_rejected(self):
        data=fixture();data['offers'][0]['url']='https://secret:password@merchant.example/'
        result=compare(data)
        self.assertEqual(result['offers'][0]['status'],'excluded')
        self.assertNotIn('password',str(result))

    def test_missing_timezone_or_duplicate_id_rejected(self):
        data=fixture();data['request']['as_of']='2026-10-16T10:00:00'
        with self.assertRaises(ValueError):compare(data)
        data=fixture();data['offers'].append(copy.deepcopy(data['offers'][0]))
        with self.assertRaises(ValueError):compare(data)

if __name__ == '__main__':unittest.main()

import requests
import json
import csv

from app.ShopifyTemplateWriter import ShopifyTemplateWriter
'''
Client for connecting to and performing operations against Depop

Depop does not have an open API, but their REST endpoints are exposed (for the time being: 3/7/2020)
'''
class DepopClient:
    base_url = 'https://webapi.depop.com/api/v1/'
    def __init__(self, shop_id):
        self.shopify_helper = ShopifyTemplateWriter()
        self.shop_id = shop_id
        self.shop_name = None
        self.file = 'inventory_' + self.shop_id + '.csv'
        self.data = []
        self.shopify_product_list = []
    
    '''
    Method to fetch products from the Depop shop 
    '''
    def get_products(self, item_count=24):
        endpoint = 'shop/' + self.shop_id + '/products?limit=' + str(item_count)
        data = self._build_request('get', endpoint)
        self.data = data

    '''
    Build dict that maps csv header's to product data for easy writing
    '''
    def format_products_for_import(self):
        # shopify_product_list = []
        for item in self.data['products']:
            item_dict = {}
            item_dict['Handle'] = self.format_slug_to_handle(item['slug'])
            item_dict['Title'] = self.format_slug_to_title(item['slug'])
            item_dict['Vendor'] = self.shop_name if self.shop_name else self.set_shop_name(item['slug'])
            # item_dict['Type'] = None
            item_dict['Variant Price'] = item['price']['price_amount']
            item_dict['Image Src'] = item['preview']['1280']
            self.shopify_product_list.append(item_dict)
        
    '''
    Convert Depop slug to Shopify handle
    '''
    def format_slug_to_title(self, slug):
        words = slug.split('-')
        words.pop(0)
        return ' '.join(words).title()

    '''
    Convert Depop slug to Shopify title
    '''
    def format_slug_to_handle(self, slug):
        words = slug.split('-')
        words.pop(0)
        return '-'.join(words)

    '''
    Set shop_name to the shop name imbedded in the Depop slug
    '''
    def set_shop_name(self, slug):
        words = slug.split('-')
        shop_words = words[0].split('_')
        self.shop_name = ' '.join(shop_words).title()
        return self.shop_name

    '''
    Looks like Shopify only supports bulk imports of products with CSV
    '''
    def write_csv(self):
        with open(self.file, 'w', newline='') as csv_f:
            writer = csv.DictWriter(csv_f, fieldnames=self.shopify_helper.headers)
            writer.writeheader()
            for item in self.shopify_product_list:
                writer.writerow(item)

    # Private    
    '''
    _build_request takes two parameters

    @param string method is the HTTP method we are invoking in our call
    @param string endpoint is the url extension
    @param mixed options can be whatever options
    '''
    def _build_request(self, method, endpoint, options={}):
        url = self.base_url + endpoint
        if method == 'get':
            req = requests.get(url)
            data = json.loads(req.content)
        return data
import requests
import json
'''
Client for connecting to and performing operations against Depop

Depop does not have an open API, but their REST endpoints are exposed (for the time being)
'''
class DepopClient:
    base_url = 'https://webapi.depop.com/api/v1/'
    def __init__(self, shop_id):
        self.shop_id = shop_id
        self.file = 'inventory_' + self.shop_id + '.csv'
        self.products = []
    
    '''
    Method to fetch products from the Depop shop 
    '''
    def get_products(self, item_count=24):
        endpoint = 'shop/' + self.shop_id + '/products?limit=' + item_count
        data = self._build_request('get', endpoint)
        self.products = data
        print(data)
        return data
    
    '''
    Looks like Shopify only supports bulk imports of products with CSV
    '''
    def write_csv(self):

        # with open(self.file, 'w') as f:
        return

    # Private
    
    '''
    _build_request takes two parameters

    @param string method is the HTTP method we are invoking in our call
    @param string endpoint is the url extension
    @param mixed options can be whatever options
    '''
    def _build_request(method, endpoint, options={}):
        url = self.base_url + endpoint
        if method == 'get':
            req = requests.get(url)
            data = json.loads(req.content)
        return data
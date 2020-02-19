import requests
import json

'''
Think about the task we want this to do.
Grab all of the products.
Iterate over the products.
Grab the item url, to further query that item for additional information not retrieved from the 'shop' endpoint
'''
class Popget:
    base_url = 'https://webapi.depop.com/api/v1/shop'
    products = []

    def __init__(self, depop_shop_id=None):
        self.shop_id = ''
        self.depop_shop_id = depop_shop_id

    def main(self):
        url = 'https://webapi.depop.com/api/v1/shop/6969590/products?limit=24'
        page = requests.get(url)

        data = json.loads(page.content)

        print(type(data))

        products = data['products']

        for item in products:
            print(item)

        return


if __name__ == '__main__':
    pop = WG_Popget('6969590')
    pop.main()
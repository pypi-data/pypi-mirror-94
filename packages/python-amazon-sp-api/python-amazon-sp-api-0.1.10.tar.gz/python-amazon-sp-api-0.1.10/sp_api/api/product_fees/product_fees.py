import json

from sp_api.api.product_fees.models.get_my_fees_estimate_response import GetMyFeesEstimateResponse
from sp_api.base.helpers import sp_endpoint, fill_query_params
from sp_api.base import Client, Marketplaces


class ProductFees(Client):

    @sp_endpoint('/products/fees/v0/listings/{}/feesEstimate', method='POST')
    def get_product_fees_estimate_for_sku(self, seller_sku, price: float, shipping_price=None, currency='USD',
                                          is_fba=False, points: dict = dict, **kwargs):
        kwargs.update(self._create_body(price, shipping_price, currency, is_fba, seller_sku, points))
        return GetMyFeesEstimateResponse(
            **self._request(fill_query_params(kwargs.pop('path'), seller_sku), data=kwargs).json())

    @sp_endpoint('/products/fees/v0/items/{}/feesEstimate', method='POST')
    def get_product_fees_estimate_for_asin(self, asin, price: float, currency='USD', shipping_price=None, is_fba=False,
                                           points: dict = dict,
                                           **kwargs):
        kwargs.update(self._create_body(price, shipping_price, currency, is_fba, asin, points))
        return GetMyFeesEstimateResponse(
            **self._request(fill_query_params(kwargs.pop('path'), asin), data=kwargs).json())

    def _create_body(self, price, shipping_price=None, currency='USD', is_fba=False, identifier=None, points=dict):
        return {
            'FeesEstimateRequest': {
                'Identifier': identifier or str(price),
                'PriceToEstimateFees': {
                    'ListingPrice': {
                        'Amount': price,
                        'CurrencyCode': currency
                    },
                    'Shipping': {
                        'Amount': shipping_price,
                        'CurrencyCode': currency
                    } if shipping_price else None,
                    **points
                },
                'IsAmazonFulfilled': is_fba,
                'MarketplaceId': self.marketplace_id
            }
        }

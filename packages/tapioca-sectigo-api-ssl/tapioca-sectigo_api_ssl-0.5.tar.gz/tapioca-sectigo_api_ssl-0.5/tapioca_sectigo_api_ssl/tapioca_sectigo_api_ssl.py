# coding: utf-8
from tapioca import (
    TapiocaAdapter, generate_wrapper_from_adapter, FormAdapterMixin)


from .resource_mapping import RESOURCE_MAPPING


class Sectigo_api_sslClientAdapter(FormAdapterMixin, TapiocaAdapter):
    api_root = 'https://secure.trust-provider.com'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(Sectigo_api_sslClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        return params

    def get_iterator_list(self, response_data):
        return response_data

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs,
                                         response_data, response):
        pass


Sectigo_api_ssl = generate_wrapper_from_adapter(Sectigo_api_sslClientAdapter)

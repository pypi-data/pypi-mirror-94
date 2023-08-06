from ._common import append_iex_token, get_iex_json_request, replace_url_var

IEX_STOCK_BASE_URL = 'https://cloud.iexapis.com/beta/account/'

#   Metadata
IEX_METADATA_URL = IEX_STOCK_BASE_URL + 'metadata?'
def metadata(vprint=False):
    return get_iex_json_request(IEX_METADATA_URL)

#   Usage
IEX_USAGE_URL = IEX_STOCK_BASE_URL + 'usage/{type}?'
def metadata(type, vprint=False):
    url = replace_url_var(IEX_USAGE_URL, type=type)
    return get_iex_json_request(url, vprint=vprint)

#   Pay as you go
IEX_PAYASYOUGO_URL = IEX_STOCK_BASE_URL + 'payasyougo?'
def payasyougo(vprint=False):
    return get_iex_json_request(IEX_PAYASYOUGO_URL)

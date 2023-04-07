from currency_converter import CurrencyConverter


def get_exchange_info(currency_from, currency_to, units=100):
    converter = CurrencyConverter()
    res = converter.convert(units, currency_from, currency_to)
    return res

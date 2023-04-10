from currency_converter import CurrencyConverter


def get_exchange_info(currency_from, currency_to, units):
    converter = CurrencyConverter()
    return converter.convert(units, currency_from, currency_to)

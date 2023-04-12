from currency_converter import CurrencyConverter


def get_exchange_info(currency_from, currency_to, units=100):
    try:
        converter = CurrencyConverter()
        res = converter.convert(units, currency_from, currency_to)
    except ValueError:
        return 0
    return res

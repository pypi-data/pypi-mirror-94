from hestia_earth.validation.utils import _list_sum


def validate_economicValueShare(products: list):
    sum = _list_sum(products, 'economicValueShare')
    return sum <= 100.5 or {
        'level': 'error',
        'dataPath': '.products',
        'message': 'economicValueShare should sum to 100 or less across all products',
        'params': {
            'sum': sum
        }
    }

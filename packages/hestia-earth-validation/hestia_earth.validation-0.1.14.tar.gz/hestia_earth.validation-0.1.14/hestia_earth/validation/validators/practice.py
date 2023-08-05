from hestia_earth.schema import TermTermType

from hestia_earth.validation.utils import _filter_list, _list_sum


def validate_cropResidueManagement(practices: list):
    values = _filter_list(practices, 'term.termType', TermTermType.CROPRESIDUEMANAGEMENT.value)
    sum = _list_sum(values, 'value')
    return sum <= 100.5 or {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'value should sum to 100 or less across crop residue management practices',
        'params': {
            'sum': sum
        }
    }

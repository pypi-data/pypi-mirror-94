from hestia_earth.validation.utils import _list_has_props, _diff_in_years


def validate_lifespan(infrastructure: list):
    def validate(values):
        value = values[1]
        index = values[0]
        lifespan = _diff_in_years(value.get('startDate'), value.get('endDate'))
        return lifespan == round(value.get('lifespan'), 1) or {
            'level': 'error',
            'dataPath': f".infrastructure[{index}].lifespan",
            'message': f"must equal to endDate - startDate in decimal years (~{lifespan})"
        }

    results = list(map(validate, enumerate(_list_has_props(infrastructure, ['lifespan', 'startDate', 'endDate']))))
    return next((x for x in results if x is not True), True)

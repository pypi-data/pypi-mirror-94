from functools import reduce
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import non_empty_list, safe_parse_float

from hestia_earth.validation.utils import _flatten, _list_has_props, _value_range_error, _value_average


SOIL_TEXTURE_IDS = ['sandContent', 'siltContent', 'clayContent']


def _group_measurement_key(measurement: dict):
    keys = non_empty_list([
        str(measurement.get('depthUpper', '')),
        str(measurement.get('depthLower', '')),
        measurement.get('startDate'),
        measurement.get('endDate')
    ])
    return '-'.join(keys) if len(keys) > 0 else 'default'


def _group_measurements_depth(measurements: list):
    def group_by(group: dict, measurement: dict):
        key = _group_measurement_key(measurement)
        if key not in group:
            group[key] = []
        group[key].extend([measurement])
        return group

    return reduce(group_by, measurements, {})


def _validate_soilTexture_percent(lookup):
    soil_texture_ids = list(lookup.termid)

    def validate_single(measurements: list, measurement: dict, texture_id: str):
        texture = find_term_match(measurements, texture_id, {})
        term_id = measurement['term']['@id']
        min = safe_parse_float(get_table_value(lookup, 'termid', term_id, column_name(f"{texture_id}min")), 0)
        max = safe_parse_float(get_table_value(lookup, 'termid', term_id, column_name(f"{texture_id}max")), 100)
        # set default value to min so if no value then passes validation
        texture_value = _value_average(texture, min)
        return min <= texture_value <= max or {
            'level': 'error',
            'dataPath': '.measurements',
            'message': 'is outside the allowed range',
            'params': {
                'term': texture['term'],
                'range': {'min': min, 'max': max}
            }
        }

    def validate_all(measurements: list):
        values = list(filter(lambda v: v['term']['@id'] in soil_texture_ids, measurements))
        return len(values) == 0 or _flatten(map(
            lambda measurement: list(map(lambda id: validate_single(measurements, measurement, id), SOIL_TEXTURE_IDS)),
            values
        ))

    return validate_all


def _validate_soiltTexture_sum(measurements: list):
    measurements = list(filter(lambda v: v['term']['@id'] in SOIL_TEXTURE_IDS, measurements))
    measurements = list(filter(lambda v: 'value' in v, measurements))
    terms = list(map(lambda v: v['term']['@id'], measurements))
    sum_values = sum(map(lambda v: _value_average(v), measurements))
    return len(set(terms)) != len(SOIL_TEXTURE_IDS) or 99.5 < sum_values < 100.5 or {
        'level': 'error',
        'dataPath': '.measurements',
        'message': f"sum not equal to 100% for {', '.join(SOIL_TEXTURE_IDS)}"
    }


def validate_soilTexture(measurements: list):
    soilTexture = download_lookup('soilTexture.csv', True)
    groupped_measurements = _group_measurements_depth(measurements).values()
    results_sum = list(map(_validate_soiltTexture_sum, groupped_measurements))
    valid_sum = next((x for x in results_sum if x is not True), True)
    results_percent = _flatten(map(_validate_soilTexture_percent(soilTexture), groupped_measurements))
    valid_percent = next((x for x in results_percent if x is not True), True)
    return valid_sum if valid_sum is not True else valid_percent


def validate_depths(measurements: list):
    def validate(values):
        index = values[0]
        measurement = values[1]
        return measurement['depthUpper'] < measurement['depthLower'] or {
            'level': 'error',
            'dataPath': f".measurements[{index}].depthLower",
            'message': 'must be greater than depthUpper'
        }

    results = list(map(validate, enumerate(_list_has_props(measurements, ['depthUpper', 'depthLower']))))
    return next((x for x in results if x is not True), True)


def validate_value_min_max(measurements: list):
    def validate(values):
        index = values[0]
        measurement = values[1]
        props = measurement.get('term', {}).get('defaultProperties', [])
        mininum = next((prop.get('value') for prop in props if prop.get('term', {}).get('@id') == 'minimum'), None)
        maximum = next((prop.get('value') for prop in props if prop.get('term', {}).get('@id') == 'maximum'), None)
        value = _value_average(measurement)
        error = _value_range_error(value, mininum, maximum) if value is not None else False
        return error is False or ({
            'level': 'error',
            'dataPath': f".measurements[{index}].value",
            'message': f"should be above {mininum}"
        } if error == 'minimum' else {
            'level': 'error',
            'dataPath': f".measurements[{index}].value",
            'message': f"should be below {maximum}"
        })

    results = list(map(validate, enumerate(measurements)))
    return next((x for x in results if x is not True), True)

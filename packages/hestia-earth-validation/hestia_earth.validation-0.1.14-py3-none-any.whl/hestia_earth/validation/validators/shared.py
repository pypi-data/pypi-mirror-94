from typing import List
import re

from hestia_earth.validation.geojson import _get_geojson_area
from hestia_earth.validation.gadm import _get_gadm_data
from hestia_earth.validation.utils import _same_properties, _value_average


def validate_dates(node: dict):
    start = node.get('startDate')
    end = node.get('endDate')
    return start is None or end is None or (len(start) <= 7 and len(end) <= 7 and end >= start) or end > start


def validate_list_dates(node: dict, list_key: str):
    def validate(values):
        value = values[1]
        index = values[0]
        return validate_dates(value) or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].endDate",
            'message': 'must be greater than startDate'
        }

    results = list(map(validate, enumerate(node.get(list_key, []))))
    return next((x for x in results if x is not True), True)


def validate_list_min_max(node: dict, list_key: str):
    def validate(values):
        value = values[1]
        index = values[0]
        return value.get('min', 0) <= value.get('max', 0) or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].max",
            'message': 'must be greater than min'
        }

    results = list(map(validate, enumerate(node.get(list_key, []))))
    return next((x for x in results if x is not True), True)


def validate_list_duplicates(node: dict, list_key: str, props: List[str]):
    def validate(values):
        value = values[1]
        index = values[0]
        values = node[list_key].copy()
        values.pop(index)
        duplicates = list(filter(_same_properties(value, props), values))
        return len(duplicates) == 0 or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}]",
            'message': f"Duplicates found. Please make sure there is only one entry with the same {', '.join(props)}"
        }

    results = list(map(validate, enumerate(node.get(list_key, []))))
    return next((x for x in results if x is not True), True)


def validate_list_term_percent(node: dict, list_key: str):
    def validate(values):
        index = values[0]
        value = values[1]
        units = value.get('term', {}).get('units', '')
        value = _value_average(value)
        return units != '% (0-100)' or value is None or type(value) == str or (0 <= value and value <= 100) or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].value",
            'message': 'should be between 0 and 100 (percentage)'
        }

    results = list(map(validate, enumerate(node.get(list_key, []))))
    return next((x for x in results if x is not True), True)


def validate_region(node: dict, region_key='region'):
    country = node.get('country', {})
    region_id = node.get(region_key, {}).get('@id', '')
    return region_id[0:8] == country.get('@id') or {
        'level': 'error',
        'dataPath': f".{region_key}",
        'message': 'must be within the country',
        'params': {
            'country': country.get('name')
        }
    }


def validate_country(node: dict):
    country_id = node.get('country', {}).get('@id', '')
    # handle additional regions used as country, like region-world
    is_region = country_id.startswith('region-')
    return is_region or bool(re.search(r'GADM-[A-Z]{3}', country_id)) or {
        'level': 'error',
        'dataPath': '.country',
        'message': 'must be a country'
    }


def need_validate_coordinates(node: dict): return 'latitude' in node and 'longitude' in node


def validate_coordinates(node: dict, region_key='region'):
    latitude = node.get('latitude')
    longitude = node.get('longitude')
    country = node.get('country', {})
    region = node.get(region_key)
    gadm_id = region.get('@id') if region else country.get('@id')
    id = _get_gadm_data(gadm_id, id=gadm_id, latitude=latitude, longitude=longitude).get('id')
    return (region and region.get('@id') == id) or (country.get('@id') == id) or {
        'level': 'error',
        'dataPath': f".{region_key}" if region else '.country',
        'message': 'does not contain latitude and longitude'
    }


def need_validate_area(node: dict): return 'area' in node and 'boundary' in node


def validate_area(node: dict):
    try:
        area = _get_geojson_area(node.get('boundary'))
        return area == round(node.get('area'), 1) or {
            'level': 'error',
            'dataPath': '.area',
            'message': f"must be equal to boundary (~{area})"
        }
    except KeyError:
        # if getting the geojson fails, the geojson format is invalid
        # and the schema validation step will detect it
        return True

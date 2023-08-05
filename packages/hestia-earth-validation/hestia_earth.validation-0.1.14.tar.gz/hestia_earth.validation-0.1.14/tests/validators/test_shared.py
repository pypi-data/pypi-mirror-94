import unittest
import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.shared import validate_dates, validate_list_dates, validate_list_duplicates, \
    validate_list_min_max, validate_country, validate_region, validate_area, validate_coordinates, \
    need_validate_coordinates, validate_list_term_percent


class TestValidatorsShared(unittest.TestCase):
    def test_validate_dates(self):
        self.assertEqual(validate_dates({
            'startDate': '2020-01-01'
        }), True)

        self.assertEqual(validate_dates({
            'endDate': '2020-01-02'
        }), True)

        self.assertEqual(validate_dates({
            'startDate': '2020-01-01',
            'endDate': '2020-01-02'
        }), True)

        self.assertEqual(validate_dates({
            'startDate': '2020-01-02',
            'endDate': '2020-01-01'
        }), False)

    def test_validate_emissions_dates_valid(self):
        node = {
            'list': [{
                'startDate': '2020-01-01',
                'endDate': '2020-01-02'
            }]
        }
        self.assertEqual(validate_list_dates(node, 'list'), True)

    def test_validate_emissions_dates_invalid(self):
        node = {
            'list': [{
                'startDate': '2020-01-02',
                'endDate': '2020-01-01'
            }]
        }
        self.assertEqual(validate_list_dates(node, 'list'), {
            'level': 'error',
            'dataPath': '.list[0].endDate',
            'message': 'must be greater than startDate'
        })

    def test_validate_list_duplicates_valid(self):
        node = {
            'list': [{
                'startDate': '2020-01-01',
                'endDate': '2020-01-02',
                'value': 1,
                'nested': [{
                    'value': 1
                }]
            }, {
                'startDate': '2020-01-01',
                'endDate': '2020-01-02',
                'value': 2,
                'nested': [{
                    'value': 2
                }]
            }]
        }
        self.assertEqual(validate_list_duplicates(node, 'list', ['startDate', 'endDate', 'nested.value']), True)

    def test_validate_list_duplicates_invalid(self):
        node = {
            'list': [{
                'startDate': '2020-01-01',
                'endDate': '2020-01-02',
                'value': 1,
                'nested': [{
                    'value': 1
                }]
            }, {
                'startDate': '2020-01-01',
                'endDate': '2020-01-02',
                'value': 2,
                'nested': [{
                    'value': 1
                }, {
                    'value': 2
                }]
            }]
        }
        self.assertEqual(validate_list_duplicates(node, 'list', ['startDate', 'endDate', 'nested.value']), {
            'level': 'error',
            'dataPath': '.list[0]',
            'message': 'Duplicates found. '
            'Please make sure there is only one entry with the same startDate, endDate, nested.value'
        })

    def test_validate_list_min_max_valid(self):
        node = {
            'list': [{
                'min': 10,
                'max': 100
            }]
        }
        self.assertEqual(validate_list_min_max(node, 'list'), True)

    def test_validate_list_min_max_invalid(self):
        node = {
            'list': [{
                'min': 100,
                'max': 10
            }]
        }
        self.assertEqual(validate_list_min_max(node, 'list'), {
            'level': 'error',
            'dataPath': '.list[0].max',
            'message': 'must be greater than min'
        })

    def test_validate_country_valid(self):
        node = {
            'country': {
                '@id': 'GADM-AUS',
                'name': 'Australia'
            }
        }
        self.assertEqual(validate_country(node), True)
        node['country']['@id'] = 'region-world'
        self.assertEqual(validate_country(node), True)

    def test_validate_country_invalid(self):
        node = {
            'country': {
                '@id': 'random-term',
                'name': 'Random'
            }
        }
        self.assertEqual(validate_country(node), {
            'level': 'error',
            'dataPath': '.country',
            'message': 'must be a country'
        })

    def test_validate_region_valid(self):
        node = {
            'country': {
                '@id': 'GADM-AUS',
                'name': 'Australia'
            },
            'region': {
                '@id': 'GADM-AUS.1_1'
            }
        }
        self.assertEqual(validate_region(node), True)

    def test_validate_region_invalid(self):
        node = {
            'country': {
                '@id': 'GADM-AUS',
                'name': 'Australia'
            },
            'region': {
                '@id': 'GADM-FRA.1_1'
            }
        }
        self.assertEqual(validate_region(node), {
            'level': 'error',
            'dataPath': '.region',
            'message': 'must be within the country',
            'params': {
                'country': 'Australia'
            }
        })

    def test_validate_area_valid(self):
        with open(f"{fixtures_path}/shared/area/valid.json") as f:
            node = json.load(f)
        self.assertEqual(validate_area(node), True)

        # will return valid if the geojson is malformed
        del node['boundary']['features'][0]['type']
        self.assertEqual(validate_area(node), True)

    def test_validate_area_invalid(self):
        with open(f"{fixtures_path}/shared/area/invalid.json") as f:
            node = json.load(f)
        self.assertEqual(validate_area(node), {
            'level': 'error',
            'dataPath': '.area',
            'message': 'must be equal to boundary (~13.8)'
        })

    def test_validate_coordinates_valid(self):
        with open(f"{fixtures_path}/shared/coordinates/valid.json") as f:
            node = json.load(f)
        self.assertEqual(validate_coordinates(node), True)

    def test_validate_coordinates_invalid(self):
        with open(f"{fixtures_path}/shared/coordinates/invalid.json") as f:
            node = json.load(f)
        self.assertEqual(validate_coordinates(node), {
            'level': 'error',
            'dataPath': '.country',
            'message': 'does not contain latitude and longitude'
        })

    def test_need_validate_coordinates(self):
        node = {}
        self.assertEqual(need_validate_coordinates(node), False)
        node['latitude'] = 0
        node['longitude'] = 0
        self.assertEqual(need_validate_coordinates(node), True)

    def test_validate_list_term_percent_valid(self):
        with open(f"{fixtures_path}/shared/unit-percent/valid.json") as f:
            node = json.load(f)
        self.assertEqual(validate_list_term_percent(node, 'measurements'), True)

    def test_validate_list_term_percent_invalid(self):
        with open(f"{fixtures_path}/shared/unit-percent/invalid.json") as f:
            node = json.load(f)
        self.assertEqual(validate_list_term_percent(node, 'measurements'), {
            'level': 'error',
            'dataPath': '.measurements[0].value',
            'message': 'should be between 0 and 100 (percentage)'
        })

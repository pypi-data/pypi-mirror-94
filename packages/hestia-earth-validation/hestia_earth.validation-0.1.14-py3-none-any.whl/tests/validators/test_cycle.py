import unittest
import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.cycle import validate_cycle, validate_cycle_dates, validate_cycleDuration, \
    validate_functionalUnitMeasure, validate_relDays, validate_altStartDate, validate_startDate, \
    validate_economicValueShare


class TestValidatorsCycle(unittest.TestCase):
    def test_validate_valid(self):
        with open(f"{fixtures_path}/cycle/valid.json") as f:
            node = json.load(f)
        self.assertListEqual(validate_cycle(node), [True] * 19)

    def test_validate_cycle_dates_valid(self):
        cycle = {
            'startDate': '2020-01-01',
            'endDate': '2020-01-02'
        }
        self.assertEqual(validate_cycle_dates(cycle), True)
        cycle = {
            'startDate': '2020-01',
            'endDate': '2020-01'
        }
        self.assertEqual(validate_cycle_dates(cycle), True)
        cycle = {
            'startDate': '2020',
            'endDate': '2020'
        }
        self.assertEqual(validate_cycle_dates(cycle), True)

    def test_validate_cycle_dates_invalid(self):
        cycle = {
            'startDate': '2020-01-02',
            'endDate': '2020-01-01'
        }
        self.assertEqual(validate_cycle_dates(cycle), {
            'level': 'error',
            'dataPath': '.endDate',
            'message': 'must be greater than startDate'
        })
        cycle = {
            'startDate': '2020-01-01',
            'endDate': '2020-01-01'
        }
        self.assertEqual(validate_cycle_dates(cycle), {
            'level': 'error',
            'dataPath': '.endDate',
            'message': 'must be greater than startDate'
        })

    def test_validate_cycleDuration_valid(self):
        cycle = {
            'startDate': '2020-01-02',
            'endDate': '2021-01-01',
            'cycleDuration': 365
        }
        self.assertEqual(validate_cycleDuration(cycle), True)

    def test_validate_cycleDuration_invalid(self):
        cycle = {
            'startDate': '2020-01-02',
            'endDate': '2021-01-01',
            'cycleDuration': 200
        }
        self.assertEqual(validate_cycleDuration(cycle), {
            'level': 'error',
            'dataPath': '.cycleDuration',
            'message': 'must equal to endDate - startDate in days (~365.0)'
        })

    def test_validate_functionalUnitMeasure_valid(self):
        cycle = {
            'functionalUnitMeasure': '1 ha',
            'site': {
                'siteType': 'cropland'
            }
        }
        self.assertEqual(validate_functionalUnitMeasure(cycle), True)

    def test_validate_functionalUnitMeasure_invalid(self):
        cycle = {
            'functionalUnitMeasure': 'relative',
            'site': {
                'siteType': 'cropland'
            }
        }
        self.assertEqual(validate_functionalUnitMeasure(cycle), {
            'level': 'error',
            'dataPath': '.functionalUnitMeasure',
            'message': 'must equal to 1 ha'
        })

    def test_validate_relDays_valid(self):
        cycle = {
            'emissions': [{
                'value': [1],
                'relDays': [1]
            }]
        }
        self.assertEqual(validate_relDays(cycle, 'emissions'), True)

    def test_validate_relDays_invalid(self):
        cycle = {
            'emissions': [{
                'value': [1],
                'relDays': [1, 2]
            }]
        }
        self.assertEqual(validate_relDays(cycle, 'emissions'), {
            'level': 'error',
            'dataPath': '.emissions[0].relDays',
            'message': 'must contain 1 value'
        })

    def test_validate_altStartDate_valid(self):
        cycle = {
            'altStartDate': '2020-01-01',
            'altStartDateDefinition': 'the defintion'
        }
        self.assertEqual(validate_altStartDate(cycle), True)

    def test_validate_altStartDate_invalid(self):
        cycle = {
            'altStartDate': '2020-01-01',
            'altStartDateDefinition': ''
        }
        self.assertEqual(validate_altStartDate(cycle), {
            'level': 'error',
            'dataPath': '.altStartDateDefinition',
            'message': 'is required when using altStartDate'
        })

    def test_validate_startDate_valid(self):
        cycle = {
            'startDate': '2020-01-01'
        }
        self.assertEqual(validate_startDate(cycle), True)

    def test_validate_startDate_invalid(self):
        cycle = {
            'startDate': '2020-01-01',
            'altStartDate': '2020-01-01'
        }
        self.assertEqual(validate_startDate(cycle), {
            'level': 'error',
            'dataPath': '.altStartDate',
            'message': 'cannot be used with startDate'
        })

    def test_validate_economicValueShare_valid(self):
        products = [{
            'economicValueShare': 10
        }, {
            'economicValueShare': 80
        }]
        self.assertEqual(validate_economicValueShare(products), True)

    def test_validate_economicValueShare_invalid(self):
        products = [{
            'economicValueShare': 10
        }, {
            'economicValueShare': 90
        }, {
            'economicValueShare': 10
        }]
        self.assertEqual(validate_economicValueShare(products), {
            'level': 'error',
            'dataPath': '.products',
            'message': 'economicValueShare should sum to 100 or less across all products',
            'params': {
                'sum': 110
            }
        })

import unittest
import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.organisation import validate_organisation, validate_organisation_dates


class TestValidatorsOrganisation(unittest.TestCase):
    def test_validate_valid(self):
        with open(f"{fixtures_path}/organisation/valid.json") as f:
            node = json.load(f)
        self.assertListEqual(validate_organisation(node), [True] * 5)

    def test_validate_organisation_dates_valid(self):
        organisation = {
            'startDate': '2020-01-01',
            'endDate': '2020-01-02'
        }
        self.assertEqual(validate_organisation_dates(organisation), True)

    def test_validate_organisation_dates_invalid(self):
        organisation = {
            'startDate': '2020-01-02',
            'endDate': '2020-01-01'
        }
        self.assertEqual(validate_organisation_dates(organisation), {
            'level': 'error',
            'dataPath': '.endDate',
            'message': 'must be greater than startDate'
        })

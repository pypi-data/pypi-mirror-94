import unittest
import json
from hestia_earth.schema import SiteSiteType

from tests.utils import fixtures_path
from hestia_earth.validation.validators.site import validate_site, validate_site_dates, validate_site_coordinates


class TestValidatorsSite(unittest.TestCase):
    def test_validate_valid(self):
        with open(f"{fixtures_path}/site/valid.json") as f:
            node = json.load(f)
        self.assertListEqual(validate_site(node), [True] * 12)

    def test_validate_site_dates_valid(self):
        site = {
            'startDate': '2020-01-01',
            'endDate': '2020-01-02'
        }
        self.assertEqual(validate_site_dates(site), True)

    def test_validate_site_dates_invalid(self):
        site = {
            'startDate': '2020-01-02',
            'endDate': '2020-01-01'
        }
        self.assertEqual(validate_site_dates(site), {
            'level': 'error',
            'dataPath': '.endDate',
            'message': 'must be greater than startDate'
        })

    def test_need_validate_coordinates(self):
        site = {'siteType': SiteSiteType.CROPLAND.value}
        self.assertEqual(validate_site_coordinates(site), False)
        site['latitude'] = 0
        site['longitude'] = 0
        self.assertEqual(validate_site_coordinates(site), True)
        site['siteType'] = SiteSiteType.AQUACULTURE_PENS
        self.assertEqual(validate_site_coordinates(site), False)

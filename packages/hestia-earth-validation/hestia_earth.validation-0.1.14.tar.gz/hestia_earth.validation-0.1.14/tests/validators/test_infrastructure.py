import unittest
import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.infrastructure import validate_lifespan


class TestValidatorsInfrastructure(unittest.TestCase):
    def test_validate_lifespan_valid(self):
        with open(f"{fixtures_path}/infrastructure/lifespan/valid.json") as f:
            infrastructure = json.load(f)
        self.assertEqual(validate_lifespan([infrastructure]), True)

    def test_validate_lifespan_invalid(self):
        with open(f"{fixtures_path}/infrastructure/lifespan/invalid.json") as f:
            infrastructure = json.load(f)
        self.assertEqual(validate_lifespan([infrastructure]), {
            'level': 'error',
            'dataPath': '.infrastructure[0].lifespan',
            'message': 'must equal to endDate - startDate in decimal years (~2.6)'
        })

import unittest
import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.practice import validate_cropResidueManagement


class TestValidatorsPractice(unittest.TestCase):
    def test_validate_cropResidueManagement_valid(self):
        with open(f"{fixtures_path}/practice/cropResidueManagement/valid.json") as f:
            data = json.load(f)
        self.assertEqual(validate_cropResidueManagement(data.get('nodes')), True)

    def test_validate_cropResidueManagement_invalid(self):
        with open(f"{fixtures_path}/practice/cropResidueManagement/invalid.json") as f:
            data = json.load(f)
        self.assertEqual(validate_cropResidueManagement(data.get('nodes')), {
            'level': 'error',
            'dataPath': '.practices',
            'message': 'value should sum to 100 or less across crop residue management practices',
            'params': {
                'sum': 110
            }
        })

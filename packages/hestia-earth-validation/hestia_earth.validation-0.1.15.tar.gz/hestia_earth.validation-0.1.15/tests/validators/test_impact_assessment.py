import unittest
import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.impact_assessment import validate_impact_assessment


class TestValidatorsImpactAssessment(unittest.TestCase):
    def test_validate_valid(self):
        with open(f"{fixtures_path}/impactAssessment/valid.json") as f:
            node = json.load(f)
        self.assertListEqual(validate_impact_assessment(node), [True] * 8)

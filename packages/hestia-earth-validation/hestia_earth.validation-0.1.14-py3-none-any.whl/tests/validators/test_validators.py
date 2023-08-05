import unittest
from unittest.mock import patch
import json
from hestia_earth.schema import NodeType

from tests.utils import fixtures_path
from hestia_earth.validation.validators import validate_node


class TestValidators(unittest.TestCase):
    @patch('hestia_earth.validation.validators.validate_site')
    def test_validate_node_type_validation(self, mock_validate_site):
        node = {'type': NodeType.SITE.value}
        validate_node(node)
        mock_validate_site.assert_called_once_with(node)

    def test_validate_node_no_validation(self):
        node = {'@type': NodeType.ACTOR.value}
        self.assertEqual(validate_node(node), [])

    @patch('hestia_earth.validation.validators.validate_cycle')
    @patch('hestia_earth.validation.validators.validate_impact_assessment')
    @patch('hestia_earth.validation.validators.validate_site')
    def test_validate_nested(self, mock_validate_site, mock_validate_impact_assessment, mock_validate_cycle):
        with open(f"{fixtures_path}/impactAssessment/valid.json") as f:
            node = json.load(f)
        self.assertEqual(validate_node(node), [])
        self.assertEqual(mock_validate_cycle.call_count, 1)
        self.assertEqual(mock_validate_impact_assessment.call_count, 1)
        self.assertEqual(mock_validate_site.call_count, 2)

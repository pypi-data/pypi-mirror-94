from hestia_earth.validation.utils import _flatten
from .shared import validate_list_duplicates, validate_list_min_max, validate_region, validate_country, \
    validate_list_term_percent


def validate_impact_assessment(impact_assessment: dict):
    """
    Validates a single `ImpactAssessment`.

    Parameters
    ----------
    impact_assessment : dict
        The `ImpactAssessment` to validate.

    Returns
    -------
    List
        The list of errors for the `ImpactAssessment`, which can be empty if no errors detected.
    """
    return [
        validate_country(impact_assessment) if 'country' in impact_assessment else True,
        validate_region(impact_assessment) if 'region' in impact_assessment else True
    ] + _flatten([
        validate_list_min_max(impact_assessment, 'impacts'),
        validate_list_term_percent(impact_assessment, 'impacts'),
        validate_list_duplicates(impact_assessment, 'impacts', [
            'term.@id'
        ])
    ] if 'impacts' in impact_assessment else []) + _flatten([
        validate_list_min_max(impact_assessment, 'emissionsResourceUse'),
        validate_list_term_percent(impact_assessment, 'emissionsResourceUse'),
        validate_list_duplicates(impact_assessment, 'emissionsResourceUse', [
            'term.@id'
        ])
    ] if 'emissionsResourceUse' in impact_assessment else [])

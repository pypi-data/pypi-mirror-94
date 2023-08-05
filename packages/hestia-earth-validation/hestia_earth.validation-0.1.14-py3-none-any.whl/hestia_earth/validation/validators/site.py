from hestia_earth.schema import SiteSiteType

from .shared import validate_dates, validate_list_dates, validate_list_duplicates, \
    validate_list_min_max, validate_region, validate_country, validate_coordinates, need_validate_coordinates, \
    validate_area, need_validate_area, validate_list_term_percent
from .infrastructure import validate_lifespan
from .measurement import validate_soilTexture, validate_depths, validate_value_min_max
from .practice import validate_cropResidueManagement


INLAND_TYPES = [
    SiteSiteType.CROPLAND.value,
    SiteSiteType.PERMANENT_PASTURE.value,
    SiteSiteType.POND.value,
    SiteSiteType.BUILDING.value,
    SiteSiteType.FOREST.value,
    SiteSiteType.OTHER_NATURAL_VEGETATION.value
]


def validate_site_dates(site: dict):
    return validate_dates(site) or {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def validate_site_coordinates(site: dict):
    return need_validate_coordinates(site) and site.get('siteType') in INLAND_TYPES


def validate_site(site: dict):
    """
    Validates a single `Site`.

    Parameters
    ----------
    site : dict
        The `Site` to validate.

    Returns
    -------
    List
        The list of errors for the `Site`, which can be empty if no errors detected.
    """
    return [
        validate_site_dates(site),
        validate_country(site) if 'country' in site else True,
        validate_region(site) if 'region' in site else True,
        validate_coordinates(site) if validate_site_coordinates(site) else True,
        validate_area(site) if need_validate_area(site) else True
    ] + ([
        validate_list_dates(site, 'measurements'),
        validate_list_min_max(site, 'measurements'),
        validate_list_term_percent(site, 'measurements'),
        validate_soilTexture(site.get('measurements')),
        validate_depths(site.get('measurements')),
        validate_value_min_max(site.get('measurements')),
        validate_list_duplicates(site, 'measurements', [
            'term.@id',
            'method.@id',
            'methodDescription',
            'startDate',
            'endDate',
            'depthUpper',
            'depthLower'
        ])
    ] if 'measurements' in site else []) + ([
        validate_list_dates(site, 'infrastructure'),
        validate_lifespan(site.get('infrastructure'))
    ] if 'infrastructure' in site else []) + ([
        validate_list_dates(site, 'practices'),
        validate_list_min_max(site, 'practices'),
        validate_list_term_percent(site, 'practices'),
        validate_cropResidueManagement(site.get('practices'))
    ] if 'practices' in site else [])

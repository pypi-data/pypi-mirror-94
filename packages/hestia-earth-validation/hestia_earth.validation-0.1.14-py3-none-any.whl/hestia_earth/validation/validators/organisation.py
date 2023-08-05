from .shared import validate_dates, validate_region, validate_country, \
    need_validate_coordinates, validate_coordinates, \
    validate_area, need_validate_area


def validate_organisation_dates(organisation: dict):
    return validate_dates(organisation) or {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def validate_organisation(organisation: dict):
    """
    Validates a single `Organisation`.

    Parameters
    ----------
    organisation : dict
        The `Organisation` to validate.

    Returns
    -------
    List
        The list of errors for the `Organisation`, which can be empty if no errors detected.
    """
    return [
        validate_organisation_dates(organisation),
        validate_country(organisation) if 'country' in organisation else True,
        validate_region(organisation) if 'region' in organisation else True,
        validate_coordinates(organisation) if need_validate_coordinates(organisation) else True,
        validate_area(organisation) if need_validate_area(organisation) else True
    ]

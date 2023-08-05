from hestia_earth.schema import NodeType

from hestia_earth.validation.utils import _flatten
from .cycle import validate_cycle
from .impact_assessment import validate_impact_assessment
from .organisation import validate_organisation
from .site import validate_site


VALIDATE_NODE_TYPE = {
    NodeType.CYCLE.value: lambda v: validate_cycle(v),
    NodeType.IMPACTASSESSMENT.value: lambda v: validate_impact_assessment(v),
    NodeType.ORGANISATION.value: lambda v: validate_organisation(v),
    NodeType.SITE.value: lambda v: validate_site(v)
}


def _update_error(error: dict, key: str, index=None):
    path = f".{key}[{index}]{error.get('dataPath')}" if index is not None else f".{key}{error.get('dataPath')}"
    return {**error, **{'dataPath': path}}


def _validate_node_children(node: dict):
    validations = []
    for key, value in node.items():
        if isinstance(value, list):
            validations.extend([_validate_node_child(key, value, index) for index, value in enumerate(value)])
        if isinstance(value, dict):
            validations.append(_validate_node_child(key, value))
    return _flatten(validations)


def _validate_node_child(key: str, value: dict, index=None):
    values = validate_node(value)
    return list(map(lambda error: _update_error(error, key, index) if isinstance(error, dict) else error, values))


def validate_node(node: dict):
    """
    Validates a single Node.

    Parameters
    ----------
    node : dict
        The JSON-Node to validate.

    Returns
    -------
    List
        The list of errors for the node, which can be empty if no errors detected.
    """
    ntype = node.get('type', node.get('@type')) if isinstance(node, dict) else None
    if ntype is None:
        return []
    validations = _flatten(
        (VALIDATE_NODE_TYPE[ntype](node) if ntype in VALIDATE_NODE_TYPE else []) +
        _validate_node_children(node)
    )
    return list(filter(lambda v: v is not True, validations))

"""Utilities to access MR system specifications bundled with the package.

This module loads MRSystems.json (packaged under pulseq_systems/json) at import
time and provides helpers to query manufacturers, models, gradient
configurations and basic pulseq specifications.
"""

import json
import sys

if sys.version_info >= (3, 9):
    from importlib.resources import files
else:
    from importlib_resources import files

def _load_mr_systems():
    """Load MR systems data from the bundled JSON file.

    Returns:
        dict: Dictionary containing MR system configurations
    """
    package_files = files('pulseq_systems')
    json_file = package_files / 'json' / 'MRSystems.json'

    with json_file.open('r') as f:
        return json.load(f)

_systems = _load_mr_systems()
_metadata = _systems['_metadata']
del _systems['_metadata']

def list_manufacturers() -> list:
    """List all available MR system manufacturers.

    Returns:
        list: Manufacturer names present in the systems data.
    """
    return list(_systems.keys())

def list_models(manufacturer: str) -> list:
    """List all available models for a given manufacturer.

    Args:
        manufacturer (str): Manufacturer name.

    Returns:
        list: Model names for the given manufacturer.
    """
    return list(_systems[manufacturer].keys())

def list_gradients(manufacturer: str, model: str) -> list:
    """List gradient configurations available for a specific model.

    Args:
        manufacturer (str): Manufacturer name.
        model (str): Model name.

    Returns:
        list: Gradient configuration names for the given model.
    """
    return list(_systems[manufacturer][model]['gradient_configurations'].keys())

def get_pulseq_specs(manufacturer: str, model: str, gradient: str = None) -> dict:
    """Retrieve pulseq specifications for the specified system.

    If `gradient` is None the first available gradient configuration is used.

    Args:
        manufacturer (str): Manufacturer name.
        model (str): Model name.
        gradient (str, optional): Gradient configuration name. Defaults to None.

    Returns:
        dict: Dictionary with keys 'grad_unit', 'max_grad', 'max_slew', and 'B0'.
    """
    model_spec = _systems[manufacturer][model]['gradient_configurations']
    if not gradient:
        # select the first available gradient name in a safe, iterator-based way
        gradient = next(iter(model_spec))
    return {
        'grad_unit': 'mT/m',
        'max_grad': float(model_spec[gradient]['max_gradient_strength_mT_per_m']),
        'slew_unit': 'T/m/s',
        'max_slew': float(model_spec[gradient]['max_slew_rate_T_per_m_per_s']),
        'B0': float(_systems[manufacturer][model]['B0_field_strength_T'])
    }

def get_metadata():
    """Get the metadata of the system list

    Returns:
        dictionary: Metadata dictionary
    """

    return _metadata
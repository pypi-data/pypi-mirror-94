# -*- coding: utf-8 -*-

"""
control_parameters_step
A step for control parameters in SEAMM
"""

# Bring up the classes so that they appear to be directly in
# the control_parameters_step package.

from control_parameters_step.control_parameters import ControlParameters  # noqa: F401, E501
from control_parameters_step.control_parameters_parameters import ControlParametersParameters  # noqa: F401, E501
from control_parameters_step.control_parameters_step import ControlParametersStep  # noqa: F401, E501
from control_parameters_step.tk_control_parameters import TkControlParameters  # noqa: F401, E501

# Handle versioneer
from ._version import get_versions
__author__ = """Paul Saxe"""
__email__ = 'psaxe@molssi.org'
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions

# Classes and functions constituting the public API of this package.
# By importing them here, we make them importable from the package
# base namespace, i.e., "from yscoverage import T_CLASS",
# rather than from the submodule (yscoverage.coverage.T_CLASS).
# Any classes, functions, etc. in this package that are *not* thus published
# should be considered private APIs subject to change.
from .coverage import YangCoverage

# Additional storage paths defined by this package, if any
# from yangsuite.paths import register_path
# register_path(...)

# Must be set for auto-discovery by yangsuite core
default_app_config = 'yscoverage.apps.YScoverageConfig'

# Boilerplate for versioneer auto-versioning
from ._version import get_versions          # noqa: E402
__version__ = get_versions()['version']
del get_versions

# Classes and functions loaded when calling "from yscoverage import *".
# (Although users generally shouldn't do that!)
# Same list as the public API above, typically.
__all__ = (
    YangCoverage,
)

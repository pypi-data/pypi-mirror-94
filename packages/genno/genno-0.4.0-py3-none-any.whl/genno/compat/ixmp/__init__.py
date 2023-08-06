"""ixmp compatibility

Valid configuration keys—passed as *config* keyword arguments—include:

``rename_dims``: mapping of str -> str
   Update :obj:`.RENAME_DIMS`.
"""

try:
    import ixmp  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover
    HAS_IXMP = False
else:
    HAS_IXMP = True

import logging

from genno import Computer, config

log = logging.getLogger(__name__)


@config.handles("rename_dims", type_=dict, apply=False)
def rename_dims(c: Computer, info):
    """Handle one entry from the ``rename_dims:`` config section."""
    if not HAS_IXMP:  # pragma: no cover
        log.warning("Missing ixmp; configuration section 'rename_dims:' ignored")
        return

    from .util import RENAME_DIMS

    RENAME_DIMS.update(info)

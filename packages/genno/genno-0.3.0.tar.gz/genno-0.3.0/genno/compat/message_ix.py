from functools import partial  # pragma: no cover
from typing import Callable  # pragma: no cover

from genno.compat.pyam import util  # pragma: no cover


def collapse_message_cols(
    var: str = None, kind: str = None, var_cols=[]
) -> Callable:  # pragma: no cover
    """:meth:`as_pyam` `collapse=...` callback for MESSAGEix quantities.

    Wraps :func:`.collapse` with arguments particular to MESSAGEix.

    Parameters
    ----------
    var : str
        Name for 'variable' column.
    kind : None or 'ene' or 'emi', optional
        Determines which other columns are combined into the 'region' and 'variable'
        columns:

        - 'ene': 'variable' is
          ``'<var>|<level>|<commodity>|<technology>|<mode>'`` and 'region' is
          ``'<region>|<node_dest>'`` (if `var='out'`) or
          ``'<region>|<node_origin>'`` (if `'var='in'`).
        - 'emi': 'variable' is ``'<var>|<emission>|<technology>|<mode>'``.
        - Otherwise: 'variable' is ``'<var>|<technology>'``.
    """
    columns = dict(variable=[var] if var else [])

    if kind == "ene":
        # Region column
        columns["region"] = ["nd" if var == "out" else "no"]
        columns["variable"].extend(["l", "c", "t", "m"])
    elif kind == "emi":
        columns["variable"].extend(["e", "t", "m"])
    else:
        columns["variable"].extend(["t"] + var_cols)

    return partial(util.collapse, columns=columns, sep="|")

import pytest

from genno import Computer, Key, configure
from genno.compat.ixmp import HAS_IXMP
from genno.compat.pyam import HAS_PYAM
from genno.config import HANDLERS


def test_handlers():
    # Expected config handlers are available
    assert len(HANDLERS) == 8 + (1 * HAS_IXMP) + (1 * HAS_PYAM)
    for key, func in HANDLERS.items():
        assert isinstance(key, str) and callable(func)


@pytest.mark.parametrize(
    "name",
    [
        "config-aggregate.yaml",
        "config-combine.yaml",
        "config-general0.yaml",
        pytest.param(
            "config-general1.yaml", marks=pytest.mark.xfail(raises=ValueError)
        ),
        "config-report.yaml",
        "config-units.yaml",
    ],
)
def test_file(test_data_path, name):
    """Test handling configuration file syntax using test data files."""
    c = Computer()

    # Set up test contents
    c.add(Key("X", list("abc")), None, index=True, sums=True)
    c.add(Key("Y", list("bcd")), None, index=True, sums=True)

    c.configure(path=test_data_path / name)


def test_global(test_data_path):
    configure(path=test_data_path / "config-units.yaml")

    with pytest.raises(
        RuntimeError, match="Cannot apply non-global configuration without a Computer"
    ):
        configure(path=test_data_path / "config-global.yaml")

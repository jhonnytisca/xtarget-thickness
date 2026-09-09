import math

from xtarget_thickness.converter import (
    areal_density_to_nm,
    nm_to_areal_density,
)
from xtarget_thickness.models import Material


def test_germanium_conversion():
    ge = Material(
        symbol="Ge",
        name="Germanium",
        atomic_mass=72.630,
        density=5.323,
    )

    thickness = areal_density_to_nm(
        1000,
        ge,
    )

    assert math.isclose(
        thickness,
        226.573,
        rel_tol=1e-5,
    )


def test_round_trip():
    si = Material(
        symbol="Si",
        name="Silicon",
        atomic_mass=28.085,
        density=2.329,
    )

    original = 500.0

    thickness = areal_density_to_nm(
        original,
        si,
    )

    converted_back = nm_to_areal_density(
        thickness,
        si,
    )

    assert math.isclose(
        original,
        converted_back,
        rel_tol=1e-12,
    )

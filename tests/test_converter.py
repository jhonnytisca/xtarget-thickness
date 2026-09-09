import math

from xtarget_thickness.converter import (
    areal_density_to_nm,
    layer_to_nm,
    nm_to_areal_density,
)
from xtarget_thickness.models import Layer, Material


def test_mixed_layer_conversion():
    materials = {
        "Ge": Material(
            symbol="Ge",
            name="Germanium",
            atomic_mass=72.630,
            density=5.323,
        ),
        "Sn": Material(
            symbol="Sn",
            name="Tin",
            atomic_mass=118.710,
            density=7.310,
        ),
    }

    layer = Layer(
        number=1,
        areal_density=1000.0,
        elements={
            "Ge": 0.8,
            "Sn": 0.2,
        },
    )

    thickness_nm = layer_to_nm(
        layer,
        materials,
    )

    expected_nm = (
        1000.0
        * 1e15
        / 6.022_140_76e23
        * (0.8 * 72.630 / 5.323 + 0.2 * 118.710 / 7.310)
        * 1e7
    )

    assert math.isclose(
        thickness_nm,
        expected_nm,
        rel_tol=1e-12,
    )


def test_pure_layer_conversion():
    materials = {
        "Ge": Material(
            symbol="Ge",
            name="Germanium",
            atomic_mass=72.630,
            density=5.323,
        ),
    }

    layer = Layer(
        number=1,
        areal_density=1000.0,
        elements={
            "Ge": 1.0,
        },
    )

    thickness_nm = layer_to_nm(
        layer,
        materials,
    )

    assert math.isclose(
        thickness_nm,
        226.573,
        rel_tol=1e-5,
    )


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

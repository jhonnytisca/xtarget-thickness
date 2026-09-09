from .models import Layer, Material

AVOGADRO_CONSTANT = 6.022_140_76e23


def layer_to_nm(
    layer: Layer,
    materials: dict[str, Material],
) -> float:
    """
    Convert a SIMNRA layer areal density to physical thickness.

    The layer areal density is given in units of 1e15 atoms/cm².

    For mixed layers, the volume contribution of each element is
    calculated according to its atomic fraction, atomic mass, and
    configured density.
    """

    atoms_per_cm2 = layer.areal_density * 1e15

    molar_volume = 0.0

    for symbol, fraction in layer.elements.items():
        try:
            material = materials[symbol]
        except KeyError as exc:
            raise ValueError(f"No material data configured for {symbol!r}") from exc

        molar_volume += fraction * material.atomic_mass / material.density

    thickness_cm = atoms_per_cm2 / AVOGADRO_CONSTANT * molar_volume

    return thickness_cm * 1e7


def areal_density_to_nm(
    areal_density: float,
    material: Material,
) -> float:
    """
    Convert SIMNRA areal density to physical thickness in nanometers.

    Parameters
    ----------
    areal_density:
        SIMNRA layer thickness in units of 1e15 atoms/cm².

    material:
        Material containing atomic mass in g/mol and density in g/cm³.

    Returns
    -------
    float
        Physical thickness in nanometers.
    """

    atoms_per_cm2 = areal_density * 1e15

    mass_per_area_g_cm2 = atoms_per_cm2 * material.atomic_mass / AVOGADRO_CONSTANT

    thickness_cm = mass_per_area_g_cm2 / material.density

    return thickness_cm * 1e7


def nm_to_areal_density(
    thickness_nm: float,
    material: Material,
) -> float:
    """
    Convert physical thickness in nanometers to SIMNRA units
    of 1e15 atoms/cm².
    """

    thickness_cm = thickness_nm * 1e-7

    mass_per_area_g_cm2 = thickness_cm * material.density

    atoms_per_cm2 = mass_per_area_g_cm2 / material.atomic_mass * AVOGADRO_CONSTANT

    return atoms_per_cm2 / 1e15

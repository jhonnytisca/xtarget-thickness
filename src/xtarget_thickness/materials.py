import tomllib
from pathlib import Path

from .models import Material


def load_materials(path: Path) -> dict[str, Material]:
    with path.open("rb") as file:
        data = tomllib.load(file)

    materials: dict[str, Material] = {}

    for symbol, values in data.items():
        materials[symbol] = Material(
            symbol=symbol,
            name=str(values["name"]),
            atomic_mass=float(values["atomic_mass"]),
            density=float(values["density"]),
        )

    return materials

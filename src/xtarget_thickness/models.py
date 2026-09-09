from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Material:
    symbol: str
    name: str
    atomic_mass: float
    density: float

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Material:
    symbol: str
    name: str
    atomic_mass: float
    density: float


@dataclass(frozen=True, slots=True)
class Layer:
    number: int
    areal_density: float
    elements: dict[str, float]

    @property
    def composition(self) -> str:
        return ", ".join(
            f"{symbol} {fraction * 100:.2f}%"
            for symbol, fraction in self.elements.items()
        )

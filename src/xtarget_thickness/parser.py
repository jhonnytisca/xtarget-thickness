import xml.etree.ElementTree as ET
from pathlib import Path

from .models import Layer

IDF_NAMESPACE = "http://idf.schemas.itn.pt"

NS = {
    "idf": IDF_NAMESPACE,
}


class XTargetParseError(RuntimeError):
    """Raised when a SIMNRA xtarget file cannot be parsed."""


def _parse_float(text: str | None, field_name: str) -> float:
    if text is None:
        raise XTargetParseError(f"Missing value for {field_name}")

    try:
        return float(text.strip())
    except ValueError as exc:
        raise XTargetParseError(
            f"Invalid numeric value for {field_name}: {text!r}"
        ) from exc


def parse_xtarget(path: Path) -> list[Layer]:
    """
    Parse layers from a SIMNRA .xtarget file.

    Layer thickness is returned in SIMNRA units of
    1e15 atoms/cm².

    Element concentrations are returned as atomic fractions.
    """

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        raise XTargetParseError(f"Invalid XML in xtarget file: {path}") from exc

    root = tree.getroot()

    layer_nodes = root.findall(
        "./idf:sample/idf:structure/idf:layeredstructure/idf:layers/idf:layer",
        NS,
    )

    if not layer_nodes:
        raise XTargetParseError("No target layers found in xtarget file.")

    layers: list[Layer] = []

    for number, layer_node in enumerate(layer_nodes, start=1):
        thickness_node = layer_node.find(
            "idf:layerthickness",
            NS,
        )

        if thickness_node is None:
            raise XTargetParseError(f"Layer {number} has no layerthickness.")

        units = thickness_node.get("units")

        if units != "1e15at/cm2":
            raise XTargetParseError(
                f"Layer {number} uses unsupported thickness units: {units!r}"
            )

        areal_density = _parse_float(
            thickness_node.text,
            f"layer {number} thickness",
        )

        elements: dict[str, float] = {}

        element_nodes = layer_node.findall(
            "./idf:layerelements/idf:layerelement",
            NS,
        )

        if not element_nodes:
            raise XTargetParseError(f"Layer {number} has no elements.")

        for element_node in element_nodes:
            name_node = element_node.find(
                "idf:name",
                NS,
            )

            concentration_node = element_node.find(
                "idf:concentration",
                NS,
            )

            if name_node is None or not name_node.text:
                raise XTargetParseError(
                    f"Layer {number} contains an element without a name."
                )

            if concentration_node is None:
                raise XTargetParseError(
                    f"Layer {number}, element {name_node.text!r} has no concentration."
                )

            concentration_units = concentration_node.get("units")

            if concentration_units != "fraction":
                raise XTargetParseError(
                    f"Layer {number}, element {name_node.text!r} "
                    f"uses unsupported concentration units: "
                    f"{concentration_units!r}"
                )

            symbol = name_node.text.strip()

            concentration = _parse_float(
                concentration_node.text,
                (f"layer {number} concentration for {symbol}"),
            )

            elements[symbol] = concentration

        total_concentration = sum(elements.values())

        if abs(total_concentration - 1.0) > 1e-6:
            raise XTargetParseError(
                f"Layer {number} concentrations sum to "
                f"{total_concentration:.6f}, expected 1.0."
            )

        layers.append(
            Layer(
                number=number,
                areal_density=areal_density,
                elements=elements,
            )
        )

    return layers

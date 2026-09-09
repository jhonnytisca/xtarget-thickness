from csv import DictWriter
from pathlib import Path

from .converter import layer_to_nm
from .models import Layer, Material


def build_output_path(
    input_path: Path,
    extension: str,
) -> Path:
    return input_path.with_name(f"{input_path.stem}_composition.{extension}")


def write_csv(
    input_path: Path,
    layers: list[Layer],
    materials: dict[str, Material],
) -> Path:
    output_path = build_output_path(
        input_path,
        "csv",
    )

    material_symbols = list(materials.keys())

    fieldnames = [
        "layer",
        "composition",
        *[f"{symbol}_fraction" for symbol in material_symbols],
        "areal_density_1e15_at_cm2",
        "thickness_nm",
    ]

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for layer in layers:
            row = {
                "layer": layer.number,
                "composition": layer.composition,
                "areal_density_1e15_at_cm2": layer.areal_density,
                "thickness_nm": layer_to_nm(
                    layer,
                    materials,
                ),
            }

            for symbol in material_symbols:
                row[f"{symbol}_fraction"] = layer.elements.get(
                    symbol,
                    0.0,
                )

            writer.writerow(row)

    return output_path


def write_txt(
    input_path: Path,
    layers: list[Layer],
    materials: dict[str, Material],
) -> Path:
    output_path = build_output_path(
        input_path,
        "txt",
    )

    header = (
        f"{'Layer':<8}"
        f"{'Composition':<40}"
        f"{'Areal density [1e15 at/cm²]':>30}"
        f"{'Thickness [nm]':>20}"
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        file.write(f"Target: {input_path.name}\n\n")
        file.write(header + "\n")
        file.write("-" * len(header) + "\n")

        for layer in layers:
            thickness_nm = layer_to_nm(
                layer,
                materials,
            )

            file.write(
                f"{layer.number:<8}"
                f"{layer.composition:<40}"
                f"{layer.areal_density:>30.3f}"
                f"{thickness_nm:>20.3f}\n"
            )

    return output_path

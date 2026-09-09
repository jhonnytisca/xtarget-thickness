import argparse
import sys
from pathlib import Path

from .converter import layer_to_nm
from .materials import load_materials
from .parser import XTargetParseError, parse_xtarget
from .writer import write_csv, write_txt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="xtarget-thickness",
        description=(
            "Convert SIMNRA xtarget layer areal densities to physical thicknesses."
        ),
    )

    parser.add_argument(
        "file",
        type=Path,
        help="Path to the .xtarget file",
    )

    parser.add_argument(
        "--materials",
        type=Path,
        default=Path("materials.toml"),
        help=("Material configuration file (default: materials.toml)"),
    )

    parser.add_argument(
        "--no-csv",
        action="store_true",
        help="Do not write the CSV output file.",
    )

    parser.add_argument(
        "--no-txt",
        action="store_true",
        help="Do not write the TXT output file.",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.file.exists():
        print(
            f"Error: file does not exist: {args.file}",
            file=sys.stderr,
        )
        raise SystemExit(1)

    if not args.materials.exists():
        print(
            f"Error: material configuration does not exist: {args.materials}",
            file=sys.stderr,
        )
        raise SystemExit(1)

    try:
        materials = load_materials(args.materials)
        layers = parse_xtarget(args.file)
    except (XTargetParseError, KeyError, ValueError) as exc:
        print(
            f"Error: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc

    print()
    print(f"Target: {args.file}")
    print()

    header = (
        f"{'Layer':<8}"
        f"{'Composition':<40}"
        f"{'Areal density [1e15 at/cm²]':>30}"
        f"{'Thickness [nm]':>20}"
    )

    print(header)
    print("-" * len(header))

    for layer in layers:
        try:
            thickness_nm = layer_to_nm(
                layer,
                materials,
            )
            thickness_text = f"{thickness_nm:.3f}"

        except ValueError as exc:
            thickness_text = f"error: {exc}"

        print(
            f"{layer.number:<8}"
            f"{layer.composition:<40}"
            f"{layer.areal_density:>30.3f}"
            f"{thickness_text:>20}"
        )

    written_files: list[Path] = []

    if not args.no_csv:
        written_files.append(
            write_csv(
                args.file,
                layers,
                materials,
            )
        )

    if not args.no_txt:
        written_files.append(
            write_txt(
                args.file,
                layers,
                materials,
            )
        )

    if written_files:
        print()
        print("Written files:")

        for path in written_files:
            print(f"  {path}")


if __name__ == "__main__":
    main()

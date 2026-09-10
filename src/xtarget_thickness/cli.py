import argparse
import sys
from pathlib import Path

from .converter import areal_density_to_nm, layer_to_nm
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

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    file_parser = subparsers.add_parser(
        "file",
        help="Process a SIMNRA .xtarget file.",
    )

    file_parser.add_argument(
        "file",
        type=Path,
        help="Path to the .xtarget file.",
    )

    file_parser.add_argument(
        "--materials",
        type=Path,
        default=Path("materials.toml"),
    )

    file_parser.add_argument(
        "--no-csv",
        action="store_true",
        help="Do not write CSV output.",
    )

    file_parser.add_argument(
        "--no-txt",
        action="store_true",
        help="Do not write TXT output.",
    )

    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert an individual areal density.",
    )

    convert_parser.add_argument(
        "element",
        help="Element symbol, for example Ge, Sn or Si.",
    )

    convert_parser.add_argument(
        "areal_density",
        type=float,
        help="Areal density in units of 1e15 atoms/cm².",
    )

    convert_parser.add_argument(
        "--materials",
        type=Path,
        default=Path("materials.toml"),
    )

    return parser


def convert_element(args: argparse.Namespace) -> None:
    materials = load_materials(args.materials)

    material = materials.get(args.element)

    if material is None:
        available = ", ".join(materials)

        print(
            f"Error: unknown material {args.element!r}. "
            f"Available materials: {available}",
            file=sys.stderr,
        )
        raise SystemExit(1)

    thickness_nm = areal_density_to_nm(
        args.areal_density,
        material,
    )

    print(
        f"{args.areal_density:g} × 10^15 atoms/cm² "
        f"{args.element} = {thickness_nm:.3f} nm"
    )


def process_file(args: argparse.Namespace) -> None:
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


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "convert":
        convert_element(args)
        return

    if args.command == "file":
        process_file(args)
        return


if __name__ == "__main__":
    main()

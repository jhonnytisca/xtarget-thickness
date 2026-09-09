# xtarget-thickness

Small Python tool for reading SIMNRA `.xtarget` files and converting layer areal density into physical thickness.

The conversion uses configurable material densities and currently targets:

* Ge
* Sn
* Si
* C
* Pb

## Setup

This project uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Run the CLI with:

```bash
uv run xtarget-thickness target.xtarget
```

## Development

Run tests with:

```bash
uv run pytest
```

Check code formatting and linting with Ruff:

```bash
uv run ruff check .
uv run ruff format --check .
```

To automatically format the code:

```bash
uv run ruff format .
```

Material densities and atomic masses will be stored in a configuration file so they can be adjusted without modifying the conversion code.

## Status

Initial project setup. `.xtarget` parsing and thickness conversion are under development.

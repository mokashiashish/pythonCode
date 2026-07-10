#!/usr/bin/env python3
"""ReadRegex.py

Reads a source text file and extracts only text that matches the configured regex.
Writes matched content to /Users/ashishmokashi/Documents/Python/content/output_regex.txt.
"""
import json
import re
import sys
from pathlib import Path

CONFIG_FILENAME = "config.json"
DEFAULT_INPUT_PATH = Path("/Users/ashishmokashi/Documents/Python/content/Chemistry Questions.txt")
OUTPUT_PATH = Path("/Users/ashishmokashi/Documents/Python/content/output_regex.txt")


def load_config(cfg_path: Path) -> dict:
    if not cfg_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {cfg_path}")
    with cfg_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def normalize_matches(matches):
    processed = []
    for match in matches:
        if isinstance(match, tuple):
            processed.append("".join(str(item) for item in match))
        else:
            processed.append(str(match))
    return processed


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    config_path = script_dir / CONFIG_FILENAME

    try:
        config = load_config(config_path)
    except Exception as exc:
        print(f"Failed to load configuration: {exc}")
        return 1

    regex_pattern = config.get("regex")
    if not regex_pattern:
        print(f"Missing 'regex' value in {config_path}")
        return 1

    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1])
    else:
        input_path = DEFAULT_INPUT_PATH

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        print("Provide a source text file path as the first argument, or create the default source file at:")
        print(f"  {DEFAULT_INPUT_PATH}")
        return 1

    try:
        text = input_path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"Failed to read input file: {exc}")
        return 1

    try:
        compiled = re.compile(regex_pattern, flags=re.MULTILINE)
    except re.error as exc:
        print(f"Invalid regex pattern in config: {exc}")
        return 1

    matches = compiled.findall(text)
    matches = normalize_matches(matches)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        with OUTPUT_PATH.open("w", encoding="utf-8") as out_file:
            if not matches:
                out_file.write("")
                print(f"No regex matches found. Created empty output file: {OUTPUT_PATH}")
            else:
                out_file.write("\n".join(matches))
                print(f"Wrote {len(matches)} matches to: {OUTPUT_PATH}")
    except Exception as exc:
        print(f"Failed to write output file: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

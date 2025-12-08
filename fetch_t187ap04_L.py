import argparse
import csv
import json
import urllib.request
from pathlib import Path
from typing import Iterable, List, Mapping, Sequence

DATA_URL = "https://openapi.twse.com.tw/v1/opendata/t187ap04_L"
OUTPUT_PATH = Path("data/t187ap04_L.csv")


def fetch_opendata(url: str = DATA_URL) -> List[Mapping[str, str]]:
    with urllib.request.urlopen(url) as response:
        if response.status != 200:
            raise RuntimeError(f"Unexpected status code: {response.status}")
        return json.load(response)


def load_records_from_file(path: Path) -> List[Mapping[str, str]]:
    with path.open(encoding="utf-8") as infile:
        return json.load(infile)


def collect_fieldnames(records: Iterable[Mapping[str, str]]) -> List[str]:
    fieldnames: List[str] = []
    seen = set()
    for record in records:
        for key in record.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    return fieldnames


def write_csv(records: Sequence[Mapping[str, str]], path: Path = OUTPUT_PATH) -> None:
    if not records:
        raise ValueError("No records to write")

    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = collect_fieldnames(records)

    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download the TWSE t187ap04_L dataset or convert a downloaded JSON file to CSV."
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Path to a previously downloaded JSON file (if omitted, fetch from the API)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help=f"Path to write the CSV output (default: {OUTPUT_PATH})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.input:
        records = load_records_from_file(args.input)
    else:
        records = fetch_opendata()

    write_csv(records, path=args.output)


if __name__ == "__main__":
    main()

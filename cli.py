import argparse
import sys

from input_loader import load_assets
from scanner import scan_asset
from risk_engine import assess_risk


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Context-aware security exposure and risk assessment tool"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to CSV file containing asset list"
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        assets = load_assets(args.input)
    except Exception as e:
        print(f"[ERROR] Failed to load assets: {e}")
        sys.exit(1)

    if not assets:
        print("[INFO] No valid assets found. Exiting.")
        sys.exit(0)

    print(f"[INFO] Loaded {len(assets)} assets\n")

    for asset in assets:
        ip = asset["ip"]
        asset_type = asset["asset_type"]
        zone = asset["zone"]

        print(f"[+] Scanning {ip} ({asset_type}, {zone})")

        scan_result = scan_asset(ip)

        if "error" in scan_result:
            print(f"    [ERROR] {scan_result['error']}\n")
            continue

        risk_result = assess_risk(asset, scan_result)

        print(f"    Risk Level: {risk_result['risk_level']}")
        print("    Findings:")

        for finding in risk_result["findings"]:
            print(f"      - {finding}")

        print()  # blank line between assets


if __name__ == "__main__":
    main()

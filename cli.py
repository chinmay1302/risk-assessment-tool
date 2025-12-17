import argparse
import sys

from input_loader import load_assets
from scanner import scan_asset


def parse_arguments():
    parser = argparse.ArgumentParser()
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

        result = scan_asset(ip)

        if "error" in result:
            print(f"    [ERROR] {result['error']}")
            continue

        if not result["open_ports"]:
            print("    No open ports detected\n")
            continue

        print("    Open ports:")
        for port_info in result["open_ports"]:
            port = port_info["port"]
            service = port_info["service"]
            print(f"      - {port}/{service}")

        print()  # blank line between assets


if __name__ == "__main__":
    main()

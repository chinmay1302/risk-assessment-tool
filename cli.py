import sys
import os

from input_loader import load_assets
from pdf_loader import load_assets_from_pdf
from scanner import scan_asset
from risk_engine import assess_risk


def prompt_input_format():
    print("Select input format:")
    print("1. CSV file")
    print("2. PDF file")

    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        return "csv"
    elif choice == "2":
        return "pdf"
    else:
        print("[ERROR] Invalid choice.")
        sys.exit(1)


def prompt_file_path(expected_ext):
    file_path = input(f"Enter path to {expected_ext.upper()} file: ").strip()

    if not os.path.exists(file_path):
        print("[ERROR] File does not exist.")
        sys.exit(1)

    if not file_path.lower().endswith(f".{expected_ext}"):
        print(f"[ERROR] Expected a .{expected_ext} file.")
        sys.exit(1)

    return file_path


def main():
    print("\n=== Context-Aware Security Risk Assessment Tool ===\n")

    input_type = prompt_input_format()

    try:
        if input_type == "csv":
            file_path = prompt_file_path("csv")
            assets = load_assets(file_path)

        elif input_type == "pdf":
            file_path = prompt_file_path("pdf")
            assets = load_assets_from_pdf(file_path)

    except Exception as e:
        print(f"[ERROR] Failed to load assets: {e}")
        sys.exit(1)

    if not assets:
        print("[INFO] No valid assets found. Exiting.")
        sys.exit(0)

    print(f"\n[INFO] Loaded {len(assets)} assets")
    print("[INFO] Starting assessment...\n")

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

        print()


if __name__ == "__main__":
    main()

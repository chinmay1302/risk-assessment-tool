import csv
import ipaddress
import os

ALLOWED_ASSET_TYPES = {'hmi', 'server', 'nas', 'workstation', 'printer'}
ALLOWED_IP_VERSIONS = {4, 6}
ALLOWED_ZONES = {'internal', 'external', 'dmz'}




def is_valid_ipv4(ip: str) -> bool:
    """
    Validate IPv4 address format.
    """
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        return False

def is_valid_ipv6(ip: str) -> bool:
    """
    Validate IPv6 address format.
    """
    try:
        ipaddress.IPv6Address(ip)
        return True
    except ValueError:
        return False
    

def is_valid_asset_type(asset_type: str) -> bool:
    """
    Check if asset type is allowed.
    """
    return asset_type in ALLOWED_ASSET_TYPES

def is_valid_ip_version(version: int) -> bool:
    """
    Check if IP version is allowed.
    """
    return version in ALLOWED_IP_VERSIONS

def is_valid_zone(zone: str) -> bool:
    """
    Check if zone is allowed.
    """
    return zone in ALLOWED_ZONES




def load_assets(file_path:str) -> list:
    """
    Load and validate assets from a CSV file.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    assets = []
    seen_ips = set()

    with open(file_path,newline="",encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        required_columns = {"ip", "asset_type", "zone"}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                f"CSV must contain columns: {', '.join(required_columns)}"
            )

        for row_number, row in enumerate(reader, start=2):

            ip = row.get("ip", "").strip()
            asset_type = row.get("asset_type", "").strip().lower()
            zone = row.get("zone", "").strip().lower()

            if not ip or not asset_type or not zone:
                print(f"[WARN] Row {row_number}: Missing required fields. Skipped.")
                continue

            if not is_valid_ipv4(ip):
                print(f"[WARN] Row {row_number}: Invalid IP '{ip}'. Skipped.")
                continue

            if not is_valid_asset_type(asset_type):
                print(
                    f"[WARN] Row {row_number}: Invalid asset_type '{asset_type}'. Skipped."
                )
                continue

            if not is_valid_zone(zone):
                print(f"[WARN] Row {row_number}: Invalid zone '{zone}'. Skipped.")
                continue

            if ip in seen_ips:
                print(f"[WARN] Row {row_number}: Duplicate IP '{ip}'. Skipped.")
                continue

            assets.append(
                {
                    "ip": ip,
                    "asset_type": asset_type,
                    "zone": zone,
                }
            )
            seen_ips.add(ip)

    return assets
import pdfplumber
import ipaddress


ALLOWED_ASSET_TYPES = {"server", "nas", "hmi", "workstation"}
ALLOWED_ZONES = {"internal", "dmz", "external"}


def is_valid_ipv4(ip: str) -> bool:
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        return False


def normalize_header(header: str) -> str:
    return header.strip().lower().replace(" ", "_")


def load_assets_from_pdf(file_path: str) -> list:
    assets = []
    seen_ips = set()

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                if not table or len(table) < 2:
                    continue

                headers = [normalize_header(h) for h in table[0]]

                try:
                    ip_idx = headers.index("ip_address")
                except ValueError:
                    try:
                        ip_idx = headers.index("ip")
                    except ValueError:
                        continue

                try:
                    asset_idx = headers.index("asset_type")
                    zone_idx = headers.index("zone")
                except ValueError:
                    continue

                for row in table[1:]:
                    try:
                        ip = row[ip_idx].strip()
                        asset_type = row[asset_idx].strip().lower()
                        zone = row[zone_idx].strip().lower()
                    except Exception:
                        continue

                    if not is_valid_ipv4(ip):
                        continue
                    if asset_type not in ALLOWED_ASSET_TYPES:
                        continue
                    if zone not in ALLOWED_ZONES:
                        continue
                    if ip in seen_ips:
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

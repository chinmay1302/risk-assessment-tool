import nmap


def scan_asset(ip: str) -> dict:

    scanner = nmap.PortScanner()

    try:
        scanner.scan(
            hosts=ip,
            arguments="-sT -sV -T3 --open --host-timeout 30s --max-retries 1"
        )
    except Exception as e:
        return {
            "ip": ip,
            "error": f"Scan failed: {str(e)}"
        }

    results = {
        "ip": ip,
        "open_ports": []
    }

    if ip not in scanner.all_hosts():
        return {
            "ip": ip,
            "error": "Host appears to be down or unreachable (no response from nmap)"
        }

    for protocol in scanner[ip].all_protocols():
        ports = scanner[ip][protocol].keys()
        for port in ports:
            service = scanner[ip][protocol][port].get("name", "unknown")
            results["open_ports"].append(
                {
                    "port": port,
                    "service": service
                }
            )

    return results

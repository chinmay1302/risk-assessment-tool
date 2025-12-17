import nmap


def scan_asset(ip: str) -> dict:

    scanner = nmap.PortScanner()

    try:
        scanner.scan(
            hosts=ip,
            arguments="-sT -sV -T2 --open"
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
        return results

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

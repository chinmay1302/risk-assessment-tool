MANAGEMENT_PORTS = {22, 3389, 445}


def is_management_port(port: int) -> bool:
    return port in MANAGEMENT_PORTS


def higher_risk(current: str, new: str) -> str:
    priority = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
    return new if priority[new] > priority[current] else current


def assess_risk(asset: dict, scan_result: dict) -> dict:
    risk_level = "LOW"
    findings = []

    asset_type = asset["asset_type"]
    zone = asset["zone"]
    open_ports = scan_result.get("open_ports", [])

    if not open_ports:
        findings.append("No exposed services detected")
        return {
            "risk_level": risk_level,
            "findings": findings
        }

    for entry in open_ports:
        port = entry["port"]
        service = entry["service"]

        # Rule: DMZ exposure
        if zone == "dmz":
            risk_level = higher_risk(risk_level, "MEDIUM")
            findings.append(f"{service.upper()} exposed in DMZ")

        # Rule: Management services
        if is_management_port(port):
            if zone == "dmz":
                risk_level = higher_risk(risk_level, "HIGH")
                findings.append(
                    f"Management service {service.upper()} exposed in DMZ"
                )
            else:
                risk_level = higher_risk(risk_level, "MEDIUM")
                findings.append(
                    f"Management service {service.upper()} exposed internally"
                )

        # Rule: Insecure web service
        if port == 80:
            risk_level = higher_risk(risk_level, "MEDIUM")
            findings.append("Unencrypted HTTP service exposed")

    return {
        "risk_level": risk_level,
        "findings": list(set(findings))
    }

Context-Aware Security Risk Assessment Tool
Overview

This project is a Python-based tool I built to quickly assess security exposure and risk across multiple systems in a project.

In environments where projects involve many servers, HMIs, NAS systems, and engineering workstations, security checks are often done manually or very late in the process. This tool automates visibility and basic risk prioritization while keeping the assessment safe and non-intrusive.

The focus is on understanding what is exposed and what matters, not on exploitation or penetration testing.

Why I built this

During project work, asset lists are usually already available as CSV files or PDF documents (for example, system lists used during FAT/SAT or audits).

However:

Reviewing each system one by one is slow

It’s hard to prioritize which exposures actually matter

Results are often not consistent across projects

This tool takes those existing documents and gives a clear, repeatable security view of the project in one run.

What the tool does

Loads a list of systems from CSV or structured PDF files

Performs safe service discovery using controlled scans

Applies context-based rules using asset type and network zone

Outputs simple, human-readable risk findings

It is designed to be usable by engineers, not just developers.

What the tool does NOT do

No exploitation or attack simulation

No credential testing

No interaction with PLCs or field devices

No aggressive scanning

The goal is visibility and prioritization, not testing system resilience.

Supported inputs-

    csv
    pdf


How to run
Setup

python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


Ensure Nmap is installed:

nmap --version

Run the tool
python cli.py


The CLI will guide you through selecting the input type and file.

Example Output
[INFO] Loaded 3 assets
[INFO] Starting assessment...

[+] Scanning 10.10.1.30 (hmi, dmz)
    Risk Level: HIGH
    Findings:
      - Management service SSH exposed in DMZ

Author

Chinmay Maheshwari
Cybersecurity | Controls & Digitalization | Python Automation


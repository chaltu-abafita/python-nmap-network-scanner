"""
nmap.py

This file contains code to run Nmap scans..
It creates both a text report and an HTML report in a 'reports' folder.

The main function here is: manage_nmap_scans()
"""

import subprocess
import datetime
import os


def create_reports_folder():
    """
    Make sure the 'reports' folder exists.
    If the folder does not exist, this function will create it.
    """
    if not os.path.exists("reports"):
        os.makedirs("reports")


def ask_for_target_and_company():
    """
    Ask the user for the target and the company name.

    Returns:
        target: The IP address or domain name to scan.
        company_name: The company name to use in report filenames.
    """
    target = input("Enter the target IP or domain: ")

    # Automatically remove http:// or https:// if user enters it
    if target.startswith("http://"):
        target = target.replace("http://", "")
    elif target.startswith("https://"):
        target = target.replace("https://", "")

    company_name = input("Enter the company name for the report: ")
    return target, company_name


def ask_for_port_range():
    """
    Ask the user if they want to scan all ports or a specific range.

    Returns:
        ports_option: A string like '1-1000', '80,443', or None for all ports.
    """
    print()
    print("Port options:")
    print("1. Scan all default ports.")
    print("2. Enter a custom port or port range (for example: 80 or 1-1000 or 80,443)")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "2":
        ports = input("Enter the port or port range: ").strip()
        if ports == "":
            print("No ports entered. Using default ports instead.")
            return None
        return ports
    else:
        print("Using default ports.")
        return None


def build_report_filenames(company_name):
    """
    Create filenames for the text and HTML reports using the company name and timestamp.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    safe_company = company_name.replace(" ", "_")
    txt_filename = os.path.join("reports", f"{safe_company}_nmap_report_{timestamp}.txt")
    html_filename = os.path.join("reports", f"{safe_company}_nmap_report_{timestamp}.html")
    return txt_filename, html_filename, timestamp

def run_nmap_command(arguments):
    """
    Run an Nmap command using subprocess and return the output as text.
    """
    try:
        result = subprocess.check_output(arguments, text=True, stderr=subprocess.STDOUT)
        return result

    except subprocess.CalledProcessError as error:
        return f"Nmap returned an error:\n{error.output}\n"

    except FileNotFoundError:
        return "Error: Nmap is not installed or not found in system PATH.\n"

    except OSError as error:
        return f"System error while running Nmap: {error}\n"

    except Exception as error:  # fallback, but no longer “too general”
        return f"Unexpected runtime error: {type(error).__name__}: {error}\n"

def write_text_report(
    txt_filename,
    company_name,
    target,
    timestamp,
    ports_option,
    service_scan_output,
    aggressive_scan_output,
    os_scan_output,
):
    """
    Write the text report to a .txt file.
    """
    with open(txt_filename, "w", encoding="utf-8") as report:
        report.write(f"Nmap Scan Report for {company_name}\n")
        report.write(f"Target: {target}\n")
        report.write(f"Date: {timestamp}\n")
        if ports_option:
            report.write(f"Ports: {ports_option}\n")
        else:
            report.write("Ports: Default Nmap ports\n")
        report.write("=" * 60 + "\n\n")

        report.write("Service/Version Scan (-sV)\n")
        report.write("-" * 40 + "\n")
        report.write(service_scan_output + "\n\n")

        report.write("Aggressive Scan (-A)\n")
        report.write("-" * 40 + "\n")
        report.write(aggressive_scan_output + "\n\n")

        report.write("OS Detection Scan (-O)\n")
        report.write("-" * 40 + "\n")
        report.write(os_scan_output + "\n\n")


def write_html_report(
    html_filename,
    company_name,
    target,
    timestamp,
    ports_option,
    service_scan_output,
    aggressive_scan_output,
    os_scan_output,
):
    """
    Write the HTML report to a .html file.
    """
    with open(html_filename, "w", encoding="utf-8") as report:
        report.write("<!DOCTYPE html>\n")
        report.write("<html>\n<head>\n")
        report.write("<meta charset='UTF-8'>\n")
        report.write(f"<title>Nmap Report for {company_name}</title>\n")
        report.write("<style>\n")
        report.write("body { font-family: Arial, sans-serif; background-color: #f5f5f5; }\n")
        report.write(".container { width: 90%; margin: auto; background: white; padding: 20px; }\n")
        report.write("h1, h2 { color: #333333; }\n")
        report.write("pre { background: #222222; color: #f1f1f1; padding: 10px; overflow-x: auto; }\n")
        report.write("</style>\n")
        report.write("</head>\n<body>\n")
        report.write("<div class='container'>\n")

        report.write(f"<h1>Nmap Scan Report for {company_name}</h1>\n")
        report.write(f"<p><strong>Target:</strong> {target}</p>\n")
        report.write(f"<p><strong>Date:</strong> {timestamp}</p>\n")
        if ports_option:
            report.write(f"<p><strong>Ports:</strong> {ports_option}</p>\n")
        else:
            report.write("<p><strong>Ports:</strong> Default Nmap ports</p>\n")
        report.write("<hr />\n")

        report.write("<h2>Service/Version Scan (-sV)</h2>\n")
        report.write("<pre>\n")
        report.write(service_scan_output)
        report.write("</pre>\n")

        report.write("<h2>Aggressive Scan (-A)</h2>\n")
        report.write("<pre>\n")
        report.write(aggressive_scan_output)
        report.write("</pre>\n")

        report.write("<h2>OS Detection Scan (-O)</h2>\n")
        report.write("<pre>\n")
        report.write(os_scan_output)
        report.write("</pre>\n")

        report.write("</div>\n</body>\n</html>\n")


def manage_nmap_scans():
    """
    Manage the automated Nmap scanning process.
    """
    print("\nWelcome to the Automated Nmap Scanner\n")

    create_reports_folder()
    target, company_name = ask_for_target_and_company()
    ports_option = ask_for_port_range()

    txt_filename, html_filename, timestamp = build_report_filenames(company_name)

    base_cmd = ["nmap"]

    if ports_option:
        base_cmd += ["-p", ports_option]

    print("Running Service/Version Scan (-sV)...")
    service_cmd = base_cmd + ["-sV", target]
    service_scan_output = run_nmap_command(service_cmd)

    print("Running Aggressive Scan (-A)...")
    aggressive_cmd = base_cmd + ["-A", target]
    aggressive_scan_output = run_nmap_command(aggressive_cmd)

    print("Running OS Detection Scan (-O)...")
    os_cmd = base_cmd + ["-O", target]
    os_scan_output = run_nmap_command(os_cmd)

    write_text_report(
        txt_filename,
        company_name,
        target,
        timestamp,
        ports_option,
        service_scan_output,
        aggressive_scan_output,
        os_scan_output,
    )

    write_html_report(
        html_filename,
        company_name,
        target,
        timestamp,
        ports_option,
        service_scan_output,
        aggressive_scan_output,
        os_scan_output,
    )

    print()
    print("Scan complete!")
    print(f"Text report saved as: {txt_filename}")
    print(f"HTML report saved as: {html_filename}")
    print()
